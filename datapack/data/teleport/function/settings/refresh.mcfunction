
# 音效
execute unless score @s teleport.no_sound matches 1 run playsound minecraft:ui.button.click master @s ~ ~ ~
# 清屏
function teleport:message/clear_chat
# 设置列表
function teleport:settings/show