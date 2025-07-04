#!/usr/bin/env python3
import glob, re, os

MD_DIR   = "docs/locations/districts"
OUT_JSON = "docs/locations/districts.json"

def parse_file(path):
    text = open(path, encoding="utf-8").read()

    # 1) name
    name = re.search(r"^#\s*(.+)", text, re.MULTILINE).group(1).strip()

    # 2) type
    dtype = re.search(r"\*\*District Type\*\*:\s*(.+)", text).group(1).strip()

    # 3) summary (under ## Summary)
    sm = re.search(
        r"^##\s*Summary\s*\n([\s\S]+?)(?=\n##\s|\Z)",
        text,
        re.MULTILINE
    )
    raw_summary = sm.group(1).strip() if sm else ""
    # collapse internal newlines
    summary = re.sub(r"\s*\n\s*", " ", raw_summary).replace('"', '\\"')

    # 4) tags: prefer new "## Tags" format
    tags = []
    m = re.search(r"^##\s*Tags\s*$\s*^(.+)", text, re.MULTILINE)
    if m:
        tags = [t.strip() for t in m.group(1).split(",") if t.strip()]
    else:
        # fallback to old **Tags**: line
        m2 = re.search(r"\*\*Tags\*\*:\s*(.+)", text)
        if m2:
            tags = [t.strip() for t in m2.group(1).split(",") if t.strip()]

    # 5) coordinates
    coords_block = re.search(
        r"<details>.*?<summary>Coordinates</summary>(.*?)</details>",
        text, re.DOTALL
    ).group(1)
    coords = re.findall(r"\[\s*(\d+)\s*,\s*(\d+)\s*\]", coords_block)
    coords = [[int(x), int(y)] for x, y in coords]

    # 6) link
    link = os.path.join(MD_DIR, os.path.basename(path)).replace("\\", "/")

    return {
        "name": name,
        "type": dtype,
        "summary": summary,
        "tags": tags,
        "coordinates": coords,
        "link": link
    }

def chunked(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

# gather & parse
entries = [parse_file(md) for md in sorted(glob.glob(f"{MD_DIR}/*.md"))]

# write out JSON
with open(OUT_JSON, "w", encoding="utf-8") as f:
    f.write("[\n")
    for ei, e in enumerate(entries):
        f.write("  {\n")
        f.write(f'    "name": "{e["name"]}",\n')
        f.write(f'    "type": "{e["type"]}",\n')
        f.write(f'    "summary": "{e["summary"]}",\n')

        # tags
        f.write('    "tags": [\n')
        for ti, tag in enumerate(e["tags"]):
            comma = "," if ti < len(e["tags"]) - 1 else ""
            f.write(f'      "{tag}"{comma}\n')
        f.write("    ],\n")

        # coordinates, in groups of 5
        f.write('    "coordinates": [\n')
        chunks = list(chunked(e["coordinates"], 5))
        for ci, chunk in enumerate(chunks):
            coords_str = ", ".join(f"[{x},{y}]" for x, y in chunk)
            comma = "," if ci < len(chunks) - 1 else ""
            f.write(f"      {coords_str}{comma}\n")
        f.write("    ],\n")

        f.write(f'    "link": "{e["link"]}"\n')
        f.write("  }")
        if ei < len(entries) - 1:
            f.write(",")
        f.write("\n")
    f.write("]\n")
