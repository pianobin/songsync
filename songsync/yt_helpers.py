"""YouTube helper functions"""
import dataclasses
from ytmusicapi import YTMusic


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
