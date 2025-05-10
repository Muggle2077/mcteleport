$data modify storage teleport:u p$(uid) append from storage teleport:u p$(uid)[-$(rid)]
$data remove storage teleport:u p$(uid)[-$(pid)]