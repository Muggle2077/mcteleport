import json
from pathlib import Path

lang_dir = Path(".") / "assets/teleport/lang"

for path in lang_dir.rglob(f"*.json"):
    with path.open(mode="r+", encoding="utf-8") as f:
        lang_dict: dict = json.load(f)
        sorted_lang_dict = dict(sorted(lang_dict.items()))
        f.seek(0)
        json.dump(sorted_lang_dict, f, indent=2, ensure_ascii=False)
        f.truncate()
    print(f"已排序 {path}")
