# Conversion utilities for downloaded videos
__author__ = "Matteo Golin"

# Imports
import requests
import m3u8
from progress.bar import ChargingBar

# Constants


# TS Video converter class
class TSVideo:

    def __init__(self, url: str):
        self.url = url
        self.base_url = self.url[0:self.url.find(".smil/") + 6]

    def __get_video_segments(self) -> list[dict]:

        """Returns a list of all the segments that make up the M3U8 video."""

        # Find the playlist url
        raw = requests.get(self.url).text
        m3u8_playlist = m3u8.loads(raw)
        playlist_uri = m3u8_playlist.data["playlists"][0]["uri"]

        # Locate the video from the playlist url
        video_url = self.base_url + playlist_uri
        raw_video = requests.get(video_url).text
        m3u8_video = m3u8.loads(raw_video)

        # Get all the segments that make up the video
        video_segments = m3u8_video.data["segments"]

        return video_segments

    def save(self, filename: str) -> None:

        # Fetch segments
        print("Getting segments...")
        segments = self.__get_video_segments()

        # Create progress bar
        progress_bar = ChargingBar("Saving", max=len(segments))

        # Iterate through segments and add to .ts video file
        with open(f"{filename}.ts", "wb") as file:
            for segment in segments:
                uri = segment["uri"]
                segment_raw = requests.get(self.base_url + uri)
                file.write(segment_raw.content)
                progress_bar.next()

        progress_bar.finish()  # Completed