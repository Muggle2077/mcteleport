import json
import os
from pathlib import Path

item_dir = Path(".") / "assets/teleport/items"
model_dir = Path(".") / "assets/teleport/models"
texture_dir = Path(".") / "assets/teleport/textures/item"

output_path = Path(".") / "output.md"

item_paths = set(
    path.relative_to(item_dir).with_suffix("").as_posix()
    for path in item_dir.rglob("*.json")
)
model_paths = set(
    path.relative_to(model_dir).with_suffix("").as_posix()
    for path in model_dir.rglob("*.json")
)
texture_paths = set(
    path.relative_to(texture_dir).with_suffix("").as_posix()
    for path in texture_dir.rglob("*.png")
)

both = item_paths & model_paths & texture_paths

item_extra = item_paths - both
model_extra = model_paths - both
texture_extra = texture_paths - both

text = f"""# 物品定义、模型、纹理都有
```json
{json.dumps(sorted(both),indent=2, ensure_ascii=False)}
```
# 多余的物品定义
```json
{json.dumps(sorted(item_extra),indent=2, ensure_ascii=False)}
```
# 多余的模型
```json
{json.dumps(sorted(model_extra),indent=2, ensure_ascii=False)}
```
# 多余的纹理
```json
{json.dumps(sorted(texture_extra),indent=2, ensure_ascii=False)}
```"""

output_path.write_text(text, encoding="utf-8")

print(f"已生成 {output_path}")
os.startfile(output_path)
