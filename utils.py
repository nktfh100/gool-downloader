from selenium import webdriver
import os
import xml.etree.ElementTree as ET


def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    )
    options.add_argument(
        f"user-data-dir=C:\\Users\\{os.getlogin()}\\AppData\\Local\\Google\\Chrome\\User Data"
    )

    return webdriver.Chrome(options=options)


cookies_to_grab = [
    "ASP.NET_SessionId",
    "FedAuth1",
    "FedAuth",
    "__RequestVerificationToken",
    ".ASPXAUTH",
]


def parse_cookies(driver_cookies):
    final_cookies = {
        "testimonialsPagerFirstItem": "true",
    }

    for cookie in driver_cookies:
        if cookie["name"] in cookies_to_grab:
            final_cookies[cookie["name"]] = cookie["value"]

    return final_cookies


encodings_to_try = ["cp1250", "cp1125", "cp1255", "cp1251"]


def parse_mpd_file_title(file_name):
    tree = ET.parse(file_name)

    root = tree.getroot()

    title_element = root.find(".//{urn:mpeg:dash:schema:mpd:2011}Title")

    title = title_element.text

    # Not sure why sometimes titles are encoded differently
    for encoding in encodings_to_try:
        try:
            title = title.encode(encoding).decode("iso8859_8")
            return title
        except Exception:
            pass

    # Check if the title is actually in hebrew or gibberish (couldn't find a better way to do this)
    if any(1488 <= ord(char) <= 1514 for char in title):
        return title

    print("Failed to parse title from mpd file")

    return False


def get_common_headers(gool_url):
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.3",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Origin": gool_url,
        "Connection": "keep-alive",
    }


def make_safe_filename(s):
    def safe_char(c):
        if c.isalnum():
            return c
        else:
            return "_"

    return "".join(safe_char(c) for c in s).rstrip("_")
