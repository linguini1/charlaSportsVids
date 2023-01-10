# GUI creation for the downloader
__author__ = "Matteo Golin"

# Imports
import customtkinter as ctk
import queue as q
import threading

from conversion import TSVideo
from web import get_m3u8_link
from gui.pages.login import LoginPage
from gui.pages.download import DownloadPage

# Constants
TITLE = "OUATV Video Downloader"
ICON_PATH = "./assets/charlogo.ico"
GEOMETRY = "500x500"
APPEARANCE_MODE = "dark"
THEME = "green"
UPDATE_TIME = 100


# GUI class
class GUI:

    """Contains the GUI for downloading sports videos from OUATV."""

    def __init__(self, credentials: dict[str, str], output_dir: str):

        # Variables
        self.credentials = credentials
        self.output_dir = output_dir
        self.queue = q.Queue()

        # Create root
        self.root = ctk.CTk()
        self.root.geometry(GEOMETRY)
        self.root.title(TITLE)
        self.root.iconbitmap(ICON_PATH)

        # Theme
        ctk.set_appearance_mode(APPEARANCE_MODE)
        ctk.set_default_color_theme(THEME)

        # Set up pages
        self.login_page = LoginPage(self.credentials, master=self.root)
        self.download_page = DownloadPage(master=self.root)

    def __queue_listener(self):

        """Checks for queue updates."""

        try:
            result = self.queue.get()
            print(result)
        except q.Empty:
            pass

        self.root.after(UPDATE_TIME, self.__queue_listener)  # Continue listening

    def run(self) -> None:

        """Runs the GUI main loop."""

        # Begin listening
        self.__queue_listener()

        self.login_page.pack(fill="both", expand=True)
        self.root.mainloop()
