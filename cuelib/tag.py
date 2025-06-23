from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


# Standalone functions---------------------------------
def empty_str(s: str | None) -> str:
    if s is None:
        return "None"
    if s == "":
        return '""'
    return s


# -----------------------------------------------------


@dataclass
class Tag:
    discid: str = ""
    artist: str = ""
    album: str = ""
    date: str = ""
    genre: str = ""
    comment: str = datetime.now().strftime("%Y-%m-%d")
    compilation: str = ""
    discnumber: str = ""
    totaldiscs: str = ""
    albumartist: str = ""

    def __str__(self):
        indent: str = " " * 2
        return f"""Tag Object:
{indent}discid     : {empty_str(self.discid)}
{indent}artist     : {empty_str(self.artist)}
{indent}album      : {empty_str(self.album)}
{indent}date       : {empty_str(self.date)}
{indent}genre      : {empty_str(self.genre)}
{indent}comment    : {empty_str(self.comment)}
{indent}compilation: {empty_str(self.compilation)}
{indent}discnumber : {empty_str(self.discnumber)}
{indent}totaldiscs : {empty_str(self.totaldiscs)}
{indent}albumartist: {empty_str(self.albumartist)}

"""

    def to_dict(self):
        return asdict(self)

    def from_template(self, templatefile: str) -> None:
        """Reads tags from template file."""
        with Path(templatefile).open("r") as f:
            # each tag on a separate line, remove newlines
            lines = f.read().splitlines()
        # extract the tag name and the value
        for line in lines:
            # skip blank or comment lines
            if line.strip() == "" or line.startswith("#"):
                continue

            parts = line.split("=")
            name = parts[0].upper().strip()
            value = " ".join(parts[1:])
            value = value.strip().strip('"')

            match name:
                case "DISCID":
                    self.discid = value
                case "ARTIST":
                    self.artist = value
                    if self.artist.startswith("The "):
                        self.artist = self.artist[4:] + ", The"
                case "ALBUM":
                    self.album = value
                case "DATE":
                    self.date = value
                case "GENRE":
                    self.genre = value
                case "COMMENT":
                    self.comment = value
                case "COMPILATION":
                    self.compilation = value
                case "DISCNUMBER":
                    self.discnumber = value
                case "TOTALDISCS":
                    self.totaldiscs = value
                case "ALBUMARTIST":
                    self.albumartist = value
                    if self.albumartist.startswith("The "):
                        self.albumartist = self.albumartist[4:] + ", The"

    def from_cuesheet(self, cuesheet: str) -> None:
        """Extracts tags from cuesheet file."""
        with Path(cuesheet).open("r") as cf:
            lines = cf.read()
        # spilt the file, only top part is requied
        parts = lines.split("TRACK 01 AUDIO")
        tagpart = parts[0]
        taglines = tagpart.splitlines()
        # go through each line and extract the tag and value
        for tline in taglines:
            if tline.startswith("REM"):
                tlp = tline[4:].split(" ")
                # print(tlp)
                # only consider if there are at least 2 parts
                if len(tlp) > 1:
                    name = tlp[0].upper()
                    value = " ".join(tlp[1:])
                    value = value.strip()
                    match name:
                        case "DISCID":
                            self.discid = value
                        case "DATE":
                            self.date = value
                        case "GENRE":
                            self.genre = value
                        case "COMMENT":
                            self.comment = value
                        case "COMPILATION":
                            self.compilation = value
                        case "ALBUMARTIST":
                            self.albumartist = value
                            if self.albumartist.startswith("The "):
                                self.albumartist = self.albumartist[4:] + ", The"
                        case "DISCNUMBER":
                            self.discnumber = value
                        case "TOTALDISCS":
                            self.totaldiscs = value
            elif tline.startswith("PERFORMER"):
                self.artist = tline[9:].strip().strip('"')
                if self.artist.startswith("The "):
                    self.artist = self.artist[4:] + ", The"
            elif tline.startswith("TITLE"):
                self.album = tline[6:].strip().strip('"')

    def template_str(self, header: str):
        """Returns a string for writing template."""
        ts: str = f"#---------- {header} ----------#\n"
        # ts += f"DISCID={self.discid}\n"
        if not self.discid in ["", None]:
            ts += f"DISCID={self.discid}\n"
        ts += f"ARTIST={self.artist}\n"
        ts += f"ALBUM={self.album}\n"
        ts += f"DATE={self.date}\n"
        ts += f"GENRE={self.genre}\n"
        ts += f"COMMENT={self.comment}\n"
        # skip if compilation is 0
        if not self.compilation in ["0", "", None]:
            ts += f"COMPILATION={self.compilation}\n"
        if self.discnumber != "":
            ts += f"DISCNUMBER={self.discnumber}\n"
        if self.totaldiscs != "":
            ts += f"TOTALDISCS={self.totaldiscs}\n"
        if self.albumartist != "":
            ts += f"ALBUMARTIST={self.albumartist}\n"
        ts += "\n"
        return ts

    def blank_template_str(self):
        """Returns a string for a blank template."""
        ts: str = f"#---------- BLANK TEMPLATE ----------#\n"
        ts += f"DISCID=\n"
        ts += f"ARTIST=\n"
        ts += f"ALBUM=\n"
        ts += f"DATE=\n"
        ts += f"GENRE=\n"
        ts += f"COMMENT={datetime.now().strftime('%Y-%m-%d')}\n"
        ts += f"COMPILATION=\n"
        ts += f"DISCNUMBER=\n"
        ts += f"TOTALDISCS=\n"
        ts += f"ALBUMARTIST=\n"
        ts += "\n"
        return ts

    def cuesheet_str(self) -> str:
        """Returns a string for the cuesheet header."""
        cs: str = ""
        if self.discid not in ["", None]:
            cs += f"REM DISCID {self.discid}\n"
        cs += f"REM DATE {self.date}\n"
        cs += f"REM GENRE {self.genre}\n"
        cs += f'REM COMMENT "{self.comment}"\n'
        if self.compilation not in ["0", "", None]:
            cs += f"REM COMPILATION {self.compilation}\n"
        if self.discnumber != "":
            cs += f"REM DISCNUMBER {self.discnumber}\n"
        if self.totaldiscs != "":
            cs += f"REM TOTALDISCS {self.totaldiscs}\n"
        if self.albumartist != "":
            cs += f'REM ALBUMARTIST "{self.albumartist}"\n'
        cs += f'PERFORMER "{self.artist}"\n'
        cs += f'TITLE "{self.album}"\n'
        cs += f'FILE "{self.artist} - {self.album}.flac" WAVE\n'
        return cs

    def check(self) -> bool:
        """Check tags for validity."""
        # artist, album, date, genre must be present
        if not self.artist.strip():
            print("Check: ARTIST missing")
            return False
        if not self.album.strip():
            print("Check: ALBUM missing")
            return False
        if not self.genre.strip():
            print("Check: GENRE missing")
            return False
        # check date
        if not self.date.strip():
            print("Check: DATE missing")
            return False
        try:
            d = int(self.date)
            if 1950 <= d <= 2050:
                pass
            else:
                print("Check: DATE not valid")
                return False
        except ValueError:
            print("Check: DATE not valid")
            return False
        # check compilation
        if self.compilation.strip() not in ["", "0", "1"]:
            print("Check: COMPILATION value not valid")
            return False
        # check discnumber and totaldics
        dn = self.discnumber.strip()
        td: str = self.totaldiscs.strip()
        if dn == "":
            if td != "":
                print("Check: DISCNUMBER missing when TOTALDISCS is present")
                return False
        else:
            try:
                idn = int(dn)
                if 1 <= idn <= 99:
                    pass
                else:
                    print("Check: DISCNUMBER range 1..99")
                    return False
            except ValueError:
                print("Check: DISCNUMBER not integer value")
                return False
            if td == "":
                print("Check: TOTALDISCS missing when DISCNUMBER is present")
                return False
            # numbersidcs, totaldiscs have values
            try:
                itd = int(td)
                if (itd > 1) and (idn <= itd):
                    pass
                else:
                    # print(f"dn={idn}, td={itd}")
                    print("Check: TOTALDISCS > 1 and >= DISCNUMBER")
                    return False
            except ValueError:
                print("Check: TOTALDISCS not integer value")
                return False
        return True
