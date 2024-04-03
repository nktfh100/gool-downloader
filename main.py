import requests
import xml.etree.ElementTree as ET
import os
import ffmpeg_downloader as ffdl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import argparse

parser = argparse.ArgumentParser(description="Gool Downloader CLI options")
parser.add_argument(
    "--free",
    action="store_true",
    help="Enable free mode, use this to download the free videos that do not require premium access.",
)

parser.add_argument(
    "--timeout",
    type=int,
    default=5,
    help="Time to wait between each video download, default is 5 seconds",
)

args = parser.parse_args()

premium_mode = not args.free
download_timeout = args.timeout

common_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.3",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Origin": "https://bagrut.gool.co.il",
    "Connection": "keep-alive",
}

video_view_type = "1"

if premium_mode:
    video_view_type = "2"


def get_video_token(cookies, tID, vID):
    data = {"tID": tID, "vID": vID, "videoViewType": video_view_type}
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Alt-Used": "bagrut.gool.co.il",
        "Host": "bagrut.gool.co.il",
    }

    response = requests.post(
        "https://bagrut.gool.co.il/api/Tokens/Add",
        headers={**headers, **common_headers},
        data=data,
        cookies=cookies,
    )

    if response.status_code != 200:
        print(f"get_video_token Error: {response.status_code}")
        raise Exception(f"get_video_token Error: {response.status_code}")

    return response.text


def generate_mpd_url(token, tID, vID):
    return f"https://5a153f939af4b.streamlock.net/bagrut/{vID}/manifest.mpd?tID={tID}&videoView={video_view_type}&accessToken={token}"


def download_mpd(url):
    headers = {
        "Accept-Encoding": "gzip, deflate, br",
        "Host": "5a153f939af4b.streamlock.net",
        "Referer": "https://bagrut.gool.co.il/",
    }

    response = requests.get(url, headers={**headers, **common_headers})

    if response.status_code != 200:
        print(f"download_mpd Error: {response.status_code}")
        raise Exception(f"download_mpd Error: {response.status_code}")

    with open("manifest.mpd", "w", encoding="utf-8") as f:
        f.write(response.text)


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


def download_video(name):
    command = f'streamlink "file://./manifest.mpd" best --ffmpeg-ffmpeg "{ffdl.ffmpeg_path}" -o "downloaded/{name}"'

    os.system(command)


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


def extract_course_ids(driver):
    # Run the extract-data.js script
    with open("extract-data.js", "r") as f:
        script = f.read()

    data = driver.execute_script(script)

    return data


def main():
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
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.3"
    )

    driver = webdriver.Chrome(options=options)

    driver.get("https://bagrut.gool.co.il/")

    if premium_mode:
        print("Waiting for login...")

        while premium_mode:
            if driver.current_url == "https://bagrut.gool.co.il/mycourses":
                break
            time.sleep(1)

        print("Logged in")

    time.sleep(2)
    print("Grabbing cookies...")

    cookies = parse_cookies(driver.get_cookies())
    print("Cookies grabbed")

    print("Please navigate to your desired course videos")
    print("Waiting for course videos page...")

    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".chapterPageNameDesktop"))
    )

    print("Course videos page loaded")
    print("Extracting video and topic ids...")

    ids = extract_course_ids(driver)

    print("Video and topic ids extracted")

    print("Starting download...")
    time.sleep(3)
    driver.quit()

    for course in ids:
        for video in course["data"]:
            print(f"Downloading: {video['title']}")

            token = get_video_token(cookies, course["topicId"], video["videoId"])

            url = generate_mpd_url(token, course["topicId"], video["videoId"])

            download_mpd(url)

            file_name = f'{course["title"]}/{video["title"]}.mp4'

            mpd_file_name = parse_mpd_file_title("manifest.mpd")

            if mpd_file_name is not False:
                file_name = mpd_file_name

            download_video(file_name)

            os.remove("manifest.mpd")

            time.sleep(download_timeout)

    print("Download completed!")


if __name__ == "__main__":
    if not ffdl.installed():
        print("ffmpeg is not installed!")
        print("Use this command to install: 'ffdl install'")
        exit(1)

    main()
