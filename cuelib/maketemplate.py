from pathlib import Path

from .tag import Tag


# maketemplate
# 	if template exists
# 		rename to template.old
# 	create template
# 	read any .cue files, grab tags, append to template
# 	add template.old to template
# 	add blank to template
def maketemplate() -> None:
    templatefile: str = "template"
    old_templatefile: str = "template.old"
    # backup old template file
    if Path(templatefile).exists():
        Path(templatefile).rename(old_templatefile)
    #  write_template(blank_template())
    # collect tags from any .cue files in same folder
    t = Tag()
    for fc in Path().glob("*.cue"):
        t = Tag()
        t.from_cuesheet(fc.name)
        s: str = t.template_str(fc.name)
        with Path(templatefile).open("a") as f:
            f.write(s)

    if Path(old_templatefile).exists():
        t = Tag()
        t.from_template(old_templatefile)
        s: str = t.template_str(old_templatefile)
        with Path(templatefile).open("a") as f:
            f.write(s)

    t = Tag()
    s: str = t.blank_template_str()
    with Path(templatefile).open("a") as f:
        f.write(s)
