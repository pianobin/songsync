#!/bin/bash

# Function to display help
show_help() {
    echo "Usage: $0 --yt_playlist_id [YT Playlist ID] --spotify_playlist_name [Spotify Playlist Name] [--interactive]"
    echo "Convert YT playlist to Spotify playlist."
    echo "  --yt_playlist_id: YT playlist ID to be converted to Spotify"
    echo "  --spotify_playlist_name: Name of Spotify playlist to create"
    echo "  --interactive: Enable interactive mode"
}

# Check required environment variables
if [ -z "$SPOTIPY_CLIENT_ID" ] || [ -z "$SPOTIPY_CLIENT_SECRET" ] || [ -z "$SPOTIPY_REDIRECT_URI" ]; then
    echo "Error: Environment Variables SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, and SPOTIPY_REDIRECT_URI must be set."
    exit 1
fi

# Default interactive mode to false
interactive_mode=false

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --yt_playlist_id) yt_playlist_id="$2"; shift ;;
        --spotify_playlist_name) spotify_playlist_name="$2"; shift ;;
        --interactive) interactive_mode=true ;;
        *) echo "Unknown parameter passed: $1"; show_help; exit 1 ;;
    esac
    shift
done

# Check required arguments
if [ -z "$yt_playlist_id" ] || [ -z "$spotify_playlist_name" ]; then
    echo "Error: Arguments --yt_playlist_id and --spotify_playlist_name are required."
    show_help
    exit 1
fi

# Main logic here
echo "YT Playlist ID: $yt_playlist_id"
echo "Spotify Playlist Name: $spotify_playlist_name"
echo "Interactive Mode: $interactive_mode"

if [ "$interactive_mode" = true ]; then
    echo "Interactive mode is enabled."
    python3 main.py --yt_playlist_id "$yt_playlist_id" --spotify_playlist_name "$spotify_playlist_name" --interactive
else
    echo "Interactive mode is disabled."
    python3 main.py --yt_playlist_id "$yt_playlist_id" --spotify_playlist_name "$spotify_playlist_name"
fi