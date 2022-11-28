# Handles interfacing with OUA website to parse for video download links
__author__ = "Matteo Golin"

# Imports
import requests
from bs4 import BeautifulSoup

# Constants
LOGIN_URL: str = "https://oua.yaretv.com/login"


# Helper functions
def get_csrf(page_html: str) -> str:

    """Returns the CSRF token needed to validate the login."""

    soup = BeautifulSoup(page_html, 'html5lib')
    csrf = soup.select_one('input[name="_token"]')

    return csrf["value"]


def parse_video_link(video_player: str) -> str:

    """Returns the M3U8 video link from the video player script tag."""

    start = video_player.find('file: "')
    end = video_player.find('image:')
    return video_player[start:end].split('"')[1]


def get_m3u8_link(video_url: str, credentials: dict[str, str]) -> str:

    """Returns the link to the M3U8 playlist of the video's page URL."""

    with requests.Session() as session:

        # Login
        login_page = session.get(LOGIN_URL)
        csrf = get_csrf(login_page.text)  # Get CSRF token
        credentials["_token"] = csrf  # Add token to credentials
        session.post(LOGIN_URL, data=credentials)

        # Parse video page
        html = session.get(video_url)
        soup = BeautifulSoup(html.text, 'html5lib')
        video_player = soup.select('script[type="text/javascript"]')[2].string

        return parse_video_link(video_player)


def parse_video_name(video_url: str) -> str:

    """Returns the video name from the video URL."""

    return video_url.split("/")[-1]
