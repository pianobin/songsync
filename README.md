# songsync

Convert YT playlists to Spotify playlists

## Setup

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
python3 examples/convert_yt_to_spotify_playlist.py --yt_playlist_id PLwjEXrvFo-2Bs1-hvfjQ_G61COZ0aBTK5 --spotify_playlist_name "My Playlist"
```

For interactive mode, include the `--interactive` flag.

Example:

```
python3 examples/convert_yt_to_spotify_playlist.py --yt_playlist_id PLwjEXrvFo-2Bs1-hvfjQ_G61COZ0aBTK5 --spotify_playlist_name "My Playlist" --interactive
```

In interactive mode, if the script cannot find the YouTube track on Spotify you will be prompted to manually enter a title and artist. Enter it as it would appear on the Spotify US market. You can enter blank in the prompt to skip.
