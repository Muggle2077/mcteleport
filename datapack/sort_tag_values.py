import json
from pathlib import Path

tag_dir = Path(".") / "data/teleport/tags"

for path in tag_dir.rglob(f"*.json"):
    with open(path, encoding="utf-8", mode="r+") as tag_file:
        tag_dict = json.load(tag_file)
        tag_dict["values"].sort()
        tag_file.seek(0)
        json.dump(tag_dict, tag_file, ensure_ascii=False, indent=2)
        tag_file.truncate()
    print(f"已生成 {path}")
