import json
from pathlib import Path

font_dir = Path(".") / "assets/teleport/font"

for path in font_dir.rglob(f"*.json"):
    with path.open(mode="r+", encoding="utf-8") as f:
        font_dict = json.load(f)
        font_dict["providers"].sort(key=lambda x: x["file"])
        f.seek(0)
        json.dump(font_dict, f, indent=2, ensure_ascii=False)
        f.truncate()
    print(f"已排序 {path}")
