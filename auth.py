import time
import utils


def login_and_get_cookies(driver, gool_url, premium_mode):
    driver.get(gool_url)

    if premium_mode:
        print("Waiting for login... (Go to gool.co.il/mycourses)")
        while premium_mode:
            if "gool.co.il/mycourses" in driver.current_url.lower():
                break
            time.sleep(1)
        print("Logged in")

    time.sleep(2)
    print("Grabbing cookies...")
    cookies = utils.parse_cookies(driver.get_cookies())
    print("Cookies grabbed")

    return cookies
