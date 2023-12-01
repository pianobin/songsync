import argparse
import json
import re
from ytmusicapi import YTMusic
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Create the parser
parser = argparse.ArgumentParser(description="songsync")

# Add arguments
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

# Parse arguments
args = parser.parse_args()

# Accessing the arguments
yt_playlist_id = args.yt_playlist_id
spotify_playlist_name = args.spotify_playlist_name

ytmusic = YTMusic()

tracks = ytmusic.get_playlist(yt_playlist_id)["tracks"]

playlist = []
for track in tracks:
    cleaned_title = re.sub(r"\(.*?\)|\[.*?\]", "", track["title"])
    cleaned_artist_name = re.sub(r"\(.*?\)|\[.*?\]", "", track["artists"][0]["name"])
    playlist.append({"title": cleaned_title, "artist": cleaned_artist_name})

SCOPE = (
    "user-read-private,user-read-email,playlist-modify-public,playlist-modify-private"
)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE))
sp_user_id = sp.current_user()["id"]

new_playlist_id = sp.user_playlist_create(
    sp_user_id, spotify_playlist_name, public=False
)["id"]

uris_to_add = []
songs_not_found = []
SEARCH_URL = "https://api.spotify.com/v1/search"

for track in playlist:
    title, artist = track["title"], track["artist"]
    query = f"track:{title} artist:{artist}"
    params = {
        "q": query,
        "type": "track",
        "limit": 10,
    }
    track_items = sp.search(
        params["q"],
        limit=params["limit"],
        type=params["type"],
    )[
        "tracks"
    ]["items"]
    if not track_items:
        songs_not_found.append(f"{title} {artist}")
        continue
    track_uri = track_items[0]["uri"]
    uris_to_add.append(track_uri)

print("Adding", json.dumps(uris_to_add, indent=4, ensure_ascii=False))
sp.user_playlist_add_tracks(sp_user_id, new_playlist_id, uris_to_add)

print("Couldn't find", json.dumps(songs_not_found, indent=4, ensure_ascii=False))
