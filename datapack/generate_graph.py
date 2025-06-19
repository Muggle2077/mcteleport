import ast
import json
import os
import random
import re
from pathlib import Path

input_path = Path(".") / "data/teleport/function"
output_path = Path(".") / "output.html"
color_path = Path(".") / "colors.json"

head_style = "h1, code {color: white; font-family: Consolas;}"
body_style = "background-color: #1F2020"
mermaid_from = "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs"
mermaid_init = {
    "startOnLoad": True,
    "maxEdges": 5000,
    "maxTextSize": 500000,
    "theme": "dark",
    "fontFamily": "Consolas",
    "flowchart": {"useMaxWidth": False},
}


class RePattern:
    mcfunction = re.compile(r"\bfunction [a-z0-9_.-]+:([a-z0-9_./-]+)")
    score_holder_board = re.compile(r"\bscore ([^ \n]+) ([^ \n]+)")
    score_board = re.compile(r"\bscoreboard objectives [^ \n]+ ([^ \n]+)")
    score_holder = re.compile(r"\bscoreboard players [^ \n]+ ([^ \n]+)")
    tag = re.compile(r"\btag [^ \n]+ [^ \n]+ ([^ \n]+)")
    tags = re.compile(r"\bTags *: *(\[[^\n]+\])")
    nbt_path = re.compile(r"\bstorage ([^ \n]+) ([^ \n]+)")
    pathsplit = re.compile(r"(?<=\])\.|\.|(?=\[)")


class Color:
    with color_path.open(mode="r", encoding="utf-8") as f:
        all_colors: list[int] = json.load(f)
    filtered_colors = [
        color
        for color in all_colors
        if (
            (color >> 16) >= 179
            or ((color >> 8) & 0xFF) >= 179
            or (color & 0xFF) >= 179
        )
    ]
    count = len(filtered_colors)

    def __init__(self) -> None:
        self.colors = self.filtered_colors
        self.id = -1
        random.shuffle(self.colors)

    def get(self) -> tuple[int, str]:
        self.id += 1
        return self.id, f"#{self.colors[self.id % self.count]:06x}"


class Base:
    width = 2

    def __init__(self):
        self.color: int | None = None
        self.real_color: str = ""


class Mcfunction(Base):

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name: str = name
        self.comment: str | None = None
        self.children: set[Mcfunction] = set()
        self.parents: set[Mcfunction] = set()

        self.tree: int | None = None
        self.depth: int | None = None
        self.level: int | None = None
        self.need_deepen: bool = False
        self.leaves: int | None = None

    def __repr__(self) -> str:
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
                    assert isinstance(self.level, int)
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

    def deepen(self, tree: int, depth: int) -> None:
        assert self.depth is not None
        if self.tree != tree and self.depth < depth:
            self.tree = tree
            self.depth = depth
            for child in self.children:
                child.deepen(tree=tree, depth=depth + 1)

    def set_color(self, Color: Color):
        if self.color is None:
            if self.depth == 1:
                self.color, self.real_color = Color.get()
            else:
                best_parent = None
                min_depth = self.depth
                for parent in self.parents:
                    assert isinstance(parent.depth, int) and isinstance(min_depth, int)
                    if parent.depth < min_depth:
                        min_depth = parent.depth
                        best_parent = parent
                assert best_parent is not None
                self.color, self.real_color = best_parent.set_color(Color)
                for parent in self.parents:
                    if parent != best_parent:
                        parent.set_color(Color)
        return self.color, self.real_color

    def set_comment(self, text: str) -> None:
        if text.startswith("# "):
            newline_pos = text.find("\n")
            if newline_pos == -1:
                self.comment = text[2:]
            else:
                self.comment = text[2:newline_pos]

    @staticmethod
    def should_ignore(name: str) -> bool:
        return (
            "/" in name
            and (after := name.rsplit("/", 1)[1]).isdigit()
            and after != "99"
        )


class NbtPath(Base):
    max_id = -1

    @classmethod
    def get_id(cls) -> int:
        cls.max_id += 1
        return cls.max_id

    def __init__(self, name: str, title: str) -> None:
        super().__init__()
        self.id = self.get_id()
        self.name: str = name
        self.title: str = title
        self.children: set[NbtPath] = set()

    def __repr__(self) -> str:
        return str({"name": self.name, "children": self.children})

    def set_color(self, color: tuple[int, str]) -> None:
        self.color, self.real_color = color
        for child in self.children:
            child.set_color(color)


class Main:
    def __init__(self) -> None:
        self.mcfunctions: dict[str, Mcfunction] = {}
        self.score_boards: set[str] = set()
        self.score_holders: set[str] = set()
        self.tags: set[str] = set()
        self.nbt_path_strings: dict[str, set[str]] = {}
        self.nbt_paths: dict[str, NbtPath] = {}

        self.get_data(input_path=input_path)
        self.build_mcfunctions_tree()
        self.build_nbtpaths_tree()
        self.set_mcfunctions_colors()
        self.set_nbtpaths_colors()
        self.save_graph(output_path=output_path)
        os.startfile(output_path)

    def get_data(self, input_path: Path) -> None:
        for path in input_path.rglob(f"*.mcfunction"):
            name = path.relative_to(input_path).with_suffix("").as_posix()
            if Mcfunction.should_ignore(name):
                continue
            mcfunction_contents = path.read_text(encoding="utf-8")
            if name not in self.mcfunctions:
                self.mcfunctions[name] = Mcfunction(name=name)
            self.mcfunctions[name].set_comment(mcfunction_contents)
            for child_name in RePattern.mcfunction.findall(mcfunction_contents):
                if Mcfunction.should_ignore(child_name):
                    continue
                if child_name not in self.mcfunctions:
                    self.mcfunctions[child_name] = Mcfunction(name=child_name)
                self.mcfunctions[name].children.add(self.mcfunctions[child_name])

            for holder, board in RePattern.score_holder_board.findall(
                mcfunction_contents
            ):
                self.score_boards.add(board)
                self.score_holders.add(holder)
            self.score_boards.update(RePattern.score_board.findall(mcfunction_contents))
            self.score_holders.update(
                RePattern.score_holder.findall(mcfunction_contents)
            )
            self.tags.update(RePattern.tag.findall(mcfunction_contents))
            for i in RePattern.tags.findall(mcfunction_contents):
                self.tags.update(ast.literal_eval(i))
            for storage, nbtpaths in RePattern.nbt_path.findall(mcfunction_contents):
                if storage not in self.nbt_path_strings:
                    self.nbt_path_strings[storage] = set()
                self.nbt_path_strings[storage].add(nbtpaths)

    def set_nbtpaths_colors(self) -> None:
        c = Color()
        for name in self.nbt_path_strings:
            for nbt_child in self.nbt_paths[name].children:
                nbt_child.set_color(c.get())

    def build_mcfunctions_tree(self) -> None:
        for name in self.mcfunctions:
            for child in self.mcfunctions[name].children:
                child.parents.add(self.mcfunctions[name])

        tree = 0
        for name in self.mcfunctions:
            if self.mcfunctions[name].tree is None:
                self.mcfunctions[name].build_tree(tree=tree)
                tree += 1

        for name in self.mcfunctions:
            if self.mcfunctions[name].need_deepen:
                for child in self.mcfunctions[name].children:
                    d = self.mcfunctions[name].depth
                    assert d is not None
                    child.deepen(tree=tree, depth=d + 1)
                tree += 1

    def set_mcfunctions_colors(self) -> None:
        c = Color()
        for name in self.mcfunctions:
            if self.mcfunctions[name].level == 1:
                self.mcfunctions[name].set_color(c)

    def build_nbtpaths_tree(self) -> None:
        for storage in self.nbt_path_strings:
            self.nbt_paths[storage] = NbtPath(name=storage, title=storage)
            for path in self.nbt_path_strings[storage]:
                path_parts = [part for part in RePattern.pathsplit.split(path) if part]
                key_parts = [storage, path_parts[0]]
                child_name = ".".join(key_parts)
                if child_name not in self.nbt_paths:
                    self.nbt_paths[child_name] = NbtPath(
                        name=child_name, title=key_parts[-1]
                    )
                self.nbt_paths[storage].children.add(self.nbt_paths[child_name])

                for part in path_parts[1:]:
                    key = ".".join(key_parts)
                    key_parts.append(part)
                    value = f"{key}.{part}"
                    if value not in self.nbt_paths:
                        self.nbt_paths[value] = NbtPath(name=value, title=key_parts[-1])
                    self.nbt_paths[key].children.add(self.nbt_paths[value])

    def save_graph(self, output_path: Path) -> None:
        # 备注
        frames_part: list[str] = [
            f"{name}[{json.dumps(f"{name}<hr>{comment}", ensure_ascii=False, indent=2)}]"
            for name in self.mcfunctions
            if (comment := self.mcfunctions[name].comment) is not None
        ]

        # 框的样式
        frame_styles_part: list[str] = [
            f"style {name} stroke:{self.mcfunctions[name].real_color},stroke-width:{self.mcfunctions[name].width}px"
            for name in self.mcfunctions
        ]

        # 箭头
        arrows_part: list[str] = []
        # 每个箭头的样式，包括颜色和宽度
        arrow_styles: list[tuple[str, int]] = []
        # 每种箭头的样式，颜色宽度 -> 箭头id
        arrow_styles_dict: dict[tuple[str, int], set] = {}

        for name, mcfunction in sorted(self.mcfunctions.items()):
            for child_name in sorted(child.name for child in mcfunction.children):
                arrows_part.append(f"{name} --> {child_name}")
                arrow_styles.append((mcfunction.real_color, mcfunction.width))

        for arrow_id, style in enumerate(arrow_styles):
            if style not in arrow_styles_dict:
                arrow_styles_dict[style] = set()
            arrow_styles_dict[style].add(arrow_id)

        arrow_styles_part = [
            f'linkStyle {",".join(map(str,arrow_styles_dict[style]))} stroke:{style[0]},stroke-width:{style[1]}px;'
            for style in arrow_styles_dict
        ]

        nbt_frames_part: list[str] = [
            f"{self.nbt_paths[name].id}[{json.dumps(self.nbt_paths[name].title)}]"
            for name in sorted(self.nbt_paths)
        ]

        nbt_frame_styles_part: list[str] = [
            f"style {self.nbt_paths[name].id} stroke:{self.nbt_paths[name].real_color},stroke-width:2px"
            for name in self.nbt_paths
            if self.nbt_paths[name].color is not None
        ]

        nbt_arrows_part: list[str] = []
        nbt_arrow_styles: list[str | None] = []
        nbt_arrow_styles_dict: dict[str, set[int]] = {}
        for name, nbt_path in sorted(self.nbt_paths.items()):
            for child_name in sorted(child.name for child in nbt_path.children):
                nbt_arrows_part.append(
                    f"{self.nbt_paths[name].id} --> {self.nbt_paths[child_name].id}"
                )
                nbt_arrow_styles.append(
                    nbt_path.real_color if nbt_path.color is not None else None
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

        html_text = f"""<head>
    <style>
        {head_style}
    </style>
</head>
<body style="{body_style}">
<script type="module">
    import mermaid from '{mermaid_from}';
    mermaid.initialize({json.dumps(mermaid_init)});
</script>
<h1>functions</h1>
<pre class="mermaid">
graph LR
{"\n".join(frames_part + arrows_part + frame_styles_part + arrow_styles_part)}
</pre>
<h1>scoreboard objectives</h1>
<pre>
    <code>
{'\n'.join(sorted(self.score_boards))}
    </code>
</pre>
<h1>scoreboard players</h1>
<pre>
    <code>
{'\n'.join(sorted(self.score_holders))}
    </code>
</pre>
<h1>tags</h1>
<pre>
    <code>
{'\n'.join(sorted(self.tags))}
    </code>
</pre>
<h1>storage</h1>
<pre class="mermaid">
graph LR
{"\n".join(nbt_frames_part + nbt_arrows_part + nbt_frame_styles_part + nbt_arrow_styles_part)}
</pre>
</body>"""

        output_path.write_text(html_text, encoding="utf-8")
        print(f"已生成 {output_path}")


if __name__ == "__main__":
    Main()
