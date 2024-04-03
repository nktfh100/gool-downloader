# Gool Downloader

A simple python script that downloads videos for offline use from https://bagrut.gool.co.il/

## Installation


Install python 3 then install the required packages and ffmpeg:
```bash
pip install -r requirements.txt
ffdl install
```
## CLI Options

- `--free`: Enable free mode, use this to download the free videos that do not require premium access.
- `--timeout`: Time to wait between each video download, default is 5 seconds.

## Usage

```bash
python main.py [-h] [--free] [--timeout TIMEOUT]
```

How to use the script:

1. Run the script with the desired options.
2. A web browser will open, login to your account.
3. Navigate to the topic you want to download ([Example](https://bagrut.gool.co.il/%D7%91%D7%92%D7%A8%D7%95%D7%AA-%D7%91%D7%A4%D7%99%D7%96%D7%99%D7%A7%D7%94-5-%D7%99%D7%97%D7%99%D7%93%D7%95%D7%AA-%D7%9C%D7%AA%D7%9C%D7%9E%D7%99%D7%93%D7%99-%D7%AA%D7%99%D7%9B%D7%95%D7%9F/%D7%A7%D7%95%D7%A8%D7%A1-%D7%94%D7%9B%D7%A0%D7%94-%D7%9E%D7%9C%D7%90-%D7%9C%D7%91%D7%92%D7%A8%D7%95%D7%AA-%D7%91%D7%A4%D7%99%D7%96%D7%99%D7%A7%D7%94-5-%D7%99%D7%97%D7%99%D7%93%D7%95%D7%AA-/%D7%94%D7%A7%D7%93%D7%9E%D7%94-%D7%9E%D7%AA%D7%9E%D7%98%D7%99%D7%AA-%D7%9C%D7%A7%D7%95%D7%A8%D7%A1#31762))
4. The script will start downloading the videos.
