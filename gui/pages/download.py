# Download page
__author__ = "Matteo Golin"

# Imports
import customtkinter as ctk
import re
from gui.common import GUIEntry, GUIErrorText, FONTS
from web import parse_video_name

# Constants
PADY = 12
OUATV_LINK_REGEX = "^(?:https:\\/\\/oua.yaretv.com\\/watch\\/)[a-zA-Z-0-9]{6,}"


# Page
def DownloadPage(master: ctk.CTk) -> ctk.CTkFrame:

    """Returns a frame containing the download page."""

    # Frame setup
    frame = ctk.CTkFrame(master=master)

    # Title
    ctk.CTkLabel(
        master=frame,
        text="OUATV Video Link",
        font=FONTS["h3"]
    ).pack(pady=40)

    # Credential entry fields
    video_link = GUIEntry(
        master=frame,
        placeholder_text="Video URL",
    )
    video_link.pack(pady=PADY)

    # Submission error message
    error_msg = GUIErrorText(
        master=frame,
        text="The video link entered is not a valid OUATV link."
    )

    # Submit logic
    def submit_cb():

        """Submits the OUATV link."""

        if re.match(OUATV_LINK_REGEX, video_link.get()):
            link = video_link.get()
            video_name = parse_video_name(link)
        else:
            error_msg.pack(pady=PADY)

    submit = ctk.CTkButton(
        master=frame,
        text="Submit",
        font=FONTS["h3"],
        command=submit_cb
    )
    submit.pack(pady=PADY)

    return frame
