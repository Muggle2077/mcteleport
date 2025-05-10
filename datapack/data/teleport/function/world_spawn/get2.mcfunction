data modify storage teleport:t pos set from entity @s Pos
kill @s
execute store result storage teleport:s world_spawn.x int 1 run data get storage teleport:t pos[0]
execute store result storage teleport:s world_spawn.y int 1 run data get storage teleport:t pos[1]
execute store result storage teleport:s world_spawn.z int 1 run data get storage teleport:t pos[2]