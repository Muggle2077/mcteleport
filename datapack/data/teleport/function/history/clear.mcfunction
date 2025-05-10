execute store result storage teleport:t uid.uid int 1 run scoreboard players get @s teleport.uid
function teleport:history/clear2 with storage teleport:t uid
# 显示
function teleport:history/show
# 声音
execute unless score @s teleport.no_sound matches 1 run playsound minecraft:block.stone.break block @s ~ ~ ~