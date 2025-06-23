import re
from pathlib import Path


def title_case(s: str) -> str:
    """
    Convert string into title-case.

    be mindful of the character after the '
    does not convert bel-reid to Bel-Reid
    does not convert 1st char after (,
    """
    b = []
    for word in s.split(" "):
        if word:
            if word[0] in "([{":
                word = word[0] + word[1:].capitalize()
            else:
                word = word.capitalize()
        b.append(word)
    return " ".join(b)


def remove_funny_chars(s: str) -> str:
    s = s.replace("_", " ")
    s = s.replace("?", " ")
    s = s.replace(":", " ")
    s = s.replace('"', "'")
    return s


def convert_roman(text: str) -> str:
    roman_numerals = {
        "i": "I",
        "ii": "II",
        "iii": "III",
        "iv": "IV",
        "v": "V",
        "vi": "VI",
        "vii": "VII",
        "viii": "VIII",
        "ix": "IX",
        "x": "X",
    }

    pattern = r"\b(?:i{1,3}|iv|v|vi{1,3}|ix|x)\b"
    result = re.sub(
        pattern,
        lambda m: roman_numerals.get(m.group().lower(), m.group()),
        text,
        flags=re.IGNORECASE,
    )

    return result


def get_filelist(multipleflag: bool = False) -> list[str]:
    """
    Scans current folder for flac files and returns a list.

    If multipleFlag, it means we have NN - Artist - Title
    So detect '-' and insert a sperator '|', check for number of '-'.
    Returns filelist as well as writing to file: filelist
    Creates "filelist.org" (original listing) and "filelist" for editing.
    """
    flacfiles = sorted(Path().glob("*.flac"))
    # write out this to filelist.org
    with Path("filelist.org").open("w") as f:
        for file in flacfiles:
            f.write(f"{file.name}\n")

    # clean up the filenames
    filelist = []
    for ff in flacfiles:
        # remove the .flac
        fname = ff.name[:-5]
        # clean up the filename
        fname: str = remove_funny_chars(fname)
        fname = title_case(fname)
        fname = convert_roman(fname)
        # check whether multiple artists, the separator is '-'
        if multipleflag:
            n = fname.count("-")
            s: str = ""
            if n < 2:
                s: str = "<"
            elif n == 2:
                s: str = ""
            elif n > 2:
                s: str = "*" * (n - 2)
            fname = s + fname.replace("-", "|")

        filelist.append(fname)

    # write the filelist
    with Path("filelist").open("w") as f:
        for fl in filelist:
            f.write(f"{fl}\n")

    return filelist


def make_filelist():
    """
    Creates filelist and filelist.org.

    filelist is a list of flac files, sorted by trk no.
    If multiple artists are selected then the artist and title are
    separated by "|"
    We assume that the tracks are "tt - Artist - Title"
    filelist.org is the original flac file lists
    """
    # ans: str = get_input_yn("Single Artists? (Y/n)", default="Y")
    ans: str = input("Single Album Artist (Y/n) ? ") or "Y"
    if ans == "Y":
        get_filelist(multipleflag=False)
    else:
        get_filelist(multipleflag=True)


if __name__ == "__main__":
    make_filelist()
