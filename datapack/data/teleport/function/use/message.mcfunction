data modify storage teleport:t translate.translate set from entity @s Dimension
data modify storage teleport:t pos set from entity @s Pos
execute store result score #x teleport run data get storage teleport:t pos[0]
execute store result score #y teleport run data get storage teleport:t pos[1]
execute store result score #z teleport run data get storage teleport:t pos[2]
title @s actionbar [{nbt:"translate",storage:"teleport:t",interpret:true}," ",{"score":{"name":"#x","objective":"teleport"}},", ",{"score":{"name":"#y","objective":"teleport"}},", ",{"score":{"name":"#z","objective":"teleport"}}]