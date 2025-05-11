import ast
import json
import math
import os
import random
import re
import time
from pathlib import Path
from colors import get_colors

start_time = time.perf_counter_ns()

input_dir = Path(".") / "data/teleport/function"
output_path = Path(".") / "output.html"

jspath = "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs"


class RePattern:
    mcfunction = re.compile(r"\bfunction [a-z0-9_.-]+:([a-z0-9_./-]+)")
    score_holder_board = re.compile(r"\bscore ([^ \n]+) ([^ \n]+)")
    score_board = re.compile(r"\bscoreboard objectives [^ \n]+ ([^ \n]+)")
    score_holder = re.compile(r"\bscoreboard players [^ \n]+ ([^ \n]+)")
    tag = re.compile(r"\btag [^ \n]+ [^ \n]+ ([^ \n]+)")
    tags = re.compile(r"\bTags *: *(\[[^\n]+\])")
    storage = re.compile(r"\bstorage ([^ \n]+) ([^ \n]+)")
    pathsplit = re.compile(r"(?<=\])\.|\.|(?=\[)")


class Color:

    colors = get_colors(lambda v: v >= 0.7)
    count = len(colors)

    @classmethod
    def reset(color):
        color.id = -1
        random.shuffle(color.colors)

    @classmethod
    def give(color):
        color.id += 1
        return color.id

    @classmethod
    def get(color, obj):
        return f"#{color.colors[obj.color % color.count]:06x}"


class Width:
    base = 1
    scale = 1 / 3

    @classmethod
    def get(width, obj):
        return math.ceil(obj.level * width.scale) + width.base


class Mcfunction:

    def __init__(self, name: str):
        self.name: str = name
        self.comment: str | None = None
        self.children: set[Mcfunction] = set()
        self.parents: set[Mcfunction] = set()

        self.tree: int | None = None
        self.depth: int | None = None
        self.level: int | None = None
        self.need_deepen: bool = False
        self.leaves: int | None = None

        self.color: int | None = None

    def __repr__(self):
        return str({"name": self.name, "children": self.children})

    def build_tree(self, tree: int, depth: int = 1):
        if self.tree is None:
            self.tree = tree
            self.depth = depth
            if self.children == set():
                self.level = 1
                self.leaves = 1
            else:
                self.level = 0
                self.leaves = 0
                for child in self.children:
                    child_level, child_leaves = child.build_tree(
                        tree=tree, depth=depth + 1
                    )
                    self.level = max(self.level, child_level)
                    self.leaves += child_leaves
                assert self.level is not None
                self.level += 1
        elif self.tree == tree:
            return self.level, 1
        else:
            assert self.depth is not None
            if self.depth < depth:
                self.need_deepen = True
                self.depth = depth
        return self.level, self.leaves

    def deepen(self, tree: int, depth: int):
        assert self.depth is not None
        if self.tree != tree and self.depth < depth:
            self.tree = tree
            self.depth = depth
            for child in self.children:
                child.deepen(tree=tree, depth=depth + 1)

    def set_color(self):
        if self.color is None:
            if self.depth == 1:
                self.color = Color.give()
            else:
                min_depth = self.depth
                for parent in self.parents:
                    if parent.depth < min_depth:
                        min_depth = parent.depth
                        best_parent = parent
                self.color = best_parent.set_color()
                for parent in self.parents:
                    if parent != best_parent:
                        parent.set_color()
        return self.color

    def set_comment(self, text: str):
        if text.startswith("# "):
            newline_pos = text.find("\n")
            if newline_pos == -1:
                self.comment = text[2:]
            else:
                self.comment = text[2:newline_pos]

    @staticmethod
    def should_ignore(name: str):
        return (
            "/" in name
            and (after := name.rsplit("/", 1)[1]).isdigit()
            and after != "99"
        )


class NbtPath:
    max_id = -1

    @classmethod
    def give_id(cls):
        cls.max_id += 1
        return cls.max_id

    def __init__(self, name: str, title: str):
        self.id = self.give_id()
        self.name: str = name
        self.title: str = title
        self.children: set[NbtPath] = set()
        self.color: int | None = None

    def __repr__(self):
        return str({"name": self.name, "children": self.children})

    def set_color(self, color):
        self.color = color
        for child in self.children:
            child.set_color(color)


mcfunctions: dict[str, Mcfunction] = {}
score_boards: set[str] = set()
score_holders: set[str] = set()
tags: set[str] = set()
nbt_paths_dict: dict[str, set[str]] = {}

# 遍历文件，获取每个函数的 name 和 children
for path in input_dir.rglob(f"*.mcfunction"):
    name = path.relative_to(input_dir).with_suffix("").as_posix()
    if Mcfunction.should_ignore(name):
        continue
    with open(path, mode="r", encoding="utf-8") as f:
        mcfunction_contents = f.read()
    if name not in mcfunctions:
        mcfunctions[name] = Mcfunction(name=name)
    mcfunctions[name].set_comment(mcfunction_contents)
    for child_name in RePattern.mcfunction.findall(mcfunction_contents):
        if Mcfunction.should_ignore(child_name):
            continue
        if child_name not in mcfunctions:
            mcfunctions[child_name] = Mcfunction(name=child_name)
        mcfunctions[name].children.add(mcfunctions[child_name])

    for holder, board in RePattern.score_holder_board.findall(mcfunction_contents):
        score_boards.add(board)
        score_holders.add(holder)
    score_boards.update(RePattern.score_board.findall(mcfunction_contents))
    score_holders.update(RePattern.score_holder.findall(mcfunction_contents))
    tags.update(RePattern.tag.findall(mcfunction_contents))
    for i in RePattern.tags.findall(mcfunction_contents):
        tags.update(ast.literal_eval(i))
    for storage, nbtpaths in RePattern.storage.findall(mcfunction_contents):
        if storage not in nbt_paths_dict:
            nbt_paths_dict[storage] = set()
        nbt_paths_dict[storage].add(nbtpaths)

# 获取每个函数的 parents
for name in mcfunctions:
    for child in mcfunctions[name].children:
        child.parents.add(mcfunctions[name])

# 生成树
tree = 0
for name in mcfunctions:
    if mcfunctions[name].tree is None:
        mcfunctions[name].build_tree(tree=tree)
        tree += 1

# 深度递归树
for name in mcfunctions:
    if mcfunctions[name].need_deepen:
        for child in mcfunctions[name].children:
            d = mcfunctions[name].depth
            assert d is not None
            child.deepen(tree=tree, depth=d + 1)
        tree += 1

# 设置颜色
Color.reset()
for name in mcfunctions:
    if mcfunctions[name].level == 1:
        mcfunctions[name].set_color()

# 备注
frames_part: list[str] = [
    f"{name}[{json.dumps(f"{name}<hr>{comment}", ensure_ascii=False, indent=2)}]"
    for name in mcfunctions
    if (comment := mcfunctions[name].comment) is not None
]

# 框的样式
frame_styles_part: list[str] = [
    f"style {name} stroke:{Color.get(mcfunctions[name])},stroke-width:{Width.get(mcfunctions[name])}px"
    for name in mcfunctions
]

# 箭头
arrows_part: list[str] = []
# 每个箭头的样式，包括颜色和宽度
arrow_styles: list[tuple[str, int]] = []
# 每种箭头的样式，颜色宽度 -> 箭头id
arrow_styles_dict: dict[tuple[str, int], set] = {}

for name, mcfunction in sorted(mcfunctions.items()):
    for child_name in sorted(child.name for child in mcfunction.children):
        arrows_part.append(f"{name} --> {child_name}")
        arrow_styles.append((Color.get(mcfunction), Width.get(mcfunction)))

for arrow_id, style in enumerate(arrow_styles):
    if style not in arrow_styles_dict:
        arrow_styles_dict[style] = set()
    arrow_styles_dict[style].add(arrow_id)

arrow_styles_part = [
    f'linkStyle {",".join(map(str,arrow_styles_dict[style]))} stroke:{style[0]},stroke-width:{style[1]}px;'
    for style in arrow_styles_dict
]

nbt_paths: dict[str, NbtPath] = {}

for storage in nbt_paths_dict:
    nbt_paths[storage] = NbtPath(name=storage, title=storage)
    for p in nbt_paths_dict[storage]:
        path_parts = [part for part in RePattern.pathsplit.split(p) if part]
        key_parts = [storage, path_parts[0]]
        child_name = ".".join(key_parts)
        if child_name not in nbt_paths:
            nbt_paths[child_name] = NbtPath(
                name=child_name, title=key_parts[-1]
            )
        nbt_paths[storage].children.add(nbt_paths[child_name])

        for part in path_parts[1:]:
            key = ".".join(key_parts)
            key_parts.append(part)
            value = f"{key}.{part}"
            if value not in nbt_paths:
                nbt_paths[value] = NbtPath(name=value, title=key_parts[-1])
            nbt_paths[key].children.add(nbt_paths[value])

Color.reset()
for name in nbt_paths_dict:
    for nbt_child in nbt_paths[name].children:
        nbt_child.set_color(Color.give())

nbt_frames_part: list[str] = [
    f"{nbt_paths[name].id}[{json.dumps(nbt_paths[name].title)}]"
    for name in sorted(nbt_paths)
]

nbt_frame_styles_part: list[str] = [
    f"style {nbt_paths[name].id} stroke:{Color.get(nbt_paths[name])},stroke-width:2px"
    for name in nbt_paths
    if nbt_paths[name].color is not None
]

nbt_arrows_part: list[str] = []
nbt_arrow_styles: list[str | None] = []
nbt_arrow_styles_dict: dict[str, set[int]] = {}
for name, nbt_path in sorted(nbt_paths.items()):
    for child_name in sorted(child.name for child in nbt_path.children):
        nbt_arrows_part.append(f"{nbt_paths[name].id} --> {nbt_paths[child_name].id}")
        nbt_arrow_styles.append(
            Color.get(nbt_path) if nbt_path.color is not None else None
        )

for arrow_id, nbt_style in enumerate(nbt_arrow_styles):
    if nbt_style is None:
        continue
    if nbt_style not in nbt_arrow_styles_dict:
        nbt_arrow_styles_dict[nbt_style] = set()
    nbt_arrow_styles_dict[nbt_style].add(arrow_id)

nbt_arrow_styles_part = [
    f'linkStyle {",".join(map(str,nbt_arrow_styles_dict[style]))} stroke:{style},stroke-width:2px;'
    for style in nbt_arrow_styles_dict
]

with output_path.open(mode="w+", encoding="utf-8") as f:
    f.write(
        f"""<head>
  <style>
    h1, code {{
      color: white;
      font-family: Consolas;
    }}
  </style>
</head>
<body style="background-color: #1F2020">
  <script type="module">
    import mermaid from '{jspath}';
    mermaid.initialize({{ startOnLoad: true, maxEdges: 5000, maxTextSize: 500000, theme:'dark',fontFamily:'Consolas',flowchart: {{useMaxWidth:false}} }});
  </script>
  <h1>functions</h1>
  <pre class="mermaid">
graph LR
{"\n".join(frames_part + arrows_part + frame_styles_part + arrow_styles_part)}
  </pre>
  <h1>scoreboard objectives</h1>
  <pre>
    <code>
{'\n'.join(sorted(score_boards))}
    </code>
  </pre>
  <h1>scoreboard players</h1>
  <pre>
    <code>
{'\n'.join(sorted(score_holders))}
    </code>
  </pre>
  <h1>tags</h1>
  <pre>
    <code>
{'\n'.join(sorted(tags))}
    </code>
  </pre>
  <h1>storage</h1>
  <pre class="mermaid">
graph LR
{"\n".join(nbt_frames_part + nbt_arrows_part + nbt_frame_styles_part + nbt_arrow_styles_part)}
  </pre>
</body>"""
    )

print(f"已生成 {output_path}, 用时 {(time.perf_counter_ns() - start_time) * 1e-9} 秒")

os.startfile(output_path)
