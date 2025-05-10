
# 新用户
execute unless score @s teleport.uid matches ..2147483647 run function teleport:user/new
scoreboard players set @s teleport.seeing 1
# 显示
function teleport:history/show
# 声音
execute unless score @s teleport.no_sound matches 1 run playsound minecraft:item.book.page_turn master @s ~ ~ ~ 2.0