import json
import os
import re

from pathlib import Path

lang_dir = Path(".").absolute().parent / "resourcepack/assets/teleport/lang"
mcf_dir = Path(".") / "data/teleport"

output_path = Path(".") / "output.md"
output_list = []

match_pattern = "['\"]?translate['\"]? *: *['\"]([^'\"]*)['\"]"
resource_trans: dict[str, dict] = {}
for path in lang_dir.rglob(f"*.json"):
    with open(path, mode="r", encoding="utf-8") as f:
        resource_trans[path.name] = json.load(f)

trans_keys = set()
for file_type in ("mcfunction", "json"):
    for path in mcf_dir.rglob(f"*.{file_type}"):
        with open(path, mode="r", encoding="utf-8") as f:
            file_contents = f.read()
        trans_keys |= set(re.findall(match_pattern, file_contents))

for lang_name in resource_trans:
    current_trans = resource_trans[lang_name]
    in_both = {k: current_trans[k] for k in sorted(current_trans.keys() & trans_keys)}
    only_in_data = {
        k: current_trans[k] for k in sorted(current_trans.keys() - trans_keys)
    }
    only_in_resource = trans_keys - current_trans.keys()
    output_list.append(
        f"""# {lang_name}
## 都有
```
{json.dumps(in_both,indent=2, ensure_ascii=False)}
```
## 只在资源包
```
{json.dumps(only_in_data,indent=2, ensure_ascii=False)}
```
## 只在数据包
```
{json.dumps(sorted(only_in_resource),indent=2, ensure_ascii=False)}
```
"""
    )

with open(output_path, mode="w+", encoding="utf-8") as f:
    f.write("\n".join(output_list))

print(f"已生成 {output_path}")

os.startfile(output_path)
