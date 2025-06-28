import re
from pathlib import Path
from urllib.parse import unquote

# This should match your public site structure
URL_PREFIX = "/Coinmarch/player-introduction"

def rewrite_links(md_path):
    text = md_path.read_text(encoding='utf-8')

    # Match: [label](Some Folder/Some Page.md)
    pattern = re.compile(r'\[([^\]]+)\]\(([^)]+\.md)\)')

    def convert_path(doc_path):
        decoded = unquote(doc_path)
        parts = Path(decoded).with_suffix('').parts  # Remove .md
        # Hyphenate each part, lowercase
        clean_parts = [p.lower().replace(' ', '-') for p in parts]
        return f"{URL_PREFIX}/{'/'.join(clean_parts)}/"

    def repl(match):
        label = match.group(1)
        path = match.group(2)
        return f"[{label}]({convert_path(path)})"

    updated = pattern.sub(repl, text)
    md_path.write_text(updated, encoding='utf-8')

def main():
    for md_file in Path("docs").rglob("*.md"):
        rewrite_links(md_file)

if __name__ == "__main__":
    main()
