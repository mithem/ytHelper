import os
import shutil
import utils
import argparse
from utils import col
from pathlib import Path
from fileloghelper import Logger


def parse_args():
    parser = argparse.ArgumentParser(
        description="transfer all files from the ytHelper repo to your system folder for videos, music, pictures")
    parser.add_argument("-s", "--silent", dest="silent",
                        action="store_true", help="silent mode")
    parser.add_argument("-v", "--verbose", dest="verbose",
                        action="store_true", help="verbose/debugging mode")
    args = parser.parse_args()
    return vars(args)


def main(options, logger=Logger()):
    logger.context = "transfer.py"
    VERBOSE = options.get("verbose", False)

    if __name__ == "__main__":
        utils.log_header(logger, utils.DESCRIPTION, VERBOSE)

    for i in utils.getVideos():
        videoPath = utils.videosPath()
        if not (os.listdir(str(Path.home()) + "/" + videoPath).__contains__(i)):
            logger.plain("copying to (home)/" +
                         videoPath + ": " + str(i), VERBOSE)
            shutil.copyfile("videos/" + i, str(Path.home()) +
                            "/" + videoPath + "/" + i)

    for i in utils.getMP3s():
        musicPath = utils.musicPath()
        if not (os.listdir(str(Path.home()) + "/" + musicPath).__contains__(i)):
            logger.plain("copying to (home)/" +
                         musicPath + ": " + str(i), VERBOSE)
            shutil.copyfile("music/mp3/" + i, str(Path.home()
                                                  ) + "/" + musicPath + "/" + i)

    logger.success("Copied all pending files.",
                   not options.get("silent", False))
    logger.save()


if __name__ == "__main__":
    main(parse_args())
