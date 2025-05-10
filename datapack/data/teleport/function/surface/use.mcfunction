
# 比对传送前后坐标
data modify storage teleport:t pos set from entity @s Pos
execute positioned over world_surface run tp @s ~ ~ ~
execute store success score #success teleport run data modify storage teleport:t pos set from entity @s Pos
# 坐标有变化
execute if score #success teleport matches 1 run function teleport:surface/main