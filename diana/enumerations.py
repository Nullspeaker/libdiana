from enum import Enum
from collections import namedtuple

class PacketProvenance(Enum):
	server = 0x01
	client = 0x02

class EliteAbility(Enum):
	stealth = 0x0001
	low_vis = 0x0002
	cloak = 0x0004
	het = 0x0008
	warp = 0x0010
	teleport = 0x0020
	tractor = 0x0040
	drones = 0x0080
	anti_mine = 0x0100
	anti_torp = 0x0200
	shield_drain = 0x0400

class GameType(Enum):
	siege = 0
	single_front = 1
	double_front = 2
	deep_strike = 3
	peacetime = 4
	border_war = 5

class Console(Enum):
	main_screen = 0
	helm = 1
	weapons = 2
	engineering = 3
	science = 4
	comms = 5
	fighter = 6
	data = 7
	observer = 8
	captain_map = 9
	game_master = 10

class ConsoleStatus(Enum):
	available = 0
	yours = 1
	unavailable = 2

class ObjectType(Enum):
	player_vessel = 1
	weapons_console = 2
	engineering_console = 3
	player_ship_upgrade = 4
	other_ship = 5
	base = 6
	mine = 7
	anomaly = 8
	nebula = 10
	torpedo = 11
	blackhole = 12
	asteroid = 13
	mesh = 14
	creature = 15
	drone = 16

class DriveType(Enum):
	warp = 0
	jump = 1

class ShipType(Enum):
	light_cruiser = 0
	scout = 1
	battleship = 2
	missile_cruiser = 3
	dreadnought = 4
	carrier = 5
	mine_layer = 6
	juggernaut = 7
	ximni_light_cruiser = 8
	ximni_scout = 9
	ximni_missile_cruiser = 10
	ximni_battleship = 11
	ximni_carrier = 12
	ximni_dreadnought = 13
	strongbow = 14
	longbow = 15
	brigantine = 16

	tsn_medium_fighter = 100
	tsn_bomber = 101
	tsn_shuttle = 102
	tsn_lr_shuttle = 103

	zim_fighter = 120
	zim_bomber = 121
	zim_shuttle = 122
	zim_lr_shuttle = 123

	avenger = 130
	adventure = 131

ShipSettingsRecord = namedtuple('ShipSettingsRecord', 'drive type name')

class MainView(Enum):
	forward = 0
	port = 1
	starboard = 2
	aft = 3
	tactical = 4
	lrs = 5
	status = 6

class TubeStatus(Enum):
	unloaded = 0
	loaded = 1
	loading = 2
	unloading = 3

class OrdnanceType(Enum):
	missile = 0
	nuke = 1
	mine = 2
	emp = 3

