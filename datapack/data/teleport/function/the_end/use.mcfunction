
# 新用户
execute unless score @s teleport.uid matches ..2147483647 run function teleport:user/new
# 存入历史
execute unless score @s teleport.no_history matches 1 run function teleport:history/new
# 传送
execute in minecraft:the_end run tp @s 100 49 0
# 声音和消息
function teleport:use/sound_and_message