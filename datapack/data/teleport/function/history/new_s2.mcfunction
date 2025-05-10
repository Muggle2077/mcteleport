data modify storage teleport:t hr.d set from storage teleport:t translate.translate
data modify storage teleport:t hr.t.translate set from storage teleport:t hr.d
data modify storage teleport:t hr.x set from storage teleport:t pos[0]
data modify storage teleport:t hr.y set from storage teleport:t pos[1]
data modify storage teleport:t hr.z set from storage teleport:t pos[2]
data modify storage teleport:t hr.p set from storage teleport:t pos_int
$data modify storage teleport:u h$(uid) append from storage teleport:t hr