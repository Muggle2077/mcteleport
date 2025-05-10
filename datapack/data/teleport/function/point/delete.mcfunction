execute store result storage teleport:t finder.uid int 1 run scoreboard players get @s teleport.uid
function teleport:point/delete2 with storage teleport:t finder
# 显示
function teleport:point/show
# 声音
execute unless score @s teleport.no_sound matches 1 run playsound minecraft:block.stone.break block @s ~ ~ ~