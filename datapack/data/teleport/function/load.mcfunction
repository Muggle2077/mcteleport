scoreboard objectives add teleport dummy
scoreboard players set #4 teleport 4
scoreboard players set #-1 teleport -1
scoreboard players set #pos_min teleport -30000000
scoreboard players set #pos_max teleport 29999999

scoreboard objectives add teleport.use minecraft.used:minecraft.carrot_on_a_stick
scoreboard objectives add teleport.uid dummy

scoreboard objectives add teleport.forward dummy
scoreboard objectives add teleport.backward dummy
scoreboard objectives add teleport.random_min dummy
scoreboard objectives add teleport.random_max dummy

scoreboard objectives add teleport.fly_mode dummy
scoreboard objectives add teleport.fly_speed dummy

scoreboard objectives add teleport.no_sound dummy
scoreboard objectives add teleport.no_message dummy
scoreboard objectives add teleport.no_history dummy

scoreboard objectives add teleport.seeing dummy

data modify storage teleport:t hr.p set value [0,0,0]
data modify storage teleport:t pr.p set value [0,0,0]
data modify storage teleport:t pos_int set value [0,0,0]
data modify storage teleport:t finder set value {uid:-1,rid:-1}

schedule function teleport:world_spawn/get 1t