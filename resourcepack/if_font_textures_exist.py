import json
import os
from pathlib import Path

font_dir = Path(".") / "assets/teleport/font"
texture_dir = Path(".") / "assets/teleport/textures"

output_path = Path(".") / "output.md"
output_list = []

invalid_paths: set[Path] = set()
valid_paths: set[Path] = set()

for path in font_dir.rglob(f"*.json"):
    with open(path, encoding="utf-8", mode="r+") as font_file:
        font_dict = json.load(font_file)
    for provider in font_dict["providers"]:
        if "file" in provider:
            namespace_path: str = provider["file"]
            namespace, name = namespace_path.split(":", 1)
            real_path = Path(".") / f"assets/{namespace}/textures/{name}"
            if real_path.exists():
                valid_paths.add(real_path)
            else:
                invalid_paths.add(real_path)
unused_paths: set[Path] = set(path for path in texture_dir.rglob("*.png")) - valid_paths

with output_path.open(mode="w+", encoding="utf-8") as f:
    f.write(
        f'''# 不存在的路径
```
{'\n'.join(sorted([path.as_posix() for path in invalid_paths]))}
```
# 未被使用的路径
```
{'\n'.join(sorted([path.as_posix() for path in unused_paths]))}
```'''
    )

print(f"已生成 {output_path}")
os.startfile(output_path)
