#! /usr/local/bin/python3
import shutil
import time
from datetime import datetime
import os
import logging
import requests
import praw
from urllib3.exceptions import NewConnectionError
from required_info import *

logging.basicConfig(filename=LOG_FILE_NAME,
                    level=logging.INFO, format='%(asctime)s - %(message)s')
logging.getLogger('requests').setLevel(logging.DEBUG)

reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=SECRET,
                     user_agent='wallpaper downloader')


def good_pic(submission):
    """
    Returns True if the picture is larger than the minimum width and height
    and also if the width is larger than the height
    """
    if not 'preview' in vars(submission):
        return False
    MIN_WIDTH = 0
    MIN_HEIGHT = 0
    source = submission.preview['images'][0]['source']
    pic_width, pic_height = source['width'], source['height']
    return pic_width >= MIN_WIDTH and pic_height >= MIN_HEIGHT and pic_width > pic_height


def get_top_pics(sub):
    """
    Downloads the top pictures from the given subreddit
    """
    if sub[:2] == "r/":
        sub = sub[2:]
    top_day = reddit.subreddit(sub).top('day')
    pics_per_day = 2
    num_downloaded = 0
    for submission in top_day:
        if good_pic(submission):
            image_url = submission.preview['images'][0]['source']['url']
            download_image(sub, image_url)
            logging.info(f"Downloaded {submission.title}")
            num_downloaded += 1
        if num_downloaded >= pics_per_day:
            break


def download_image(subreddit, url):
    """
    Downloads an image from the given URL
    """
    resp = requests.get(url, stream=True)
    filename = DEST_DIR + subreddit + datetime.now().strftime("%Y%m%dT%H%M%S.%f") + ".jpg"
    with open(filename, 'wb+') as file:
        resp.raw.decode_content = True
        shutil.copyfileobj(resp.raw, file)


def cleanup(num_days, dest_dir):
    """
    Moves files in given directory to the Trash that are older than NUM_DAYS days
    """
    threshold = time.time() - (num_days * 24 * 60 * 60)
    for _, _, files in os.walk(dest_dir, topdown=False):  # os.walk returns root, directories, files
        for file in files:
            if file != ".DS_Store":  # To prevent cluttering trash with all     the .DS_    Store files
                full_path = os.path.join(dest_dir, file)
                file_age = os.stat(full_path).st_mtime

                if file_age < threshold:
                    try:
                        shutil.move(full_path, TRASH_PATH)
                        logging.info(f"Moved {file} to trash")
                    except Exception as e:
                        logging.info(f"Unable to delete {file}\n {e}")


if __name__ == "__main__":
    try:
        logging.info("Launched script")
        get_top_pics(SUBREDDIT)
        cleanup(CLEANUP_DAYS, DEST_DIR)
    except NewConnectionError:
        logging.info("Unable to establish connection - couldn't download image")
    except Exception as e:
        logging.info(e)

