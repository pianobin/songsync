"""Module converting YouTube playlists to Spotify playlists"""
import argparse
import dataclasses
import json
from ytmusicapi import YTMusic
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth


@dataclasses.dataclass
class YTSong:
    """Class representing a YouTube track"""

    title: str
    artist: str


def get_yt_playlist(playlist_id: str) -> list[YTSong]:
    """fetch and parse playlist from YouTube

    Args:
        playlist_id (str): YouTube playlist ID

    Returns:
        list[YTSong]: list of YouTube tracks
    """
    ytmusic = YTMusic()

    tracks = ytmusic.get_playlist(playlist_id)["tracks"]

    playlist = []
    for track in tracks:
        title = track["title"]
        artist = track["artists"][0]["name"]
        playlist.append({"title": title, "artist": artist})
    print(f"Parsed {len(playlist)} YT tracks")
    return playlist


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
    """Search Spotify for a track that matches the provided title and artist

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


def create_spotify_playlist(playlist: list[YTSong], new_playlist_name: str):
    """create a Spotify playlist with the provided name from a YouTube playlist

    Args:
        playlist (list[YTSong]): YouTube playlist to convert to Spotify
        new_playlist_name (str): Spotify playlist name to be created
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
        while not track_uri:
            user_input = input(
                f"({index+1}/{len(playlist)}) Unable to find [title] {title} [artist] {artist}\nPlease enter a title and artist comma-separated as it would appear in Spotify US to search again (or enter blank to skip): "
            )
            if not user_input:
                print("Skipping.")
                tracks_not_found.append(f"{title} - {artist}")
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

    sp.user_playlist_add_tracks(sp_user_id, new_playlist_id, uris_to_add)
    print(f"Created new Spotify playlist {new_playlist_name}")
    print("Couldn't find", json.dumps(tracks_not_found, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="songsync")

    parser.add_argument(
        "--yt_playlist_id",
        required=True,
        type=str,
        help="YT playlist ID to be converted to Spotify",
    )
    parser.add_argument(
        "--spotify_playlist_name",
        required=True,
        type=str,
        help="Name of Spotify playlist to create",
    )

    args = parser.parse_args()

    yt_playlist_id = args.yt_playlist_id
    spotify_playlist_name = args.spotify_playlist_name

    yt_playlist = get_yt_playlist(playlist_id=yt_playlist_id)
    create_spotify_playlist(
        playlist=yt_playlist, new_playlist_name=spotify_playlist_name
    )
