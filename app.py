import json
import os
import requests
from ytmusicapi import YTMusic
import spotipy
from spotipy.oauth2 import SpotifyOAuth

YT_PLAYLIST_ID = "PLwjEXrvFo-2CqNmxxKYRIwObfWnn0soiA"

ytmusic = YTMusic()

tracks = ytmusic.get_playlist(YT_PLAYLIST_ID)["tracks"]

playlist = []
for track in tracks:
    playlist.append({"title": track["title"], "artist": track["artists"][0]["name"]})

print("Imported songs from YT", playlist)

# Get Spotify User ID
scope = "user-read-private,user-read-email,playlist-modify-public,playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
sp_user_id = sp.current_user()["id"]
print("Spotify user ID", sp_user_id)

new_playlist_id = sp.user_playlist_create(sp_user_id, 'kpop', public=False)["id"]
print("Spotify playlist ID", new_playlist_id)

uris_to_add = []
songs_not_found = []

for track in playlist:
    title, artist = track['title'], track['artist']
    search_url = "https://api.spotify.com/v1/search"
    query = f"track:{title} artist:{artist}"
    params = {
        'q': query,
        'type': 'track',
        'market': 'US',
        'limit': 10,
    }
    track_items = sp.search(params['q'], limit=params['limit'], type=params['type'], market=params['market'])["tracks"]["items"]
    if not track_items:
        songs_not_found.append(f"{title} {artist}")
        continue
    track_uri = track_items[0]["uri"]
    uris_to_add.append(track_uri)

print("Adding ", uris_to_add)
sp.user_playlist_add_tracks(sp_user_id, new_playlist_id, uris_to_add)

print("Couldn't find", songs_not_found)