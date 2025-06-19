import json
import os
from pathlib import Path

font_dir = Path(".") / "assets/teleport/font"
texture_dir = Path(".") / "assets/teleport/textures"

output_path = Path(".") / "output.md"

invalid_paths: set[Path] = set()
valid_paths: set[Path] = set()

for path in font_dir.rglob(f"*.json"):
    with path.open(mode="r+", encoding="utf-8") as f:
        font_dict = json.load(f)
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

text = f"""# 不存在的路径
```json
{json.dumps(sorted([path.as_posix() for path in invalid_paths]),indent=2, ensure_ascii=False)}
```
# 未被使用的路径
```json
{json.dumps(sorted([path.as_posix() for path in unused_paths]),indent=2, ensure_ascii=False)}
```"""

output_path.write_text(text, encoding="utf-8")

print(f"已生成 {output_path}")
os.startfile(output_path)
