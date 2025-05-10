
# 新用户
execute unless score @s teleport.uid matches ..2147483647 run function teleport:user/new
# 存入历史
execute unless score @s teleport.no_history matches 1 run function teleport:history/new
# 获取死亡位置
data modify storage teleport:t death_location set from entity @s LastDeathLocation
data modify storage teleport:t death_location.x set from storage teleport:t death_location.pos[0]
data modify storage teleport:t death_location.y set from storage teleport:t death_location.pos[1]
data modify storage teleport:t death_location.z set from storage teleport:t death_location.pos[2]
# 传送
function teleport:death/tp with storage teleport:t death_location
# 声音和消息
execute unless score @s teleport.no_sound matches 1 at @s run playsound minecraft:entity.player.teleport player @s
execute unless score @s teleport.no_message matches 1 run function teleport:death/message