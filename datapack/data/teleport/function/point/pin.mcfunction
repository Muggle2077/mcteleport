execute store result storage teleport:t pin.uid int 1 run scoreboard players get @s teleport.uid
function teleport:point/pin2 with storage teleport:t pin
# 显示
function teleport:point/show
# 声音
execute unless score @s teleport.no_sound matches 1 run playsound minecraft:ui.button.click master @s ~ ~ ~