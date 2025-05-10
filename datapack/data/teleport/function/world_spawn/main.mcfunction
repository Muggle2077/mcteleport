function teleport:world_spawn/tp with storage teleport:s world_spawn
# 声音和消息
execute unless score @s teleport.no_sound matches 1 at @s run playsound minecraft:entity.player.teleport player @s
execute unless score @s teleport.no_message matches 1 run title @s actionbar [{translate:"minecraft:overworld"}," ",{nbt:"world_spawn.x",storage:"teleport:s"},", ",{nbt:"world_spawn.y",storage:"teleport:s"},", ",{nbt:"world_spawn.z",storage:"teleport:s"}]