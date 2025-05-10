execute unless score @s teleport.no_history matches 1 run function teleport:history/new
execute store result storage teleport:t finder.uid int 1 run scoreboard players get @s teleport.uid
function teleport:point/go2 with storage teleport:t finder
function teleport:undo/tp with storage teleport:t pr
# 声音和消息
execute unless score @s teleport.no_sound matches 1 at @s run playsound minecraft:entity.player.teleport player @s
execute unless score @s teleport.no_message matches 1 run title @s actionbar [{nbt:"pr.t",storage:"teleport:t",interpret:true}," ",{nbt:"pr.p[]",storage:"teleport:t"}]