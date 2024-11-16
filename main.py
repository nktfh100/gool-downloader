import ffmpeg_downloader as ffdl
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import argparse
import utils
import auth
import videos_parser
import download


def parse_arguments():
    parser = argparse.ArgumentParser(description="Gool Downloader CLI options")
    parser.add_argument(
        "--free",
        action="store_true",
        help="Enable free mode, use this to download the free videos that do not require premium access.",
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=-1,
        help="Time to wait between each video download, if not specified will be random between 60-120 seconds",
    )

    parser.add_argument(
        "--academy",
        action="store_true",
        help="Download from gool academy (www.gool.co.il) instead of gool bagrut (bagrut.gool.co.il)",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    premium_mode = not args.free
    download_timeout = args.timeout
    academy_mode = args.academy

    if not ffdl.installed():
        print("ffmpeg is not installed!")
        print("Use this command to install: 'ffdl install'")
        exit(1)

    gool_url = f"https://{'www' if academy_mode else 'bagrut'}.gool.co.il"
    video_view_type = "1"

    if premium_mode:
        video_view_type = "2"

    driver = utils.init_driver()

    cookies = auth.login_and_get_cookies(driver, gool_url, premium_mode)

    print("Please navigate to your desired course videos")
    print("Waiting for course videos page...")

    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                "#chapter-videos" if academy_mode else ".chapterPageNameDesktop",
            )
        )
    )

    time.sleep(2)

    print("Course videos page loaded")
    print("Extracting video and topic ids...")

    course_ids = videos_parser.extract_course_ids(driver)

    print("Video and topic ids extracted")

    print("Starting download...")
    time.sleep(3)
    driver.quit()

    download.download_course_videos(
        gool_url, video_view_type, course_ids, cookies, academy_mode, download_timeout
    )
    print("Download completed!")


if __name__ == "__main__":
    if not ffdl.installed():
        print("ffmpeg is not installed!")
        print("Use this command to install: 'ffdl install'")
        exit(1)

    main()
