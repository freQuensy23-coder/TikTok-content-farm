from pytube import YouTube
import requests as req
from tqdm import tqdm
from config import *
from pprint import pprint
from pyyoutube import Api
import logging
import video_divider

log = logging.getLogger("broadcast")


def get_videos(channel_id: str)->list:
    """
    :param channel_id - youtube channel id
    Get all videos of some chanel with id =  channel_id
    """
    r = req.get(
        f"https://www.googleapis.com/youtube/v3/search?key={youtube_api_key}&channel_id={channel_id}&orderby=published&part=snippet,id&order=date&maxResults=50")
    return r.json()["items"]


def get_channel_id(channel_name: str) -> tuple:
    """:param channel_name - name of channel. You can find them in link,  ex www.youtube.com/user/Google
        :returns Returns tuple. First is bool - True if we found only one channel with such name.
    """
    channel_ids = api.get_channel_info(channel_name=channel_name)
    if len(channel_ids) == 0:
        raise Exception("No channel with such name")
    if len(channel_ids) == 1:
        return True, channel_ids[0]
    else:
        return False, channel_ids


def download_channel_videos(channel_id, folder):
    videos = get_videos(channel_id)
    log.info(f"Get {len(videos)} videos")
    log.info("Start downloading ....")

    for video in tqdm(videos):
        if video["id"]["kind"] == "youtube#video":
            log.debug(f'Downloading video {video["id"]["videoId"]}')
            link = "https://www.youtube.com/watch?v=" + video["id"]["videoId"]
            yt = YouTube(link)
            yt.streams\
            .filter(progressive=True, file_extension='mp4')\
            .order_by('resolution')\
            .desc()\
            .first()\
            .download(folder)
            log.debug(f'Downloaded video {video["id"]["videoId"]}')
        else:
            log.debug(f"{video} is not youtube#video")

    divide_videos = input("Do you want to divide downloaded videos into small parts (It is necessary if you want to "
                          "download them to TikTok)? (Y/N)")
    if divide_videos == "Y":
        video_divider.divide_videos(folder_name=folder)

    return True


if __name__ == '__main__':
    api = Api(api_key=youtube_api_key)
    log.debug("API inited")
    do = True
    while do:
        print("(0) Get last videos of some channel (by it's id)")
        print("(1) Get channel id by it's name")
        print("(2) Get last videos by some search query")
        action = input("What do you want to do \n")

        if action == "0":
            channel_id = input("Print channel id ")
            folder = input("Print folder_name ")
            download_channel_videos(channel_id, folder)
            log.info("Videos is downloaded")

        if action == "1":
            channel_name = input("Print channel name ")
            channel_id = get_channel_id(channel_name)
            log.info(f"Find {channel_name} id. It is {channel_id}.")
            download = input("Do you want to download it's last videos? (Y/N)")
            if download == "Y":
                folder = input("Print folder_name ")
                download_channel_videos(channel_id, folder)
                log.info("Videos is downloaded")

        if action == "2":
            print("Not supported")
            query = input("Print ")
            # TODO

        elif action == "c" or action == "q":
            do = False



