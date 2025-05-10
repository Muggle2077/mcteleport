
# 新用户
execute unless score @s teleport.uid matches ..2147483647 run function teleport:user/new
# 存入历史
execute unless score @s teleport.no_history matches 1 run function teleport:history/new
# 有重生点
execute if data entity @s respawn run return run function teleport:spawn/main
# 没有重生点
function teleport:world_spawn/main