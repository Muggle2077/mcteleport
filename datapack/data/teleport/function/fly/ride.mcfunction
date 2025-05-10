
# 修改飞行模式
scoreboard players set @s teleport.fly_mode 7
# 变小
attribute @s minecraft:scale modifier add teleport:fly -1000 add_value
# 召唤坐骑
summon minecraft:area_effect_cloud ~ ~ ~ {Tags:['teleport.flyer'],Radius:0.0d}
# 骑乘
ride @s mount @n[type=minecraft:area_effect_cloud,tag=teleport.flyer,distance=..0.01]
# 声音和消息
execute unless score @s teleport.no_sound matches 1 at @s run playsound minecraft:item.armor.equip_elytra player @s
execute unless score @s teleport.no_message matches 1 run title @s actionbar [{translate:"teleport.fly.control",with:[{keybind:"key.forward"},{keybind:"key.left"},{keybind:"key.back"},{keybind:"key.right"},{keybind:"key.jump"},{keybind:"key.sprint"},{keybind:"key.use"},{keybind:"key.sneak"}]}]