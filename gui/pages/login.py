# Contains the login page element
__author__ = "Matteo Golin"

# Imports
import customtkinter as ctk
import re
from gui.common import FONTS, GUIEntry, GUIErrorText

# Constants
EMAIL_REGEX = "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\\.[a-zA-Z0-9-]+)*$"
PADY = 12


# Class
def LoginPage(credentials: dict[str, str], master: ctk.CTk) -> ctk.CTkFrame:

    """Returns a frame containing the login page."""

    # Login frame
    frame = ctk.CTkFrame(master=master)

    # Title
    ctk.CTkLabel(
        master=frame,
        text="OUATV Credentials",
        font=FONTS["title"]
    ).pack(pady=40)

    # Credential entry fields
    email = GUIEntry(master=frame, placeholder_text="Email")
    email.pack(pady=PADY)

    password = GUIEntry(master=frame, placeholder_text="Password")
    password.pack(pady=PADY)

    # Submission error message
    error_msg = GUIErrorText(master=frame, text="Please enter a valid email and password.")

    # Submit logic
    def submit_cb():

        """Saves the user entered email and password to a string."""

        # Check password/email not empty
        if email.get() == "" or password.get() == "":
            error_msg.pack(pady=PADY)

        # Check valid email
        elif not re.match(EMAIL_REGEX, email.get()):
            error_msg.pack(pady=PADY)

        # Save credentials
        else:
            credentials["email"] = email.get()
            credentials["password"] = password.get()

    submit = ctk.CTkButton(
        master=frame,
        text="Submit",
        font=FONTS["h3"],
        command=submit_cb
    )
    submit.pack(pady=PADY)

    return frame
