data remove storage teleport:t h[-1]
scoreboard players remove #rid teleport 1
execute if score #rid teleport matches 1.. run function teleport:history/undo_l