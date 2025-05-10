execute if score @s teleport.seeing matches 1 run function teleport:history/clear_chat
execute store result storage teleport:t uid.uid int 1 run scoreboard players get @s teleport.uid
function teleport:history/new2 with storage teleport:t uid