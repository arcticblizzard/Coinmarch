import re
from pathlib import Path

# Map Docmost types to MyST admonition type + title
TYPE_MAP = {
    "info":   ("note",    "Note"),
    "danger": ("warning", "Warning"),
}

# This pattern finds:
#  1) an optional indent (captured as "indent")
#  2) an opening marker :::type on its own line
#  3) everything up to the matching closing ::: on its own line
# It uses a non-greedy match for the body so it stops at the first closing :::.
PATTERN = re.compile(
    r'''
    ^(?P<indent>[ \t]*)        # any leading spaces or tabs
     :::(?P<type>\w+)\s*$      # opening marker :::type
    \r?\n                       # end of that line
    (?P<body>[\s\S]*?)          # body (non-greedy)
    ^[ \t]*:::\s*$              # closing ::: on its own line
    ''',
    re.MULTILINE | re.VERBOSE,
)

def convert_admonitions(file_path: Path):
    text = file_path.read_text(encoding="utf-8")

    def _repl(m: re.Match) -> str:
        indent = m.group("indent")
        raw   = m.group("type").lower()
        body  = m.group("body").rstrip("\r\n")

        admon_type, title = TYPE_MAP.get(raw, ("note", raw.capitalize()))

        # indent each line of the original body one level deeper
        lines = body.splitlines()
        indented = "\n".join(f"{indent}    {line.lstrip()}" for line in lines)

        # build the replacement, preserving the original indent:
        #  1) the `!!!` line at the same indent as the original :::  
        #  2) a blank line at that same indent to start the block  
        #  3) the indented body lines  
        #  4) a final blank line at the original indent to break out of the block
        return (
            f"{indent}!!! {admon_type} \"{title}\"\n"
            f"{indent}\n"
            f"{indented}\n"
            f"{indent}\n"
        )

    new_text = PATTERN.sub(_repl, text)
    file_path.write_text(new_text, encoding="utf-8")


def main():
    for md in Path("docs").rglob("*.md"):
        convert_admonitions(md)


if __name__ == "__main__":
    main()
