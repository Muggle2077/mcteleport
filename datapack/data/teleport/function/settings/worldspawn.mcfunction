schedule function teleport:world_spawn/get 1t
# 告知玩家
title @s actionbar {"translate":"teleport.generic.worldspawn"}
execute unless score @s teleport.no_sound matches 1 run playsound minecraft:ui.button.click player @s