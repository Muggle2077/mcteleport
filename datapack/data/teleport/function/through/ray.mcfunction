scoreboard players remove #steps teleport 1
execute if score #steps teleport matches 1.. positioned ^ ^ ^0.25 if function teleport:if/through run return run function teleport:through/ray
execute positioned ^ ^ ^0.25 unless block ~ ~ ~ #teleport:through run return run function teleport:through/through
tp @s ~ ~ ~