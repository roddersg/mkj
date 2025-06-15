from pathlib import Path

from shared.tags import (
    Tag,
    blank_template,
    get_tags_from_cuefile,
    get_tags_from_template,
    write_tags,
)


# maketemplate
# 	if template exists
# 		rename to template.old
# 	create template
# 	read any .cue files, grab tags, append to template
# 	add template.old to template
# 	add blank to template
def maketemplate() -> None:
    templatefile: str = "template"
    # backup old template file
    if Path(templatefile).exists():
        Path(templatefile).rename(templatefile + ".old")
    #  write_template(blank_template())
    # collect tags from any .cue files in same folder
    for f in Path().glob("*.cue"):
        tag: Tag = get_tags_from_cuefile(f.name)
        write_tags("template", tag, f.stem)
    if Path(templatefile + ".old").exists():
        tag: Tag = get_tags_from_template("template.old")
        write_tags("template", tag, "template.old")
    tag: Tag = blank_template()
    write_tags("template", tag, "Blank Template")
