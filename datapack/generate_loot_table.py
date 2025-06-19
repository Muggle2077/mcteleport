from pathlib import Path

loot_table_dir = Path(".") / "data/teleport/loot_table"

item_type = "carrot_on_a_stick"
item_names = ["surface"]

for item_name in item_names:
    loot_table_path = loot_table_dir / f"{item_name}.json"
    if loot_table_path.exists():
        print(f"{loot_table_path} 已存在")
    else:
        text = f"""{{
  "pools": [
    {{
      "rolls": 1,
      "entries": [
        {{
          "type": "minecraft:item",
          "name": "minecraft:{item_type}",
          "functions": [
            {{
              "function": "minecraft:set_components",
              "components": {{
                "minecraft:custom_data": {{
                  "is_teleport": true,
                  "teleport": "{item_name}"
                }},
                "minecraft:item_name": {{
                  "translate": "teleport.{item_name}"
                }},
                "minecraft:item_model": "teleport:{item_name}"
              }}
            }}
          ]
        }}
      ]
    }}
  ]
}}"""
        loot_table_path.write_text(text, encoding="utf-8")
        print(f"已生成 {loot_table_path}")
