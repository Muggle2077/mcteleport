# Teleport
Teleport is a Minecraft data pack that adds tools to help you move quickly.

Use command `/function teleport:item` to get all tools.

Hold in hand and right click to use.

## ![](resourcepack/assets/teleport/textures/item/forward.png) Forward teleport

Teleport you to the block that you are looking at.

Stop if [max forward teleport distance](#-teleport-settings) is reached.

## ![](resourcepack/assets/teleport/textures/item/backward.png) Backward teleport

Teleport you along the opposite direction of where you are looking.

Stop if blocked, or [max backward teleport distance](#-teleport-settings) is reached.

## ![](resourcepack/assets/teleport/textures/item/through.png) To the back of the wall

Teleport you to the other side of the wall that you are looking at.

Before entering the wall, stop if [max forward teleport distance](#-teleport-settings) is reached.

## ![](resourcepack/assets/teleport/textures/item/top.png) To the top of the wall

Teleport you to the top of the wall that you are looking at.

Before entering the wall, stop if [max forward teleport distance](#-teleport-settings) is reached.

## ![](resourcepack/assets/teleport/textures/item/surface.png) To the world surface

Teleport you to the world surface (the top of the highest block) where you are.

The same as `execute positioned over world_surface`.

## ![](resourcepack/assets/teleport/textures/item/random.png) Random Teleport

Teleport you Randomly.

Your x and z coordinates will change by a random value whose absolute value is between [min and max random teleport offsets](#-teleport-settings), while your y coordinate remains unchanged.

## ![](resourcepack/assets/teleport/textures/item/the_nether.png) To the Nether

Teleport you to the Nether.

## ![](resourcepack/assets/teleport/textures/item/the_end.png) To the End

Teleport you to the obsidian platform (to 100, 49, 0) in the End.

## ![](resourcepack/assets/teleport/textures/item/world_spawn.png) To the world spawn point

Teleport you to the world spawn point.

The world spawn point is cached. Each time the world spawn point is modified (e.g., via the `/setworldspawn` command), please use the `/reload` command or [go there](#-teleport-settings) to update the cache.

## ![](resourcepack/assets/teleport/textures/item/spawn.png) To my spawn point

Teleport you to your spawn point.

If you don't have a spawn point, teleport you to the world spawn point.

## ![](resourcepack/assets/teleport/textures/item/death.png) Back to death location

Teleport you to your last death location.

## ![](resourcepack/assets/teleport/textures/item/undo.png) Undo

Teleport you to where you last used other teleport tools.

## ![](resourcepack/assets/teleport/textures/item/history.png) Teleport history

Show the teleport history.

Each time when you use teleport tools, before teleporting, your position will be added to the teleport history.

Newly added record appears at the buttom, and has a smaller index.

Click ![](resourcepack/assets/teleport/textures/font/16/clear.png) to clear teleport history.

For each record:

- Click ![](resourcepack/assets/teleport/textures/item/undo.png) to teleport you to the recorded location and delete it and all subsequent records.
- Click ![](resourcepack/assets/teleport/textures/font/16/delete.png) to delete it.

If you don't want it to record teleport history, click ![](resourcepack/assets/teleport/textures/font/16/record_pause.png) to pause. Click ![](resourcepack/assets/teleport/textures/font/16/record_start.png) to restart. You can also change it in [settings](#-teleport-settings).

## ![](resourcepack/assets/teleport/textures/item/add_a_point.png) Add a point

It's a writable book. Write some words and click 'Done', and a teleport point will be added.

Where you are will be the location of the point, What you write will be the name of the point.

## ![](resourcepack/assets/teleport/textures/item/point.png) Teleport points

Show all teleport points you added.

Newly added point appears at the buttom, and has a smaller index.

Click ![](resourcepack/assets/teleport/textures/font/16/clear.png) to delete all points.

For each point:

- Click ![](resourcepack/assets/teleport/textures/font/16/go.png) to teleport you to it.
- Click ![](resourcepack/assets/teleport/textures/font/16/pin.png) to move it to the bottom.
- Click ![](resourcepack/assets/teleport/textures/font/16/delete.png) to delete it.

## ![](resourcepack/assets/teleport/textures/item/chest.png) All teleport tools

It's a written book. You can use all teleport tools in it.

## ![](resourcepack/assets/teleport/textures/item/fly.png) Fly

Right click to ride a cloud. 

- Press keys to start continuously moving.

| Key          | Direction |
| ------------ | --------- |
| W            | Forward   |
| A            | Left      |
| S            | Backward  |
| D            | Right     |
| Space        | Up        |
| Left Control | Down      |

- Right click to stop.

Press Left Shift to dismount.

You can change [flying speed](#-teleport-settings).

## ![](resourcepack/assets/teleport/textures/item/settings.png) Teleport settings

| Settings                                                                                    | Default       |
| ------------------------------------------------------------------------------------------- | ------------- |
| ![](resourcepack/assets/teleport/textures/item/forward.png) Max forward teleport distance   | 32 blocks     |
| ![](resourcepack/assets/teleport/textures/item/backward.png) Max backward teleport distance | 32 blocks     |
| ![](resourcepack/assets/teleport/textures/item/fly.png) Flying speed                        | 16 blocks / s |
| ![](resourcepack/assets/teleport/textures/item/random.png) Min random teleport offset       | 1024 blocks   |
| ![](resourcepack/assets/teleport/textures/item/random.png) Max random teleport offset       | 2048 blocks   |
| ![](resourcepack/assets/teleport/textures/item/history.png) Record teleport history         | true          |
| ![](resourcepack/assets/teleport/textures/font/16/feedback.png) Actionbar messages          | true          |
| ![](resourcepack/assets/teleport/textures/font/16/sounds.png) Sounds                        | true          |

If it's a number, click it and input a new number and press enter to change it.

Click ![](resourcepack/assets/teleport/textures/font/16/refresh.png) to refresh the page to see your changes.

If it's true or false, click it to change it.


| Options                                                                                            |
| -------------------------------------------------------------------------------------------------- |
| ![](resourcepack/assets/teleport/textures/item/world_spawn.png) Update the world spawn point cache |
| ![](resourcepack/assets/teleport/textures/font/16/reset.png) Reset all settings to default         |
| ![](resourcepack/assets/teleport/textures/font/16/refresh.png) Refresh the page                    |