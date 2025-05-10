
# 新用户
execute unless score @s teleport.uid matches ..2147483647 run function teleport:user/new
# 符合条件
execute if score @s teleport.backward matches 1.. anchored eyes positioned ^ ^ ^ if function teleport:if/through run function teleport:backward/main