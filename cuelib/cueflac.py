# cueflac.py
# 24-07-20
# objective:
#   requires templete, joined.cue, joined.flac and cover.jpg
#   extracts tags from template -> tagdict
#   makes the basename: ARTIST - ALBUM, renames/copies files
#   creates mkmeta.sh
#   creates Cuesheet
# returns cuefile name so that it can be checked
# any errors will be handled by sys.exit(1)

import subprocess
import sys
from pathlib import Path

from .makemeta import make_cue_tracks, make_meta
from .tag import Tag


def cueflac():
    """
    Makes the .cue, .flac and .jpg files with tags inserted.

    Returns the basename of the files created.
    """
    # check whether we have the requisite files
    files: list[str] = [
        "template",
        "joined.cue",
        "joined.flac",
        "filelist",
        "cover.jpg",
    ]
    for f in files:
        if not Path(f).is_file():
            print(f"Missing {f}")
            if f == "cover.jpg":
                ans = input("Fix/Copy cover.jpg to current folder, ENTER when ready: ")
                if not Path(f).is_file():
                    print("Can't find cover.jpg, aborting")
                else:
                    continue
            sys.exit(1)

    # we assume that template is correct
    t = Tag()
    t.from_template("template")
    print(t)

    # generate the filenames
    basename: str = f"{t.artist} - {t.album}"
    flacfile = basename + ".flac"
    cuefile = basename + ".cue"
    jpgfile = basename + ".jpg"

    # create the mkmeta.sh file
    mk: str = make_meta(t)
    with Path("mkmeta.sh").open("w") as f:
        f.write(mk)
    print("cueflac mkmeta.sh created")

    # make the cue file
    with Path(cuefile).open("w") as f:
        # hdr: str = make_cue_header(t)
        hdr: str = t.cuesheet_str()
        f.write(hdr)
        trk: str = make_cue_tracks(t)
        if trk:
            f.write(trk)
        else:
            print("cueflac Error: No tracks found")
            sys.exit(1)
    # print(f"cueflac {cuefile} created")

    # check the ceusheet file before proecesing
    subprocess.run(["subl", cuefile])
    ans: str = input(f"cueflac {cuefile} created, please check, ENTER when ready: ")

    # execute mkmeta.sh
    result = subprocess.run(["bash", "./mkmeta.sh"])
    if result.returncode != 0:
        print("Error: mkmeta.sh failed")
        sys.exit(1)
    print("cueflac mkmeta.sh executed without error.")

    return basename
