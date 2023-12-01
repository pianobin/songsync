# songsync (WIP)

Convert YT playlists to Spotify playlists

## Installation

Install poetry: https://python-poetry.org/docs/#installation

Setup and activate virtual environment

```
python3 -m venv .venv && source .venv/bin/activate
```

Install poetry dependencies

```
poetry install
```

Create a Spotify app by following the instructions in the Spotify Web API documentation: https://developer.spotify.com/documentation/web-api

Set the following environment variables

```
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-app-redirect-url'
```

## Run

The YT playlist ID can be found from the URL of your Youtube/Youtube Music playlist. The YT playlist must be public/unlisted. Run the script:

```
python3 app.py --yt_playlist_id PLwjEXrvFo-2Bs1-hvfjQ_G61COZ0aBTK5 --spotify_playlist_name "My Playlist"
```
