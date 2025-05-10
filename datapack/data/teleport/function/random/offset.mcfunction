
# 获取随机数范围
execute store result storage teleport:t random.min int 1 run scoreboard players get @s teleport.random_min
execute store result storage teleport:t random.max int 1 run scoreboard players get @s teleport.random_max
# 生成随机数 random_x, random_z
function teleport:random/x with storage teleport:t random
function teleport:random/z with storage teleport:t random