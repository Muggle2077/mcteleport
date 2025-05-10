scoreboard objectives remove teleport
# holder: #steps #max_uid #random_x #random_z #x #y #z #fly_mode #c #success

scoreboard objectives remove teleport.use
scoreboard objectives remove teleport.uid

scoreboard objectives remove teleport.forward
scoreboard objectives remove teleport.backward
scoreboard objectives remove teleport.random_min
scoreboard objectives remove teleport.random_max

scoreboard objectives remove teleport.fly_mode
scoreboard objectives remove teleport.fly_speed

scoreboard objectives remove teleport.no_sound
scoreboard objectives remove teleport.no_message
scoreboard objectives remove teleport.no_history

scoreboard objectives remove teleport.seeing

data remove storage teleport:s world_spawn

# id:{id:"forward"} 一个传送工具的id
data remove storage teleport:t id
# uid:{uid:1} 一名玩家的uid
data remove storage teleport:t uid
# random:{min:1,max:2} 随机数范围
data remove storage teleport:t random
# xz:{x:1,y:2} x和z坐标
data remove storage teleport:t xz
# death_location:{dimension:"minecraft:overworld",x:1,y:2,z:3}
data remove storage teleport:t death_location
data remove storage teleport:t respawn
# hr:{...} 一名玩家的一条历史
data remove storage teleport:t hr
# h:[{...},{...},{...)] 一名玩家的所有历史
data remove storage teleport:t h
# pr:{...} 一名玩家的一条传送点
data remove storage teleport:t pr
# p:[{...},{...},{...)] 一名玩家的所有传送点
data remove storage teleport:t p
# translate:{translate:"minecraft:overworld"} 显示翻译
data remove storage teleport:t translate
# dimension:{dimension:"minecraft:overworld"} 一个维度
data remove storage teleport:t dimension

data remove storage teleport:t finder
data remove storage teleport:t pin
data remove storage teleport:t text_no_sound
data remove storage teleport:t text_no_message
data remove storage teleport:t text_no_history

# pos:[0.0d,0.0d,0.0d] 坐标
data remove storage teleport:t pos
# pos_int:[0,0,0] 整型坐标
data remove storage teleport:t pos_int

clear @a *[minecraft:custom_data~{is_teleport:true}]
execute as @e[type=minecraft:item] if items entity @s container.0 *[minecraft:custom_data~{is_teleport:true}] run kill @s
kill @e[type=minecraft:area_effect_cloud,tag=teleport.flyer]

function teleport:message/clear_chat