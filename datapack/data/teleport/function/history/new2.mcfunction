data modify storage teleport:t hr.d set from entity @s Dimension
data modify storage teleport:t hr.t.translate set from storage teleport:t hr.d
data modify storage teleport:t pos set from entity @s Pos
data modify storage teleport:t hr.x set from storage teleport:t pos[0]
data modify storage teleport:t hr.y set from storage teleport:t pos[1]
data modify storage teleport:t hr.z set from storage teleport:t pos[2]
execute store result storage teleport:t hr.p[0] int 1 run data get storage teleport:t pos[0]
execute store result storage teleport:t hr.p[1] int 1 run data get storage teleport:t pos[1]
execute store result storage teleport:t hr.p[2] int 1 run data get storage teleport:t pos[2]
$data modify storage teleport:u h$(uid) append from storage teleport:t hr