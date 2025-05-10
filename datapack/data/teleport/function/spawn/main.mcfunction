data modify storage teleport:t respawn set from entity @s respawn
execute unless data storage teleport:t respawn.dimension run data modify storage teleport:t respawn.dimension set value "minecraft:overworld"
data modify storage teleport:t respawn.x set from storage teleport:t respawn.pos[0]
data modify storage teleport:t respawn.y set from storage teleport:t respawn.pos[1]
data modify storage teleport:t respawn.z set from storage teleport:t respawn.pos[2]
function teleport:spawn/tp with storage teleport:t respawn
# 声音和消息
execute unless score @s teleport.no_sound matches 1 at @s run playsound minecraft:entity.player.teleport player @s
execute unless score @s teleport.no_message matches 1 run function teleport:spawn/message