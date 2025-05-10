execute as @a[scores={teleport.use=1..}] at @s run function teleport:use/carrot
execute as @a[scores={teleport.fly_mode=1..}] at @s run function teleport:fly/tick
execute as @a if items entity @s weapon.* #teleport:books[minecraft:custom_data~{teleport:'add_a_point'}] run function teleport:add_a_point/use