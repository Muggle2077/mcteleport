$execute unless data storage teleport:u h$(uid)[0] run return fail
$data modify storage teleport:t hr set from storage teleport:u h$(uid)[-1]
function teleport:undo/tp with storage teleport:t hr
$data remove storage teleport:u h$(uid)[-1]
# 声音和消息
execute unless score @s teleport.no_sound matches 1 at @s run playsound minecraft:entity.player.teleport player @s
execute unless score @s teleport.no_message matches 1 run title @s actionbar [{nbt:"hr.t",storage:"teleport:t",interpret:true}," ",{nbt:"hr.p[]",storage:"teleport:t"}]