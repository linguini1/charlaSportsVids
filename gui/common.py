# Common items between GUI elements
__author__ = "Matteo Golin"

# Imports
import customtkinter as ctk

# Constants
FONT_FAMILY = "Montserrat"
FONTS = {
    "title": (FONT_FAMILY, 32),
    "h1": (FONT_FAMILY, 24),
    "h2": (FONT_FAMILY, 16),
    "h3": (FONT_FAMILY, 14),
    "text": (FONT_FAMILY, 12)
}


# Elements
class GUIEntry(ctk.CTkEntry):

    def __init__(self, master, placeholder_text: str):
        self.master = master
        self.placeholder = placeholder_text
        super().__init__(
            master=master,
            placeholder_text=placeholder_text,
            font=FONTS["h3"],
            width=300
        )


class GUIErrorText(ctk.CTkLabel):

    def __init__(self, master, text: str):
        super().__init__(
            master=master,
            text=text.upper(),
            text_color="red",
            width=300,
            font=FONTS["text"]
        )
