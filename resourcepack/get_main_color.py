import os
from pathlib import Path

from colorthief import ColorThief  # type: ignore
from PIL import Image

input_path = Path(".") / "assets/teleport/textures/item/chest.png"
output_path = Path(".") / "output.png"

thief = ColorThief(input_path)
palette = thief.get_palette()

color_image = Image.new("RGB", (len(palette), 1))
color_image.putdata(palette)
color_image.save(output_path)

print(f"主要颜色 {palette}\n已生成 {output_path}")
os.startfile(output_path)
