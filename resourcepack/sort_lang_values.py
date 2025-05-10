from pathlib import Path
import json

lang_dir = Path(".") / "assets/teleport/lang"

for path in lang_dir.rglob(f"*.json"):
    with open(path, encoding="utf-8", mode="r+") as f:
        lang_dict: dict = json.load(f)
        sorted_lang_dict = dict(sorted(lang_dict.items()))
        f.seek(0)
        json.dump(sorted_lang_dict, f, indent=2, ensure_ascii=False)
        f.truncate()
    print(f"已排序 {path}")
