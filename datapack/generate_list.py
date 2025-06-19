from pathlib import Path

output_path = Path(".") / "output.mcfunction"

text = "\n".join(
    [
        f'execute if score #c teleport matches {i}.. run tellraw @s ["",{{text:"{i}",color:"gold"}}," ",{{storage:"teleport:t",nbt:"p[-{i}].t",interpret:true}}," ",{{storage:"teleport:t",nbt:"p[-{i}].n",hover_event:{{action:"show_text",value:{{storage:"teleport:t",nbt:"p[-{i}].p[]"}}}}}}," ",{{text:"传",font:"teleport:12",click_event:{{action:"run_command",command:"/function teleport:point/go/{i}"}},hover_event:{{action:"show_text",value:{{translate:"teleport.point.go"}}}}}},{{text:"置",font:"teleport:12",click_event:{{action:"run_command",command:"/function teleport:point/pin/{i}"}},hover_event:{{action:"show_text",value:{{translate:"teleport.point.pin"}}}}}},{{text:"删",font:"teleport:12",click_event:{{action:"run_command",command:"/function teleport:point/delete/{i}"}},hover_event:{{action:"show_text",value:{{translate:"teleport.ui.delete"}}}}}}]'
        for i in range(99, 0, -1)
    ]
)

output_path.write_text(text, encoding="utf-8")

print(f"已生成 {output_path}")