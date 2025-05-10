scoreboard players reset @s teleport.use
execute if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{is_teleport:true}] run function teleport:use/mainhand
execute if items entity @s weapon.offhand minecraft:carrot_on_a_stick[minecraft:custom_data~{is_teleport:true}] run function teleport:use/offhand