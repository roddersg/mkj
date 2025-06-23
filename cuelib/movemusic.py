# movemusic.py
# moves the .cue, .flac. .jpg files to the TARGETDIR

import re
import sys
from pathlib import Path

from .tag import Tag


def movemusic(basename: str, targetdir: str):
    """Moves the music files to the target directory."""
    # check whether targetdir exists
    if not Path(targetdir).is_dir():
        print(f"{targetdir} does not exist")
        sys.exit(1)
    # check that the music files exist
    flacfile = basename + ".flac"
    jpgfile = basename + ".jpg"
    cuefile = basename + ".cue"

    files: list[str] = [flacfile, jpgfile, cuefile]
    for f in files:
        if not Path(f).is_file():
            print(f"movemusic:Missing {f}")
            sys.exit(1)

    # we need the tags to form the folder
    t = Tag()
    t.from_cuesheet(basename + ".cue")

    # obtain the album directory
    # fix the artist name first, move "The to the end"
    artist: str = t.artist
    if artist.startswith("The "):
        artist = artist[4:] + ", The"
    # fix the album name, if it is part of a multi-disc album
    album: str = re.sub(r" CD[0-9]*", "", t.album)
    basefolder: str = f"{t.date}-{album}"

    # Check the genre for Christmas or Soundtrac
    if t.genre in ["Christmas", "Soundtrack"]:
        targetfolder: str = f"{targetdir}/{t.genre}"
    else:
        targetfolder: str = targetdir

    # add the artist, date-album
    targetfolder = f"{targetfolder}/{artist}/{basefolder}"
    # now make the directory
    Path(targetfolder).mkdir(parents=True, exist_ok=True)

    # move the files
    for f in files:
        Path(f).rename(f"{targetfolder}/{f}")

    print("movemusic done!")
