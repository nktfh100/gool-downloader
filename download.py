import os
import random
import time
import requests
import utils
import ffmpeg_downloader as ffdl


def download_video(course_title, video_name):
    command = f'streamlink "file://./manifest.mpd" best --ffmpeg-ffmpeg "{ffdl.ffmpeg_path}" -o "downloaded/{course_title}/{video_name}.mp4"'

    os.system(command)


def get_video_token(cookies, tID, vID, video_view_type, gool_url):
    data = {"tID": tID, "vID": vID, "videoViewType": video_view_type}

    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Alt-Used": gool_url.replace("https://", ""),
        "Host": gool_url.replace("https://", ""),
    }

    response = requests.post(
        gool_url + "/api/Tokens/Add",
        headers=headers,
        data=data,
        cookies=cookies,
    )

    if response.status_code != 200:
        print(f"get_video_token Error: {response.status_code}")
        raise Exception(f"get_video_token Error: {response.status_code}")

    return response.text


def generate_mpd_url(token, tID, vID, academy_mode, video_view_type):
    base_url = "https://5a153f939af4b.streamlock.net"
    path = f"{'academy' if academy_mode else 'bagrut'}/{vID}/manifest.mpd"
    return (
        f"{base_url}/{path}?tID={tID}&videoView={video_view_type}&accessToken={token}"
    )


def download_mpd(url, gool_url):
    headers = {
        "Accept-Encoding": "gzip, deflate, br",
        "Host": "5a153f939af4b.streamlock.net",
        "Referer": gool_url,
    }

    response = requests.get(
        url, headers={**headers, **utils.get_common_headers(gool_url)}
    )
    if response.status_code != 200:
        print(f"download_mpd Error: {response.status_code}")
        raise Exception(f"download_mpd Error: {response.status_code}")

    with open("manifest.mpd", "w", encoding="utf-8") as f:
        f.write(response.text)


def download_course_videos(
    gool_url, video_view_type, course_ids, cookies, academy_mode, download_timeout
):
    total_courses_count = len(course_ids)
    total_videos_count = sum(len(course["data"]) for course in course_ids)
    videos_downloaded = 0
    courses_downloaded = 0

    for course in course_ids:
        course_title = utils.make_safe_filename(course["title"])
        topic_id = course["topicId"]
        print(
            f"Downloading course: {course_title} {
                courses_downloaded}/{total_courses_count}"
        )
        courses_downloaded += 1
        for video in course["data"]:
            video_title = video["title"]
            video_id = video["videoId"]

            print(
                f"Downloading: {video['title']} {
                    videos_downloaded}/{total_videos_count}"
            )
            videos_downloaded += 1
            file_name = utils.make_safe_filename(video_title)

            if os.path.exists(f"downloaded/{course_title}/{file_name}.mp4"):
                print(f"Skipping: {file_name} - already downloaded")
                time.sleep(1)
                continue

            token = get_video_token(
                cookies, topic_id, video_id, video_view_type, gool_url
            )
            url = generate_mpd_url(
                token,
                topic_id,
                video_id,
                academy_mode,
                video_view_type,
            )

            download_mpd(url, gool_url)

            if not video_title:
                mpd_file_name = utils.parse_mpd_file_title("manifest.mpd")

                if mpd_file_name is not False:
                    file_name = utils.make_safe_filename(mpd_file_name)
                else:
                    file_name = utils.make_safe_filename(video_id)

            if os.path.exists(f"downloaded/{course_title}/{file_name}"):
                print(f"Skipping: {file_name} - already downloaded")
                continue

            download_video(course_title, file_name)
            os.remove("manifest.mpd")

            timeout = (
                random.randint(60, 120) if download_timeout == -1 else download_timeout
            )

            print("Sleeping for", timeout, "seconds")
            time.sleep(timeout)
