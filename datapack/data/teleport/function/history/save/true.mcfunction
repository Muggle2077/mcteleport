scoreboard players reset @s teleport.no_history
# 显示
function teleport:history/show
# 声音
execute unless score @s teleport.no_sound matches 1 run playsound minecraft:ui.button.click master @s ~ ~ ~