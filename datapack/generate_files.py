from pathlib import Path

output_dir = Path(".") / "output"

if not output_dir.exists():
    output_dir.mkdir()

for i in range(99, 0, -1):
    text = f"""data modify storage teleport:t pin.rid set value {i}
data modify storage teleport:t pin.pid set value {i+1}
function teleport:point/pin"""
    (output_dir / f"{i}.mcfunction").write_text(text, encoding="utf-8")

print(f"已生成 {output_dir}/")
