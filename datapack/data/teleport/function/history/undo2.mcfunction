$data modify storage teleport:t h set from storage teleport:u h$(uid)
execute if score #rid teleport matches 1.. run function teleport:history/undo_l
data modify storage teleport:t hr set from storage teleport:t h[-1]
data remove storage teleport:t h[-1]
function teleport:undo/tp with storage teleport:t hr
$data modify storage teleport:u h$(uid) set from storage teleport:t h