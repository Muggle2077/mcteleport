import ast
import json
import math
import os
import random
import re
import time
from pathlib import Path

start_time = time.time()

input_dir = Path(".") / "data/teleport/function"
output_path = Path(".") / "output.html"

graph_start = "graph LR"

jspath = "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs"


class RePattern:
    mcfunction = r"\bfunction [a-z0-9_.-]+:([a-z0-9_./-]+)"
    scoreboard = r"\bscore ([^ \n]+) ([^ \n]+)"
    scoreboard_objective = r"\bscoreboard objectives [^ \n]+ ([^ \n]+)"
    scoreboard_player = r"\bscoreboard players [^ \n]+ ([^ \n]+)"
    tag = r"\btag [^ \n]+ [^ \n]+ ([^ \n]+)"
    tags = r"\bTags *: *(\[[^\n]+\])"
    storage = r"\bstorage ([^ \n]+) ([^ \n]+)"


class Color:
    from colors import get_colors

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

    def __init__(self, name: str, children: set[str], comment: str):
        self.name: str = name
        self.comment: str = comment
        self.children: set[str] = children
        self.parents: set[str] = set()

        self.tree: int = None
        self.depth: int = None
        self.level: int = None
        self.need_deepen: bool = False
        self.leaves: int = None

        self.color: int = None

    def __repr__(self):
        return str(
            {
                "name": self.name,
                "color": self.color,
                "comment": self.comment,
                "children": self.children,
            }
        )

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
                    child_level, child_leaves = mcfunctions[child].build_tree(
                        tree=tree, depth=depth + 1
                    )
                    self.level = max(self.level, child_level)
                    self.leaves += child_leaves
                self.level += 1
        elif self.tree == tree:
            return self.level, 1
        elif self.depth < depth:
            self.need_deepen = True
            self.depth = depth
        return self.level, self.leaves

    def deepen(self, tree: int, depth: int):
        if self.tree != tree and self.depth < depth:
            self.tree = tree
            self.depth = depth
            for child in self.children:
                mcfunctions[child].deepen(tree=tree, depth=depth + 1)

    def set_color(self):
        if self.color is None:
            if self.depth == 1:
                self.color = Color.give()
            else:
                min_depth = self.depth
                for parent in self.parents:
                    if mcfunctions[parent].depth < min_depth:
                        min_depth = mcfunctions[parent].depth
                        best_parent = parent
                self.color = mcfunctions[best_parent].set_color()
                for parent in self.parents:
                    if parent != best_parent:
                        mcfunctions[parent].set_color()
        return self.color

    @staticmethod
    def get_comment(text: str):
        if text.startswith("# "):
            newline_pos = text.find("\n")
            if newline_pos == -1:
                return text[2:]
            else:
                return text[2:newline_pos]
        else:
            return None

    @staticmethod
    def should_ignore(name: str):
        return (
            "/" in name
            and (after := name.rsplit("/", 1)[1]).isdigit()
            and after != "99"
        )


class NbtPath:
    def __init__(self, name: str, title: str):
        self.name: str = name
        self.title: str = title
        self.children: set[str] = set()
        self.color: int = None

    def __repr__(self):
        return str(
            {
                "name": self.name,
                "color": self.color,
                "title": self.title,
                "children": self.children,
            }
        )

    def set_color(self, color):
        self.color = color
        for child in self.children:
            nbt_paths[child].set_color(color)

    @staticmethod
    def filter(path):
        return re.sub(r'[()[\]<>{}"-]', "_", path)


mcfunctions: dict[str, Mcfunction] = {}
score_boards: set[str] = set()
score_holders: set[str] = set()
tags: set[str] = set()
storages_set: set[str] = set()
nbt_paths_set: set[str] = set()

# 遍历文件，获取每个函数的 name 和 children
for path in input_dir.rglob(f"*.mcfunction"):
    name = path.relative_to(input_dir).with_suffix("").as_posix()
    if Mcfunction.should_ignore(name):
        continue
    with open(path, mode="r", encoding="utf-8") as mcfunction_file:
        mcfunction_contents = mcfunction_file.read()
        children = set(re.findall(RePattern.mcfunction, mcfunction_contents))
        children = {child for child in children if not Mcfunction.should_ignore(child)}
        mcfunctions[name] = Mcfunction(
            name=name,
            children=children,
            comment=Mcfunction.get_comment(mcfunction_contents),
        )
        result_list = re.findall(RePattern.scoreboard, mcfunction_contents)
        for i in result_list:
            score_boards.add(i[1])
            score_holders.add(i[0])
        result_list = re.findall(RePattern.scoreboard_objective, mcfunction_contents)
        for i in result_list:
            score_boards.add(i)
        result_list = re.findall(RePattern.scoreboard_player, mcfunction_contents)
        for i in result_list:
            score_holders.add(i)
        result_list = re.findall(RePattern.tag, mcfunction_contents)
        for i in result_list:
            tags.add(i)
        result_list = re.findall(RePattern.tags, mcfunction_contents)
        for i in result_list:
            tags |= set(ast.literal_eval(i))
        result_list = re.findall(RePattern.storage, mcfunction_contents)
        for i in result_list:
            storages_set.add(i[0])
            nbt_paths_set.add(i[0] + "." + i[1])

# 创建被调用了但是没有相应文件的函数
new_mcfunctions = {}
for name in mcfunctions:
    for child in mcfunctions[name].children:
        if child not in mcfunctions:
            new_mcfunctions[child] = Mcfunction(name=child, children=set())
mcfunctions.update(new_mcfunctions)

# 获取每个函数的 parents
for name in mcfunctions:
    for child in mcfunctions[name].children:
        mcfunctions[child].parents.add(name)

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
            mcfunctions[child].deepen(tree=tree, depth=mcfunctions[name].depth + 1)
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

for name, mcfunction in mcfunctions.items():
    for child in sorted(mcfunction.children):
        arrows_part.append(f"{name} --> {child}")
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

for path in nbt_paths_set:
    path_parts = re.split(r"(?<=\])\.|\.|(?=\[)", path)
    path_parts = [_ for _ in path_parts if _ != ""]

    current_parts = []
    for part in path_parts:
        current_parts.append(part)
        key = NbtPath.filter(".".join(current_parts))
        parent_key = (
            NbtPath.filter(".".join(current_parts[:-1]))
            if len(current_parts) > 1
            else None
        )
        if key not in nbt_paths:
            nbt_paths[key] = NbtPath(name=key, title=current_parts[-1])
        if parent_key is not None:
            nbt_paths[parent_key].children.add(key)

Color.reset()
for name in storages_set:
    for child in nbt_paths[name].children:
        nbt_paths[child].set_color(Color.give())

nbt_frames_part: list[str] = [
    f"{name}[{json.dumps(nbt_paths[name].title)}]" for name in nbt_paths
]

nbt_frame_styles_part: list[str] = [
    f"style {name} stroke:{Color.get(nbt_paths[name])},stroke-width:2px"
    for name in nbt_paths
    if nbt_paths[name].color is not None
]

nbt_arrows_part: list[str] = []
arrow_styles: list[str] = []
arrow_styles_dict: dict[str, set[int]] = {}
for name, storage_path in nbt_paths.items():
    for child in sorted(storage_path.children):
        nbt_arrows_part.append(f"{name} --> {child}")
        arrow_styles.append(
            Color.get(storage_path) if storage_path.color is not None else None
        )

for arrow_id, style in enumerate(arrow_styles):
    if style is None:
        continue
    if style not in arrow_styles_dict:
        arrow_styles_dict[style] = set()
    arrow_styles_dict[style].add(arrow_id)

nbt_arrow_styles_part = [
    f'linkStyle {",".join(map(str,arrow_styles_dict[style]))} stroke:{style},stroke-width:2px;'
    for style in arrow_styles_dict
]

with output_path.open(mode="w+", encoding="utf-8") as readme_file:
    readme_file.write(
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
{graph_start}
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
{graph_start}
{"\n".join(nbt_frames_part + nbt_arrows_part + nbt_frame_styles_part + nbt_arrow_styles_part)}
  </pre>
</body>"""
    )

print(f"已生成 {output_path}, 用时 {time.time()-start_time} 秒")

os.startfile(output_path)
