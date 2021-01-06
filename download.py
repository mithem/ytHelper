import argparse
import concurrent.futures
import os
from pathlib import Path

import youtube_dl
from fileloghelper import Logger
from youtube_dl.utils import DownloadError, UnavailableVideoError

import utils
from utils import DESCRIPTION, VERSION, col, removeExtension


def split_list(alist, wanted_parts=1):
    """returns the specified list cut in n parts (n=wanted_parts)"""
    avg = len(alist) / float(wanted_parts)
    out = []
    last = 0.0
    while last < len(alist):
        out.append(alist[int(last):int(last + avg)])
        last += avg
    return out


def download_list(l, options, logger: Logger, index=1, list_count=1):
    """downloads list l with options"""
    videos_without_format_avail = []
    keep_file = options.get("keep_file", False)
    options.pop("keep_file", None)
    try:
        with youtube_dl.YoutubeDL(options) as ydl:
            for i in l:
                logger.debug(
                    f"[{str(l.index(i) + 1)}/{str(index + 1)}/{str(list_count)}] downloading {i}", options.get("verbose", False))
                ydl.download([i])
    except DownloadError:
        videos_without_format_avail.append(i)
        video_format = options["format"]
        del options["format"]
    finally:
        with youtube_dl.YoutubeDL(options) as ydl:
            for i in videos_without_format_avail:
                video_name = "notafile.txt"
                ydl.download([i])
                files = os.listdir()
                files.sort()
                for i in files:
                    if not utils.is_video(i):
                        files.pop(files.index(i))
                    else:
                        video_name = i
                os.system("ffmpeg -i '" + video_name + "' '" +
                          removeExtension(video_name) + "." + video_format + "'")
                if not keep_file and video_name != "notafile.txt":
                    os.remove(video_name)


def download_query(query: list, options, logger: Logger):
    """uses youtube-dl to download the query with options"""
    # convert own arguments to ydl's
    new_options = {}
    if options.get("no_check_certificate", False):
        new_options["nocheckcertificate"] = True
    if options.get("include_ads", False):
        new_options["include_ads"] = True
    if options.get("playlist", False):
        new_options["noplaylist"] = False
    if options.get("silent", False):
        new_options["quiet"] = True
    if options.get("format", False):
        new_options["format"] = options.get("format")
    if options.get("verbose", False):
        new_options["verbose"] = True
    if options.get("filename", False):
        new_options["outtmpl"] = options.get("filename")
    lists = split_list(query, options["threads"])
    del options["threads"]
    for l in lists:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.submit(download_list, l, options,
                            lists.index(l), len(lists))


def parse_args():
    parser = argparse.ArgumentParser(
        description=DESCRIPTION)
    parser.add_argument("--version", action="version", version=VERSION)
    parser.add_argument("-ncc", "--no-check-certificate", dest="no_check_certificate", action="store_true",
                        help="pass --no-check-certificate option to youtube-dl")
    parser.add_argument("--include-ads", dest="include_ads",
                        action="store_true", help="pass --include-ads option to youtube-dl")
    parser.add_argument("--playlist", "--yes-playlist", dest="playlist",
                        action="store_true", help="pass --yes-playlist to youtube-dl")
    parser.add_argument("-v", "--verbose", dest="verbose",
                        action="store_true", help="verbose/debugging mode")
    parser.add_argument("-s", "--silent", dest="silent",
                        action="store_true", help="silent/quiet mode")
    parser.add_argument("-f", "--format", dest="format",
                        help="pass format to youtube-dl (try to download format from website)")
    parser.add_argument("-t", "--threads", dest="threads", type=int, default=1,
                        help="number of threads to use (not CPU but processes to call for video download in parallel)")
    parser.add_argument("-k", "--keep", dest="keep_file", action="store_true",
                        help="when wished format is not availabe, it will be automatically converted by default. This keeps the old format, too.")
    parser.add_argument("--filename", "--fname", nargs="?",
                        type=str, help="filename to save the file under")

    options = parser.parse_args()
    return vars(options)


def main(options, logger=None):
    if logger == None:
        logger = Logger("download.log", "download.py", True, True)
    else:
        logger.context = "download.py"
    try:
        query = utils.getQuery()
        logger.context = "download.py"
        if __name__ == "__main__":
            utils.log_header(logger, DESCRIPTION,
                             options.get("verbose", False))

        logger.debug("Options:", options.get("verbose", False))
        for i in options:
            logger.debug(
                i + ": " + str(options[i]), options.get("verbose", False))
        download_query(query, options, logger)

        # move all downloaded videos in videos directory
        repoDir = utils.repoPath()
        fs = os.listdir(repoDir)
        for f in fs:
            if utils.is_video(f):
                os.rename(f, "videos/" + f)
        logger.success("All files downloaded.",
                       not options.get("silent", False))
    except Exception as e:
        logger.handle_exception(e)
        raise e


if __name__ == "__main__":
    logger = Logger("download.log", "download.py", False, True)
    logger.header(
        True, True, DESCRIPTION, 0, True)
    main(parse_args(), logger)
