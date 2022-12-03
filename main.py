# Downloads sports videos off of OUA TV
__author__ = "Matteo Golin"

# Imports
from conversion import TSVideo
from web import get_m3u8_link, parse_video_name
import moviepy.editor as mp
from gui import GUI

# Constants
OUTPUT_DIR = "./output"
CREDENTIALS = {
    "email": "",
    "password": ""
}


# Main
def main():

    # Create GUI
    gui = GUI(
        credentials=CREDENTIALS,
        output_dir=OUTPUT_DIR
    )
    gui.run()


if __name__ == '__main__':
    main()
