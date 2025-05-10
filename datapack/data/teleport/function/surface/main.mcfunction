
# 新用户
execute unless score @s teleport.uid matches ..2147483647 run function teleport:user/new
# 存储整数坐标
execute store result score #x teleport run data get storage teleport:t pos[0]
execute store result score #y teleport run data get storage teleport:t pos[1]
execute store result score #z teleport run data get storage teleport:t pos[2]
data modify storage teleport:t translate.translate set from entity @s Dimension
# 存入历史
execute unless score @s teleport.no_history matches 1 run function teleport:history/new_s
# 声音和消息
execute unless score @s teleport.no_sound matches 1 at @s run playsound minecraft:entity.player.teleport player @s
execute unless score @s teleport.no_message matches 1 run title @s actionbar [{nbt:"translate",storage:"teleport:t",interpret:true}," ",{"score":{"name":"#x","objective":"teleport"}},", ",{"score":{"name":"#y","objective":"teleport"}},", ",{"score":{"name":"#z","objective":"teleport"}}]