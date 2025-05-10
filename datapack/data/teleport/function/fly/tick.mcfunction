
# flyer: 0.0, plyer: 0.4625, player head: 0.56375

# as @a at @s run:
# 玩家输入
execute if predicate teleport:move run function teleport:fly/input
scoreboard players operation #fly_mode teleport = @s teleport.fly_mode
scoreboard players operation #steps teleport = @s teleport.fly_speed
# 如果有坐骑
execute anchored eyes positioned ^ ^ ^ on vehicle as @s[tag=teleport.flyer] run return run function teleport:fly/if_move
# 如果没有坐骑
function teleport:fly/unride