execute if score @s teleport.fly_mode matches 7 unless score @s teleport.no_sound matches 1 run playsound minecraft:item.elytra.flying player @s ~ ~ ~ 0.2
execute if predicate teleport:forward run return run function teleport:fly/to_forward
execute if predicate teleport:backward run return run function teleport:fly/to_backward
execute if predicate teleport:left run return run function teleport:fly/to_left
execute if predicate teleport:right run return run function teleport:fly/to_right
execute if predicate teleport:jump run return run function teleport:fly/to_up
function teleport:fly/to_down