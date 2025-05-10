execute if score @s teleport.random_max > @s teleport.random_min run return run function teleport:random/offset
scoreboard players operation #random_x teleport = @s teleport.random_min
scoreboard players operation #random_z teleport = @s teleport.random_min