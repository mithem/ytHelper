import eyed3
import utils
import os
import sys
from pathlib import Path
from utils import col

musicDir = str(Path.home()) + "/" + str(utils.musicPath())
#musicDir = "/Users/miguel/repos/ytHelper/music/mp3/"


def newArtist(af):
    """asks the user about the artist and returns the string"""
    try:
        a = input("(" + str(af.tag.artist) + ") New Artist?> ")
    except AttributeError:
        a = input("(None) New Artist?> ")
    if a == None or a == "":
        if af.tafg.artist != None:
            return af.tag.artist
        else:
            return None
    elif a == " ":
        return None
    else:
        return a


def newAlbum(Af):
    """asks the user about the album and returns the string"""
    try:
        A = input("(" + str(Af.tag.album) + ") New Album?> ")
    except AttributeError:
        A = input("(None) New Album?> ")
    if A == None or A == "":
        if Af.tag.album != None:
            return Af.tag.album
        else:
            return None
    elif A == " ":
        return None
    else:
        return A


def newTitle(tf):
    """asks the user about the title and returns the string"""
    try:
        t = input("(" + str(tf.tag.title) + ") New Title?> ")
    except AttributeError:
        t = input("(None) New Title?> ")
    if t == None or t == "":
        if tf.tag.title != None:
            return tf.tag.title
        else:
            return None
    elif t == " ":
        return None
    else:
        return t


def setTags(array):
    """asks the user about artist, album and title of all songs in array"""
    try:
        for i in array:
            f = eyed3.load(musicDir + i)
            print("\n")
            print(str(array.index(i) + 1) + "/" + str(len(array)))
            print(i)
            print("-" * 15)
            f.tag.artist = newArtist(f)
            f.tag.album = newAlbum(f)
            f.tag.title = newTitle(f)
            f.tag.save()
            print("-" * 15)
            print("\n")
    except KeyboardInterrupt:
        print(col.WARNING + "\n\nexiting..." + col.ENDC)


if len(sys.argv) >= 2:
    files = []
    for i in range(len(sys.argv)):
        if i >= 2:
            files.append(sys.argv[i])
    setTags(files)
else:
    musicFiles = os.listdir(Path.home().__str__() +
                            "/" + utils.musicPath())
    for i in musicFiles:
        if ((os.path.isdir(Path.home().__str__() + "/" + utils.musicPath() + i)) and not (os.path.isfile(Path.home().__str__() + "/" + utils.musicPath() + i))) or i == "Music" or i == ".DS_Store" or i == ".localized":
            musicFiles.remove(i)
    if "Music" in musicFiles and os.path.isdir(Path.home().__str__() + "/" + utils.musicPath()):
        musicFiles.remove("Music")
    if ".localized" in musicFiles and os.path.isdir(Path.home().__str__() + "/" + utils.musicPath()):
        musicFiles.remove(".localized")
    setTags(musicFiles)
