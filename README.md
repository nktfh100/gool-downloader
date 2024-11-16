# Gool Downloader

A simple python script that downloads videos for offline use from https://gool.co.il/ (Works for gool bagrut and gool academy).

## Installation


Install python 3 then install the required packages and ffmpeg:
```bash
pip install -r requirements.txt
ffdl install
```
## CLI Options

- `--free`: Enable free mode, use this to download the free videos that do not require premium access.
- `--timeout`: Time to wait between each video download, if no option specified it will use a random time between 60 and 120 seconds.
- `--academy`: Download from gool academy instead of gool bagrut.

## Usage

```bash
python main.py [-h] [--free] [--academy] [--timeout TIMEOUT]
```

How to use the script:

1. Make sure chrome is closed, since the script uses the default chrome profile. (So you won't have to login again and to not exeed the device limit).
2. Run the script with the desired options.
3. A web browser will open, if you are not logged in, login to your account.
4. Navigate to https://(bagrut or www).gool.co.il/mycourses
5. Navigate to the topic you want to download ([Example](https://bagrut.gool.co.il/%D7%91%D7%92%D7%A8%D7%95%D7%AA-%D7%91%D7%A4%D7%99%D7%96%D7%99%D7%A7%D7%94-5-%D7%99%D7%97%D7%99%D7%93%D7%95%D7%AA-%D7%9C%D7%AA%D7%9C%D7%9E%D7%99%D7%93%D7%99-%D7%AA%D7%99%D7%9B%D7%95%D7%9F/%D7%A7%D7%95%D7%A8%D7%A1-%D7%94%D7%9B%D7%A0%D7%94-%D7%9E%D7%9C%D7%90-%D7%9C%D7%91%D7%92%D7%A8%D7%95%D7%AA-%D7%91%D7%A4%D7%99%D7%96%D7%99%D7%A7%D7%94-5-%D7%99%D7%97%D7%99%D7%93%D7%95%D7%AA-/%D7%94%D7%A7%D7%93%D7%9E%D7%94-%D7%9E%D7%AA%D7%9E%D7%98%D7%99%D7%AA-%D7%9C%D7%A7%D7%95%D7%A8%D7%A1#31762))
6. The script will start downloading the videos.
