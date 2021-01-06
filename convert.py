import utils
from utils import col
import os
import sys
import argparse
from pathlib import Path
from fileloghelper import Logger
from utils import DESCRIPTION


def parse_args():
    parser = argparse.ArgumentParser(
        description="convert videos to wav and mp3s in no time!")
    parser.add_argument("bitrate", type=int, help="bitrate of new mp3")
    parser.add_argument("-s", "--silent", dest="silent",
                        action="store_true", help="silent/quiet mode")
    parser.add_argument("-v", "--verbose", dest="verbose",
                        action="store_true", help="verbose/debugging mode")

    args = parser.parse_args()
    return vars(args)


def main(options, logger=Logger()):
    VERBOSE = options.get("verbose", False)
    logger.context = "convert.py"
    if __name__ == "__main__":
        utils.log_header(logger, DESCRIPTION, VERBOSE)
    logger.debug("Bitrate: " + str(options.get("bitrate", "(error)")), VERBOSE)

    utils.convertFiles(options.get("bitrate", 320),
                       options.get("silent", False))
    logger.plain(
        "Converted files. Now extracting thumbnails from videos...", VERBOSE)
    utils.extractThumbnails(options.get("silent", False))
    logger.plain(
        "Extracted thumbnails from videos, now writing them to mp3-files...", VERBOSE)
    utils.writeThumbnails()

    logger.success("All files converted.", not options.get("silent", False))
    logger.save()


if __name__ == "__main__":
    main(parse_args())
