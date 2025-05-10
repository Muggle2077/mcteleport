execute if data entity @s equipment.offhand.components."minecraft:written_book_content".pages[0] run data modify storage teleport:t pr.n set from entity @s equipment.offhand.components."minecraft:written_book_content".pages[0].raw
item replace entity @s weapon.offhand with minecraft:air
loot replace entity @s weapon.offhand 1 loot teleport:add_a_point
function teleport:add_a_point/add