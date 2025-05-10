
# 新用户
execute unless score @s teleport.uid matches ..2147483647 run function teleport:user/new
# 卡在墙中
execute anchored eyes positioned ^ ^ ^ unless block ~ ~ ~ #teleport:through run return run function teleport:through/main2
# 符合条件
execute if score @s teleport.forward matches 1.. anchored eyes positioned ^ ^ ^ if function teleport:if/through run function teleport:through/main