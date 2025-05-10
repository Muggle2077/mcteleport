
# 修改飞行模式
scoreboard players reset @s teleport.fly_mode
# 变大
attribute @s minecraft:scale modifier remove teleport:fly
# 删除坐骑
execute as @e[type=minecraft:area_effect_cloud,tag=teleport.flyer] unless predicate teleport:has_passenger run kill @s
# 音效
stopsound @s player minecraft:item.elytra.flying