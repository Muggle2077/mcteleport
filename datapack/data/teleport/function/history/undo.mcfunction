execute store result storage teleport:t uid.uid int 1 run scoreboard players get @s teleport.uid
function teleport:history/undo2 with storage teleport:t uid
# 显示
function teleport:history/show_u
# 声音和消息
execute unless score @s teleport.no_sound matches 1 at @s run playsound minecraft:entity.player.teleport player @s
execute unless score @s teleport.no_message matches 1 run title @s actionbar [{nbt:"hr.t",storage:"teleport:t",interpret:true}," ",{nbt:"hr.p[]",storage:"teleport:t"}]