import re
from pathlib import Path

# Map Docmost types to (admonition type, title)
type_map = {
    "info": ("info", "Note"),
    "danger": ("warning", "Warning"),
}

def convert_admonitions(file_path):
    content = file_path.read_text(encoding='utf-8')

    # Pattern: :::type\n<block body>\n:::
    pattern = re.compile(
        r'^:::(\w+)\s*\n(.*?)\n:::', 
        re.DOTALL | re.MULTILINE
    )

    def repl(match):
        raw_type = match.group(1).lower()
        body = match.group(2).strip()
        admon_type, title = type_map.get(raw_type, ("note", raw_type.capitalize()))

        # Indent each line by 4 spaces
        indented_body = "\n".join("    " + line for line in body.splitlines())
        return f'!!! {admon_type} "{title}"\n\n{indented_body}'

    updated = pattern.sub(repl, content)

    file_path.write_text(updated, encoding='utf-8')

def main():
    for md_file in Path("docs").rglob("*.md"):
        convert_admonitions(md_file)

if __name__ == "__main__":
    main()
