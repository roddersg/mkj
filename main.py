# import os
import subprocess
import sys
from pathlib import Path

from cuelib.cueflac import cueflac
from cuelib.filelist import make_filelist
from cuelib.maketemplate import maketemplate
from cuelib.movemusic import movemusic

TARGETDIR: str = str(Path.home() / "Music/done/cdimages")


def run_command_capture_output(command):
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

    output_lines = []
    while True:
        line = process.stdout.readline()
        if not line:
            break
        print(line, end="")
        output_lines.append(line)

    process.wait()
    return "".join(output_lines), process.returncode


def main():
    print("mkj v0.3.0")

    # remove joined.flac and joined.cue before running shntool
    print("Removing joined.flac and joined.cue")
    if Path("joined.cue").exists():
        Path("joined.cue").unlink()
    if Path("joined.flac").exists():
        Path("joined.flac").unlink()

    if Path("template").is_file():
        ans: str = input("Template file exists, use it? (y/N) " or "N")
        if ans == "N":
            maketemplate()
            print("template created.")
    else:
        maketemplate()
        print("template created.")

    make_filelist()
    print("filelist & filelist.org created")

    # allow user to edit template, filelist
    # shntool cue -F filelist.org > joined.cue
    # shntool join -F filelist.org -o flac     ---> joined.flac

    # don't need to check, as this just calls the editor
    result = subprocess.run(["subl", "template", "filelist"])

    # result = subprocess.run(
    #     ["shntool", "cue", "-F", "filelist.org"], capture_output=True, text=True
    # )
    # command_to_run: list[str] = ["shntool", "cue", "-F", "filelist.org"]
    # output, return_code = run_command_capture_output(command_to_run)
    print("Creating joined.cue")
    result = subprocess.run(
        ["shntool", "cue", "-F", "filelist.org"], capture_output=True, text=True
    )
    output, return_code = (result.stdout, result.returncode)
    if return_code == 0:
        with Path("joined.cue").open("w") as f:
            f.write(output)
    else:
        print("Error running shntool cue")
        sys.exit(1)

    print("Creating joined.flac")
    result = subprocess.run(["shntool", "join", "-F", "filelist.org", "-o", "flac"])
    if result.returncode != 0:
        print("Error running shntool join")
        sys.exit(1)

    ans = input(
        "\nFinished join, check template and filelist, press ENTER when ready to run cueflac.py : "
    )
    # ignore the answer, as this is just to pause

    # create the necessary files for operation
    basename = cueflac()

    # move the files
    movemusic(basename, TARGETDIR)

    print("Completed!")


if __name__ == "__main__":
    main()
