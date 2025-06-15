import datetime
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class Tag:
    discid: str = ""
    artist: str = ""
    album: str = ""
    date: str = ""
    genre: str = ""
    comment: str = ""
    compilation: str = ""
    discnumber: str = ""
    totaldiscs: str = ""
    albumartist: str = ""


def tag_to_dict(tag: Tag) -> dict:
    return asdict(tag)


def clean_str(s: str) -> str:
    """Cleans up a string removing whitespace and quotes."""
    return s.strip().strip('"')


def get_tags_from_cuefile(cuefile: str) -> Tag:
    """Reads cuefile and return a Tag object."""
    t = Tag()
    with Path(cuefile).open("r") as f:
        lines: list[str] = f.readlines()
    for line in lines:
        if line.startswith("REM DISCID"):
            t.discid = clean_str(line[10:])
        elif line.startswith("PERFORMER"):
            t.artist = clean_str(line[9:])
        elif line.startswith("TITLE"):
            t.album = clean_str(line[6:])
        elif line.startswith("REM DATE"):
            t.date = clean_str(line[8:])
        elif line.startswith("REM GENRE"):
            t.genre = clean_str(line[9:])
        elif line.startswith("REM COMMENT"):
            t.comment = clean_str(line[12:])
        elif line.startswith("REM COMPILATION"):
            t.compilation = clean_str(line[16:])
        elif line.startswith("REM DISCNUMBER"):
            t.discnumber = clean_str(line[15:])
        elif line.startswith("REM TOTALDISCS"):
            t.totaldiscs = clean_str(line[15:])
        elif line.startswith("REM ALBUMARTIST"):
            t.albumartist = clean_str(line[16:])
    return t


def get_tags_from_template(templatefile: str) -> Tag:
    """Returns a Tag object from a template file."""
    t = Tag()
    with Path(templatefile).open("r") as f:
        lines = f.readlines()
    for line in lines:
        nl = line.split("=")
        if nl[0] == "DISCID":
            t.discid = clean_str(nl[1])
        elif nl[0] == "ARTIST":
            t.artist = clean_str(nl[1])
        elif nl[0] == "ALBUM":
            t.album = clean_str(nl[1])
        elif nl[0] == "DATE":
            t.date = clean_str(nl[1])
        elif nl[0] == "GENRE":
            t.genre = clean_str(nl[1])
        elif nl[0] == "COMMENT":
            t.comment = clean_str(nl[1])
        elif nl[0] == "COMPILATION":
            t.compilation = clean_str(nl[1])
        elif nl[0] == "DISCNUMBER":
            t.discnumber = clean_str(nl[1])
        elif nl[0] == "TOTALDISCS":
            t.totaldiscs = clean_str(nl[1])
        elif nl[0] == "ALBUMARTIST":
            t.albumartist = clean_str(nl[1])
    return t


def blank_template() -> Tag:
    t: Tag = Tag()
    today: datetime.date = datetime.date.today()
    t.comment = f"{today.year}-{today.month:02}-{today.day:02}"
    return t


def write_tags(templatefile: str, tag: Tag, header: str = "template") -> None:
    """Writes tags to a template file with comments."""
    with Path(templatefile).open("a") as f:
        f.write(f"#---------- {header} ----------#\n")
        f.write(f"DISCID={tag.discid}\n")
        f.write(f"ARTIST={tag.artist}\n")
        f.write(f"ALBUM={tag.album}\n")
        f.write(f"DATE={tag.date}\n")
        f.write(f"GENRE={tag.genre}\n")
        f.write(f"COMMENT={tag.comment}\n")
        f.write(f"COMPILATION={tag.compilation}\n")
        f.write(f"DISCNUMBER={tag.discnumber}\n")
        f.write(f"TOTALDISCS={tag.totaldiscs}\n")
        f.write(f"ALBUMARTIST={tag.albumartist}\n")
        f.write("\n")
