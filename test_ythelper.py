import pytest
from download import split_list
from utils import is_video, removeExtension

# test download.py


def test_split_list():
    s1 = split_list([], 0)
    s2 = split_list([], 1)
    s3 = split_list(["hello world!"], 0)
    s4 = split_list(["hello world!"], 1)
    s5 = split_list(["item1", "item2", "item3", "item4"], 0)
    s6 = split_list(["item1", "item2", "item3", "item4"], 1)

    b1 = s1 == []
    b2 = s2 == [[]]
    b3 = s3 == []
    b4 = s4 == [["hello world!"]]
    b5 = s5 == []
    b6 = s6 == [["item1", "item2", "item3", "item4"]]
    print(b1, b2, b3, b4, b5, b6)
    print(s1, s2, s3, s4, s5, s6)
    assert b1 and b2 and b3 and b4 and b5 and b6

# test utily.py


def test_is_video():
    v1 = is_video("dkfgkjrkes.mp4")
    v2 = is_video("swhdui43i83h.mov")
    v3 = is_video("heldfhflsdhfw4u38lo.webm")
    v4 = is_video("dehai3hafhleakö.mkv")

    v5 = is_video("d3ug7qk3u,jd.mp3")
    v6 = is_video("u2qkd3qkfugqsabf.flaaac")
    v7 = is_video("FWLFJHaEljhdfjahf.stl")

    assert v1 and v2 and v3 and v4 and not (v5 or v6 or v7)


def test_remove_extension():
    f1 = removeExtension("dfjhskhfefjhkjsfe.mp4") == "dfjhskhfefjhkjsfe"
    f2 = removeExtension("3iz5böovulz.mkv") == "3iz5böovulz"
    f3 = removeExtension("jdjfhgsekbc47i.webm") == "jdjfhgsekbc47i"
    f4 = removeExtension("aei3ucoröiu3.mov") == "aei3ucoröiu3"
    f5 = removeExtension("adjfhsluhw3o.avi") == "adjfhsluhw3o"

    assert f1 and f2 and f3 and f4 and f5
