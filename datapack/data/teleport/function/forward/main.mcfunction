
# 存入历史
execute unless score @s teleport.no_history matches 1 run function teleport:history/new
# 步数
scoreboard players operation #steps teleport = @s teleport.forward
scoreboard players operation #steps teleport *= #4 teleport
# 向前递归
execute positioned ^ ^ ^0.25 if function teleport:if/through run function teleport:forward/ray
# 声音和消息
function teleport:use/sound_and_message