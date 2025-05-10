
# 新用户
execute unless score @s teleport.uid matches ..2147483647 run function teleport:user/new

execute store result storage teleport:t uid.uid int 1 run scoreboard players get @s teleport.uid
function teleport:add_a_point/add2 with storage teleport:t uid

execute if score @s teleport.seeing matches 2 run return run function teleport:add_a_point/show_point
execute unless score @s teleport.no_message matches 1 run title @s actionbar [{storage:"teleport:t",nbt:"pr.t",interpret:true}," ",{storage:"teleport:t",nbt:"pr.n"}]