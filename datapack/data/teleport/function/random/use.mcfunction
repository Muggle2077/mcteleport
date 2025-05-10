
# 新用户
execute unless score @s teleport.uid matches ..2147483647 run function teleport:user/new
# 符合条件
execute if score @s teleport.random_min matches 0..59999998 if score @s teleport.random_max matches 0..59999998 if score @s teleport.random_max >= @s teleport.random_min run function teleport:random/main