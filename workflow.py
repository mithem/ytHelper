import argparse
import os
import sys

from fileloghelper import Logger

import convert
import download
import facerec
import transfer
import utils
from utils import DESCRIPTION, VERSION, col

parser = argparse.ArgumentParser(description=DESCRIPTION)
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
parser.add_argument("-b", "--bitrate", dest="bitrate",
                    type=int, default=320, help="bitrate to convert video")
parser.add_argument("-f", "--format", dest="format",
                    help="pass format to youtube-dl (try to download format from website)")
parser.add_argument("-t", "--threads", dest="threads", type=int, default=1,
                    help="number of threads to use (not CPU but processes to call for video download in parallel)")
parser.add_argument("--facerec", dest="facerec", nargs="*", metavar="path",
                    help="invoke facerec.py for selected files (filepaths)")
parser.add_argument("--test", dest="test", action="store_true",
                    help="test mode (no actual files will be downloaded/converted/changed)")
parser.add_argument("-k", "--keep", dest="keep_files", action="store_true",
                    help="when wished format is not availabe, it will be automatically converted by default. This keeps the old format, too.")
parser.add_argument("--filename", "--fname", nargs="?",
                    type=str, help="filename to save the file under")

arguments = parser.parse_args()
args = vars(arguments)
VERBOSE = args.get("verbose", False)

log = Logger("workflow.log", "workflow.py", True, True)
utils.log_header(log, DESCRIPTION, VERBOSE)

try:
    log.debug("Debug mode activated.", VERBOSE)
    log.debug("Args: ", VERBOSE)
    for i in args:
        log.debug(
            i + ": " + str(args[i]), VERBOSE)
    if not args.get("test", False):
        download.main(args, logger=log)
    if args.get("facerec", None) != None and not args.get("test", False):
        if "all" in args.get("facerec", []):
            # pass all videos from utils.getVideos() to facerec
            facerec.main({"files": utils.getVideos()})
        else:
            # pass all videos from args to facerec
            facerec.main({"files": args.get("facerec", [])})
    if not args.get("test", False):
        convert.main(args, log)
    if not args.get("test", False):
        transfer.main(args, log)
    log.success("Workflow routine finished!", not args.get("silent", False))
except KeyboardInterrupt:
    log.context = "workflow.py"
    log.warning("exiting...", True)
    exit(0)
