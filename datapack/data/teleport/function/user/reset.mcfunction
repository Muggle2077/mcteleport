function teleport:user/reset_score
execute store result storage teleport:t uid.uid int 1 run scoreboard players get @s teleport.uid
function teleport:user/reset_storage with storage teleport:t uid