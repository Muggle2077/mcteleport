
# 新用户
execute unless score @s teleport.uid matches ..2147483647 run function teleport:user/new
# 存入历史
execute unless score @s teleport.no_history matches 1 run function teleport:history/new
# 获取uid
execute store result storage teleport:t uid.uid int 1 run scoreboard players get @s teleport.uid
# 从下界返回
execute if dimension minecraft:the_nether run return run function teleport:the_nether/back with storage teleport:t uid
# 前往下界
function teleport:the_nether/go with storage teleport:t uid