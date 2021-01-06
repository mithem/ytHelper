# ytHelper

## Setup

- run setup.py and enter folders (e.g. /home/name/Videos)

## Requirements

- youtube-dl
- mplayer
- lame
- eyeD3 (command-line)
- ffmpeg (command-line)

## Usage

- enter YT-URLs to download each on a new line in config.json
- run download.py to download pending videos into the videos directory
- run convert.py to convert all videos in the videos directory to wav and mp3-format in the music directory
- run transfer.py to copy all videos and wav-audio files into $home/Videos, $home/Music etc (you can customize this by running setup.py)
- run workflow.py to do all steps above (from download on) automatically

## Features

- Downloads YouTube-Videos into the videos directory
- Converts Videos to wav and mp3-format
- copies videos and wav-audio into home/videos, respectively home/music (customizable)
- extracts thumbnails to /thumbnails and writes them to the mp3 files

### Parameters

| parameter              | description                                                                                                                                               |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| -b [bitrate]           | sets the bitrate for conversion (only MP3s, max. 320 bits/s; only in **workflow** and **convert**)                                                        |
| -p [provider]          | sets the library to be used to download the videos (pytube / youtube-dl; only in **workflow** and **download**)                                           |
| --no-check-certificate | passes option to youtube-dl (only in **workflow** and **download**)                                                                                       |
| --include-ads          | passes option to youtube-dl (only in **workflow** and **download**)                                                                                       |
| --format [format]      | passes '--format [format]' to youtube-dl (only in **workflow** and **download**)                                                                          |
| --playlist             | passes '--yes-playlist' to youtube-dl (only in **workflow** and **download**)                                                                             |
| --verbose              | enables verbose mode                                                                                                                                      |
| --threads [n]          | uses n threads (only in **workflow** and **download**)                                                                                                    |
| --filename [fname]     | saves downloaded videos under specified template (as in ytdl, for single videos, this can be a normal string, too; only in **workflow** and **download**) |
