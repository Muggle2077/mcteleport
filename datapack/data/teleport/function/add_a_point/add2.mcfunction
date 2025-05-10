data modify storage teleport:t pr.d set from entity @s Dimension
data modify storage teleport:t pr.t.translate set from storage teleport:t pr.d
data modify storage teleport:t pos set from entity @s Pos
data modify storage teleport:t pr.x set from storage teleport:t pos[0]
data modify storage teleport:t pr.y set from storage teleport:t pos[1]
data modify storage teleport:t pr.z set from storage teleport:t pos[2]
execute store result storage teleport:t pr.p[0] int 1 run data get storage teleport:t pos[0]
execute store result storage teleport:t pr.p[1] int 1 run data get storage teleport:t pos[1]
execute store result storage teleport:t pr.p[2] int 1 run data get storage teleport:t pos[2]
$data modify storage teleport:u p$(uid) append from storage teleport:t pr