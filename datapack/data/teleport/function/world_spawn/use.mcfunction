
# 新用户
execute unless score @s teleport.uid matches ..2147483647 run function teleport:user/new
# 存入历史
execute unless score @s teleport.no_history matches 1 run function teleport:history/new
# 回到出生点
function teleport:world_spawn/main