
# 新用户
execute unless score @s teleport.uid matches ..2147483647 run function teleport:user/new
# 音效
execute unless score @s teleport.no_sound matches 1 run playsound minecraft:item.book.page_turn player @s
# 清屏
scoreboard players reset @s teleport.seeing
function teleport:message/clear_chat
# 设置列表
function teleport:settings/show