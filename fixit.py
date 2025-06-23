# fixit.py
# fixes the music files and moves them if necessary

# %%
from pathlib import Path
from cuelib.tag import Tag


def fixit(cuefile: str, movefiles: bool = True, cleanup: bool = True) -> int:
    """
    Fixes the music files and moves them if necessary.

    Returns a non-zero value if an error occurs.
    """

    # check to see whether all files are present
    basename = Path(cuefile).stem
    flacfile = basename + ".flac"
    cuefile: str = basename + ".cue"
    jpgfile = basename + ".jpg"

    files = [flacfile, cuefile, jpgfile]
    for f in files:
        if not Path(f).is_file():
            print(f"fixit: Error - Missing {f}")
            return 1

`   # rename the flac file
    Path(flacfile).rename("joined.flac")
    # rename the .jpg if cover.jpg does not exist
    if Path("cover.jpg").is_file(): 
        Path(jpgfile).unlink()
    else:
        Path(jpgfile).rename("cover.jpg")
    
    # cuefile is correct, so get the tags from it
    t = Tag()
    t.from_cuesheet(cuefile)
    


    return 0
