import json
import os
from pathlib import Path

lang_a_name = "zh_cn.json"
lang_dir = Path(".") / "assets/teleport/lang"

output_path = Path(".") / "output.md"
output_list = []

with (lang_dir / lang_a_name).open(mode="r", encoding="utf-8") as f:
    lang_a: dict = json.load(f)

lang_dict = {}
for path in lang_dir.rglob(f"*.json"):
    if (lang_b_name := path.name) != lang_a_name:
        with path.open(mode="r", encoding="utf-8") as f:
            lang_dict[lang_b_name] = json.load(f)

lang_b: dict
for lang_b_name, lang_b in lang_dict.items():
    only_in_a = {k: v for k, v in lang_a.items() if k not in lang_b}
    only_in_b = {k: v for k, v in lang_b.items() if k not in lang_a}
    output_list.append(
        f"""# {lang_b_name}
## 删除
```json
{json.dumps(only_in_a,indent=2, ensure_ascii=False)}
```
## 增加
```json
{json.dumps(only_in_b,indent=2, ensure_ascii=False)}
```"""
    )

output_path.write_text("\n".join(output_list), encoding="utf-8")

print(f"已生成 {output_path}")
os.startfile(output_path)
