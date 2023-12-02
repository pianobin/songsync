"""Spotify helper functions"""
import json
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from songsync.yt_helpers import YTSong


def auth_to_spotify() -> Spotify:
    """authenticate to Spotify

    Returns:
        Spotify: Spotify object
    """
    scope = ",".join(
        [
            "user-read-private",
            "user-read-email",
            "playlist-modify-public",
            "playlist-modify-private",
        ]
    )
    return Spotify(auth_manager=SpotifyOAuth(scope=scope))


def search_spotify_track(title: str, artist: str, sp: Spotify) -> str | None:
    """Search Spotify for a track that matches the queried title and artist

    Args:
        title (str): Spotify track title
        artist (str): Spotify track artist
        sp (Spotify): Spotify object

    Returns:
        str | None: Spotify track uri or None if not found
    """
    query = f"track:{title} artist:{artist}"
    params = {
        "q": query,
        "type": "track",
    }
    track_items = sp.search(
        params["q"],
        type=params["type"],
    )[
        "tracks"
    ]["items"]
    if not track_items:
        return None
    return track_items[0]["uri"]


def create_spotify_playlist(
    playlist: list[YTSong], new_playlist_name: str, interactive_mode: bool
):
    """create a Spotify playlist with the given name from a YouTube playlist

    Args:
        playlist (list[YTSong]): YouTube playlist to convert to Spotify
        new_playlist_name (str): Spotify playlist name to be created
        interactive_mode (bool): If true, support manually adding songs that can't be found
    """
    sp = auth_to_spotify()
    sp_user_id = sp.current_user()["id"]

    new_playlist_id = sp.user_playlist_create(
        sp_user_id, new_playlist_name, public=False
    )["id"]

    uris_to_add = []
    tracks_not_found = []

    for index, track in enumerate(playlist):
        title, artist = track["title"], track["artist"]
        track_uri = search_spotify_track(title, artist, sp)
        while not track_uri and interactive_mode:
            user_input = input(
                f"({index+1}/{len(playlist)}) Unable to find [title] {title} [artist] {artist}\nPlease enter a title and artist comma-separated as it would appear in Spotify US to search again (or enter blank to skip): "
            )
            if not user_input:
                print("Skipping.")
                break
            user_input_parts = user_input.split(",", 1)
            if len(user_input_parts) != 2:
                print("Could not parse input.")
                continue
            title, artist = user_input_parts[0], user_input_parts[1]
            track_uri = search_spotify_track(title, artist, sp)
        if track_uri:
            print(f"({index+1}/{len(playlist)}) Found {title} - {artist}: {track_uri}")
            uris_to_add.append(track_uri)
        else:
            tracks_not_found.append(f"{title} - {artist}")

    sp.user_playlist_add_tracks(sp_user_id, new_playlist_id, uris_to_add)
    print(f"Created new Spotify playlist {new_playlist_name}")
    print(
        "Could not find the following tracks",
        json.dumps(tracks_not_found, indent=4, ensure_ascii=False),
    )
