
# 存入历史
execute unless score @s teleport.no_history matches 1 run function teleport:history/new
# 如果 max = min
function teleport:random/if_same
# 随机传送方向
execute if predicate teleport:half_chance run scoreboard players operation #random_x teleport *= #-1 teleport
execute if predicate teleport:half_chance run scoreboard players operation #random_z teleport *= #-1 teleport
# 获取玩家坐标 x, z
data modify storage teleport:t pos set from entity @s Pos
execute store result score #x teleport run data get storage teleport:t pos[0]
execute store result score #z teleport run data get storage teleport:t pos[2]
# 玩家坐标 += 随机数
scoreboard players operation #x teleport += #random_x teleport
scoreboard players operation #z teleport += #random_z teleport
# 限制坐标范围
scoreboard players operation #x teleport > #pos_min teleport
scoreboard players operation #x teleport < #pos_max teleport
scoreboard players operation #z teleport > #pos_min teleport
scoreboard players operation #z teleport < #pos_max teleport
# 传送玩家
execute store result storage teleport:t xz.x int 1 run scoreboard players get #x teleport
execute store result storage teleport:t xz.z int 1 run scoreboard players get #z teleport
function teleport:random/tp with storage teleport:t xz
# 声音和消息
function teleport:use/sound_and_message