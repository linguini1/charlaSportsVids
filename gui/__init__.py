# GUI creation for the downloader
__author__ = "Matteo Golin"

# Imports
import customtkinter as ctk
import re
import threading
from conversion import TSVideo
from web import get_m3u8_link, parse_video_name

# Constants
TITLE = "OUATV Video Downloader"
ICON_PATH = "./assets/charlogo.ico"
GEOMETRY = "500x500"
APPEARANCE_MODE = "dark"
THEME = "green"
FONT_FAMILY = "Montserrat"
FONTS = {
    "title": (FONT_FAMILY, 32),
    "h1": (FONT_FAMILY, 24),
    "h2": (FONT_FAMILY, 16),
    "h3": (FONT_FAMILY, 14),
    "text": (FONT_FAMILY, 12)
}
EMAIL_REGEX = "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\\.[a-zA-Z0-9-]+)*$"
OUATV_LINK_REGEX = "^(?:https:\\/\\/oua.yaretv.com\\/watch\\/)[a-zA-Z-0-9]{6,}"


# GUI class
class GUI:

    """Runs the Tkinter GUI."""

    def __init__(self, credentials: dict[str, str], output_dir: str):

        # Variables
        self.credentials = credentials
        self.output_dir = output_dir
        self.video_link: str = ""

        # Create root
        self.root = ctk.CTk()
        self.root.geometry(GEOMETRY)
        self.root.title(TITLE)
        self.root.iconbitmap(ICON_PATH)

        # Theme
        ctk.set_appearance_mode(APPEARANCE_MODE)
        ctk.set_default_color_theme(THEME)

        # Set up pages
        self.login_page = self.__create_login_page()
        self.download_page = self.__create_download_page()

    def __create_login_page(self) -> ctk.CTkFrame:

        """Returns the frame that contains the login page."""

        # Login frame
        frame = ctk.CTkFrame(master=self.root)

        # Title
        ctk.CTkLabel(
            master=frame,
            text="OUATV Credentials",
            text_font=FONTS["title"]
        ).pack(pady=40)

        # Credential entry fields
        email = ctk.CTkEntry(
            master=frame,
            placeholder_text="Email",
            text_font=FONTS["h3"],
            width=300
        )
        email.pack(pady=12)

        password = ctk.CTkEntry(
            master=frame,
            placeholder_text="Password",
            text_font=FONTS["h3"],
            width=300
        )
        password.pack(pady=12)

        # Submission error message
        error_msg = ctk.CTkLabel(
            master=frame,
            text_font=FONTS['text'],
            width=300,
            text="Please enter a valid email and password.".upper(),
            text_color="red"
        )

        # Submit logic
        def submit_cb():

            """Saves the user entered email and password to a string."""

            # Check password/email not empty
            if email.get() == "" or password.get() == "":
                error_msg.pack(pady=12)

            # Check valid email
            elif not re.match(EMAIL_REGEX, email.get()):
                error_msg.pack(pady=12)

            # Save credentials
            else:
                self.credentials["email"] = email.get()
                self.credentials["password"] = password.get()
                self.download_page.pack(fill="both", expand=True)
                self.login_page.pack_forget()

        submit = ctk.CTkButton(
            master=frame,
            text="Submit",
            text_font=FONTS["h3"],
            command=submit_cb
        )
        submit.pack(pady=12)

        return frame

    def __create_download_page(self) -> ctk.CTkFrame:

        """Returns the frame containing the video download page."""

        # Frame setup
        frame = ctk.CTkFrame(master=self.root)

        # Title
        ctk.CTkLabel(
            master=frame,
            text="OUATV Video Link",
            text_font=FONTS["title"]
        ).pack(pady=40)

        # Credential entry fields
        video_link = ctk.CTkEntry(
            master=frame,
            placeholder_text="Video URL",
            text_font=FONTS["h3"],
            width=300
        )
        video_link.pack(pady=12)

        # Submission error message
        error_msg = ctk.CTkLabel(
            master=frame,
            text_font=FONTS['text'],
            width=300,
            text="The video link entered is not a valid OUATV link".upper(),
            text_color="red"
        )

        # Submit logic
        def submit_cb():

            """Submits the OUATV link."""

            if re.match(OUATV_LINK_REGEX, video_link.get()):
                self.video_link = video_link.get()
                self.download_page.pack_forget()
                self.progress_page = self.__create_progress_page()
            else:
                error_msg.pack(pady=12)

        submit = ctk.CTkButton(
            master=frame,
            text="Submit",
            text_font=FONTS["h3"],
            command=submit_cb
        )
        submit.pack(pady=12)

        return frame

    def __create_progress_page(self):

        """Creates the page to display the progress of the video download."""

        frame = ctk.CTkFrame()
        video_name = parse_video_name(self.video_link)

        # Title
        ctk.CTkLabel(
            master=frame,
            text=f"Downloading {video_name}",
            text_font=FONTS["title"]
        ).pack(pady=40)

        # Progress messages
        getting_m3u8 = ctk.CTkLabel(
            master=frame,
            text_font=FONTS['text'],
            width=300,
            text="Getting M3U8 data from the webpage...",
        )

        downloading_video = ctk.CTkLabel(
            master=frame,
            text_font=FONTS['text'],
            width=300,
            text="Downloading video...",
        )

        complete = ctk.CTkLabel(
            master=frame,
            text_font=FONTS['text'],
            width=300,
            text="Complete!",
        )

        finish_button = ctk.CTkButton(
            master=frame,
            text="Finish",
            text_font=FONTS["h3"],
            command=self.root.destroy
        )

        frame.pack(fill="both", expand=True)  # Show frame

        def download_logic():

            # Get M3U8
            getting_m3u8.pack(pady=12)
            m3u8_link = get_m3u8_link(self.video_link, self.credentials)

            # Download video from M3U8
            downloading_video.pack(pady=12)
            video = TSVideo(m3u8_link)
            video.save(f"{self.output_dir}/{video_name}")

            complete.pack(pady=12)  # Display completion
            finish_button.pack(pady=12)  # Allow user to finish

        threading.Thread(download_logic())

    def run(self) -> None:

        """Runs the GUI main loop."""

        self.login_page.pack(fill="both", expand=True)
        self.root.mainloop()
