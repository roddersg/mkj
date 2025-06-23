import re
from pathlib import Path

from .tag import Tag

# make_meta.py
# contains functions to make the files required for mkmeta
# make_meta - makes the cmd line file
# make_cue_header - makes the cue header
# make_cue_tracks  - makes the cue tracks


def make_meta(tag: Tag) -> str:
    """
    Makes the meta.sh cmd from the tags.

    renames joined.flac to basename.flac
    copies cover.jpg to basename.jpg
    instructs metaflac.exe to remove all tags
    instructs metaflac.exe to add the tags

    Returns the cmd as a str
    """
    basename: str = f"{tag.artist} - {tag.album}"
    cuefile = basename + ".cue"
    flacfile = basename + ".flac"
    jpgfile = basename + ".jpg"

    mkstr: str = ""
    mkstr += "#! /.bin/bash\n"
    mkstr += f'mv -vv joined.flac "{flacfile}"\n'
    mkstr += f'cp -vv cover.jpg "{jpgfile}"\n'
    mkstr += f'metaflac --remove-all "{flacfile}"\n'
    mkstr += "metaflac "
    tagdict = tag.to_dict()
    # --------need to change this, perhaps in tags
    # for t in tagdict:
    #     f.write(f' --set-tag={ttag}="{tagdict[ttag]}"')

    for k, v in tagdict.items():
        if v:
            mkstr += f' --set-tag={k.upper()}="{v}" \\\n'

    mkstr += f' --set-tag-from-file=CUESHEET="{cuefile}" \\\n'
    mkstr += f' --import-cuesheet-from="{cuefile}" \\\n'
    mkstr += f' --import-picture-from="{jpgfile}" \\\n'
    mkstr += f' "{flacfile}"\n'
    return mkstr


# def make_cue_header(tag: Tag) -> str:
#     """
#     Creates the cue header from the tags.

#     Returns a str containing the cue header.
#     """
#     header: str = ""
#     # easiest way is to use the tags
#     tagdict = tag.to_dict()
#     # write out the cue header
#     header += f"REM DISCID {tagdict['discid']}\n"
#     header += f"REM DATE {tagdict['date']}\n"
#     header += f"REM GENRE {tagdict['genre']}\n"
#     header += f"REM COMMENT {tagdict['comment']}\n"
#     if tagdict["compilation"]:
#         header += f"REM COMPILATION {tagdict['compilation']}\n"
#     if tagdict["discnumber"]:
#         header += f"REM DISCNUMBER {tagdict['discnumber']}\n"
#     if tagdict["totaldiscs"]:
#         header += f"REM TOTALDISCS {tagdict['totaldiscs']}\n"
#     header += f"REM ALBUMARTIST {tagdict['albumartist']}\n"
#     header += f'PERFORMER "{tagdict["artist"]}"\n'
#     header += f'TITLE "{tagdict["album"]}"\n'
#     header += f'FILE "{tagdict["artist"]} - {tagdict["album"]}.flac" WAVE\n'

#     return header


def make_cue_tracks(tag: Tag) -> str:
    """
    Makes the tracks section of the cuesheet file.

    Returns a string of the track section.
    """
    SPACES: int = 2  # number of spaces for INDENTing
    INDENT: str = " " * SPACES  # INDENT string

    # required from tags
    COMPILATION = tag.compilation
    ARTIST = tag.artist

    # read the joined file
    with Path("joined.cue").open("r") as file:
        content = file.read()
    pattern = re.compile(r"\s+TRACK\s+", re.IGNORECASE | re.MULTILINE | re.DOTALL)
    trks = pattern.split(content)
    trks.pop(0)
    # FILE is done in the header section
    trackinfo = []
    for trk in trks:
        t = trk.split("\n")
        nt = []
        for ele in t:
            if ele:
                nt.append(ele.strip())
        trackinfo.append(nt)

    # read in the filenames
    with Path("filelist").open("r") as fl:
        titles = fl.read().splitlines()

    # check to see whether both lists are the same length
    if len(titles) != len(trackinfo):
        print("ERROR: lists are not the same length")
        return ""

    # spaces = 2
    # INDENT = f'{" " * spaces}'
    # use the compilation flag to indicate multiple artists
    # if tagdict["ALBUMARTIST"]:
    if COMPILATION == "1":
        # multiple artists
        perfpos = int(input("Enter position of performer name (1): ") or "1")
        titlepos = int(input("Enter position of title (2): ") or "2")
        seperator = input("Enter seperator (|) : ") or "|"
        ntitles = []
        for title in titles:
            nt = title.split(seperator)
            ntitles.append(nt)
        # merge the two lists
        tracksection = ""
        for cnt, title in enumerate(ntitles):
            tracksection += f"{INDENT}TRACK {trackinfo[cnt][0]}\n"
            # fix any artist "The"
            p = title[perfpos].strip()
            if p.startswith("The "):
                p = p[4:] + ", The"
            tracksection += f'{INDENT}{INDENT}PERFORMER "{p}"\n'
            tracksection += f'{INDENT}{INDENT}TITLE "{title[titlepos].strip()}"\n'
            for ele in trackinfo[cnt][1:]:
                if ele is not None:
                    tracksection += f"{INDENT}{INDENT}{ele}\n"
    else:
        # single artist
        pos = int(input("Enter position of Songs: ") or "1")
        for i, title in enumerate(titles):
            titles[i] = title[pos - 1 :]
        # merge the two lists
        tracksection = ""
        for cnt, title in enumerate(titles):
            tracksection += f"{INDENT}TRACK {trackinfo[cnt][0]}\n"
            tracksection += f'{INDENT}{INDENT}PERFORMER "{ARTIST}"\n'
            tracksection += f'{INDENT}{INDENT}TITLE "{title}"\n'
            for ele in trackinfo[cnt][1:]:
                if ele is not None:
                    tracksection += f"{INDENT}{INDENT}{ele}\n"
    return tracksection
