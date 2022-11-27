# Downloads sports videos off of OUA TV
__author__ = "Matteo Golin"

# Imports
from M3U8Converter import TSVideo
from web import get_m3u8_link, parse_video_name
import moviepy.editor as mp

# Constants
OUTPUT_DIR = "./output"


# Main
def main():

    # Ask for URL
    video_url = input("Video URL: ")

    # Get M3U8
    m3u8_url = get_m3u8_link(video_url)

    # Save as video.ts
    video = TSVideo(m3u8_url)
    video_name = parse_video_name(video_url)
    file_path = f"{OUTPUT_DIR}/{video_name}"
    video.save(file_path)

    # Change to mp4
    clip = mp.VideoFileClip(f"{file_path}.ts")
    clip.write_videofile(f"{file_path}.mp4")


if __name__ == '__main__':
    main()