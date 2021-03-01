import subprocess
from tqdm import tqdm
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os
import time
import moviepy.editor


def get_length(path):
    video = moviepy.editor.VideoFileClip(path)
    return video.duration


def get_result_folder_name(folder: str, filename: str, i:int)->str:
    """
    :param folder: absolute path to folder with videos
    :param i: index of file in video
    :param filename: filename of input file
    :return: String - absolute path to folder to save results
    """
    return folder + "_cropped\\" + filename + f"({str(i)})" + ".mp4"


def divide_videos(folder_name, result_len: int = 40):
    """
    :param folder_name: Relative path to folder with videos
    :param result_len: Duraction of extracted subclips in seconds. Default = 40
    :return:
    """

    list_of_filenames = os.listdir(path=folder_name)

    for filename in tqdm(list_of_filenames):
        video_path = os.path.abspath(f"{folder_name}/{filename}")
        video_length = int(get_length(video_path))
        os.mkdir(os.path.abspath(folder_name) + "_cropped")
        for second in tqdm(range(8, video_length - 8, result_len)):
            ffmpeg_extract_subclip(video_path,
                                   second, second + result_len,
                                   targetname=get_result_folder_name(os.path.abspath(folder_name), filename, second))