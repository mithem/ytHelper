import os
import json
from pathlib import Path

DESCRIPTION: str = "An easy-to-use wrapper for youtube-dl to make downloading YouTube-Videos even easier"
VERSION: str = "0.0.0"


def is_video(filename):
    return (filename[-5:] == ".webm" or filename[-4:] == ".mkv" or filename[-4:] == ".mp4" or filename[-4:] == ".avi" or filename[-4:] == ".mov" or filename[-4:] == ".flv" or filename[-4:] == ".ogv" or filename[-4:] == ".ogg" or filename[-4:] == ".gif" or filename[-4:] == ".m4p" or filename[-4:] == ".m4v")


def getQuery():
    """returns a list of urls as in config.json"""
    with open("config.json", "r") as f:
        return json.loads(f.read()).get("urls", {}).get("public", [])


def getFilesFromPath(path):
    """returns all files corresponding to path parameter"""
    raw = os.listdir(Path(path))
    files_to_return = list()
    for i in raw:
        if i != ".DS_Store":
            files_to_return.append(i)
    return files_to_return


def getVideos():
    """returns all files in videos/ directory"""
    return getFilesFromPath("videos/")


def getWAVs():
    """returns all files in music/wav/ directory"""
    return getFilesFromPath("music/wav/")


def getMP3s():
    """returns all files in music/mp3/ directory"""
    return getFilesFromPath("music/mp3/")


def getThumbnails():
    """returns all files in thumbnails/ directory"""
    return getFilesFromPath("thumbnails/")


def removeExtension(file):
    """returns filename without extension"""
    if not file[-4:] == "webm":
        return file[:-4]
    else:
        return file[:-5]


def repoPath():
    """returns path to local repo"""
    # returns path of local repo
    f = open("setup.config", "r")
    resp = f.readlines()[0]
    f.close()
    return resp[:-2]


def videosPath():
    """returns path to local videos/Movies directory"""
    # returns path for storing videos
    f = open("setup.config", "r")
    resp = f.readlines()[1]
    f.close()
    return resp[:-2]


def musicPath():
    """returns path to local music directory"""
    # returns path for storing music
    f = open("setup.config", "r")
    resp = f.readlines()[2]
    f.close()
    return resp


def setUpDirs():
    """creates (if not existing) all important directories"""
    if not os.path.isdir("videos"):
        os.mkdir("videos")

    if not os.path.isdir("thumbnails"):
        os.mkdir("thumbnails")

    if not os.path.isdir("music"):
        os.mkdir("music")

    if not os.path.isdir("music/wav"):
        os.mkdir(Path("music/wav"))

    if not os.path.isdir("music/mp3"):
        os.mkdir(Path("music/mp3"))

    if not os.path.isdir("faces"):
        os.mkdir(Path("faces"))

    if not os.path.isdir("temp"):
        os.mkdir(Path("temp"))


def setUpConfig():  # TODO: Make a json out of it
    """gets config data from user and saves it"""
    f = open("setup.config", "w+")

    f.writelines(input(
        "Please enter your path of the repo[e.g. '/home/name/repos/ytHelper/]> ") + "\n")
    f.writelines(
        input("Please enter your path from home to videos [e.g. 'Videos/]> ") + "\n")
    f.writelines(
        input("Please enter your path from home to music [e.g. Music/]> "))

    f.close()


def resetAllFolders():
    """deletes all files in folders like videos, music, thumbnails (not used in project source code, but can be useful from terminal)"""
    for directory in ["videos", "music/mp3", "music/wav", "thumbnails"]:
        for i in os.listdir(directory):
            os.remove(directory + "/" + str(i))
    for i in os.listdir():
        if i[-5:] == ".part" or is_video(i):
            os.remove(i)


def convertFiles(bitrate, silent=False):
    """converts all pending video files in wav and mp3 format"""
    videos = getVideos()
    for i in videos:
        if not os.path.exists(Path("music/wav/" + removeExtension(i) + ".wav")):
            ffCommand = "ffmpeg "
            if silent:
                ffCommand += "-loglevel quiet"
            ffCommand += " -i 'videos/" + i + \
                "' 'music/wav/" + removeExtension(i) + ".wav'"
            os.system(ffCommand)
        elif not silent:
            print(col.OKBLUE + "already converted to wav: " + col.ENDC + i)

    for i in videos:
        if not os.path.exists(Path("music/mp3/" + removeExtension(i) + ".mp3")):
            os.system("lame -b " + str(bitrate) + " 'music/wav/" +
                      removeExtension(i) + ".wav' 'music/mp3/" + removeExtension(i) + ".mp3'")
        elif not silent:
            print(col.OKBLUE + "already converted to mp3: " + col.ENDC + i)


def extractThumbnails(silent=False):
    """filenameracts thumbnails from videos and saves it in thumbnails/"""
    videos = getVideos()
    for i in videos:
        ffCommand = "ffmpeg "
        if silent:
            ffCommand += "-loglevel quiet "
        ffCommand += f" -y -i videos/'{i}' -ss 00:00:03.000 -vframes 1 'thumbnails/{removeExtension(i)}.png'"
        os.system(ffCommand)


def writeThumbnails():
    """uses the thumbnails in thumbnails/ to write the front cover of corresponding mp3 files"""
    thumbs = getThumbnails()
    for i in thumbs:
        os.system(
            f"eyeD3 --add-image 'thumbnails/{i}:FRONT_COVER' 'music/mp3/{removeExtension(i)}.mp3'")


def log_header(log, description, verbose):
    log.header(True, True, description,
               6 if verbose else 0, verbose)


def get_filename(path):
    return path.split("/")[-1]


def get_extension(fname_or_path):
    n = get_filename(fname_or_path)
    if n[-3:] == ".js":
        return "js"
    if n[-5:] == ".html":
        return "html"
    if n[-4:] == ".css":
        return "css"
    if n[-4:] == ".mp4":
        return "mp4"
    if n[-4:] == ".mov":
        return "mov"
    return ""


def get_filetype(fname_or_path):
    n = get_extension(fname_or_path)
    if n == "js" or n == "html" or n == "css":
        return "text"
    if n == "mp4" or n == "mov":
        return "video"


class col:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
