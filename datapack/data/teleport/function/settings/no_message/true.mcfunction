
# 设置
scoreboard players reset @s teleport.no_message
# 音效 + 清屏
execute unless score @s teleport.no_sound matches 1 run playsound minecraft:ui.button.click player @s
function teleport:message/clear_chat
# 设置列表
function teleport:settings/show