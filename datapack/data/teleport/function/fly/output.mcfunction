execute if score #fly_mode teleport matches 1 run return run function teleport:fly/forward
execute if score #fly_mode teleport matches 2 facing ^ ^ ^-1 run return run function teleport:fly/forward
execute if score #fly_mode teleport matches 3 rotated ~-90 0 run return run function teleport:fly/forward
execute if score #fly_mode teleport matches 4 rotated ~90 0 run return run function teleport:fly/forward
execute if score #fly_mode teleport matches 5 facing ~ ~1 ~ run return run function teleport:fly/forward
execute facing ~ ~-1 ~ run function teleport:fly/forward