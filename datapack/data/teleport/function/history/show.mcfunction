
# 获取uid
execute store result storage teleport:t uid.uid int 1 run scoreboard players get @s teleport.uid
# 获取历史记录
function teleport:history/get with storage teleport:t uid

function teleport:history/show_u