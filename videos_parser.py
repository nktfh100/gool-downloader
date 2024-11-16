def extract_course_ids(driver):
    with open("extract-data.js", "r") as f:
        script = f.read()
    return driver.execute_script(script)
