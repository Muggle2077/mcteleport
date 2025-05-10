from pathlib import Path

output_dir = Path(".") / "output"

if not output_dir.exists():
    output_dir.mkdir()

for i in range(99, 0, -1):
    with open(output_dir / f"{i}.mcfunction", "w+", encoding="utf-8") as f:
        s = f"""data modify storage teleport:t pin.rid set value {i}
data modify storage teleport:t pin.pid set value {i+1}
function teleport:point/pin"""
        f.write(s)
