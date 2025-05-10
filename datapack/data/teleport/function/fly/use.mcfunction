
# 新用户
execute unless score @s teleport.uid matches ..2147483647 run function teleport:user/new
# 如果在飞行，则暂停
execute if score @s teleport.fly_mode matches 1..6 run return run function teleport:fly/to_pause
# 如果暂停，则飞行
execute if score @s teleport.fly_mode matches 7 run return run function teleport:fly/to_move
# 不在飞行
execute anchored eyes positioned ^ ^ ^ positioned ~ ~-0.56375 ~ run function teleport:fly/ride