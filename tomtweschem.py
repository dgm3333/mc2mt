# Minecraft to Minetest WE schematic MCEdit filter
# by sfan5

displayName = "-> Minetest WE schematic"

#Reference MC: http://media-mcw.cursecdn.com/8/8c/DataValuesBeta.png
#Reference MT:
# https://github.com/minetest/common/blob/master/mods/default/init.lua
# https://github.com/minetest/common/blob/master/mods/wool/init.lua
# https://github.com/minetest/common/blob/master/mods/stairs/init.lua
conversionTable = [
	#blockid blockdata minetest-nodename
	#blockdata -1 means ignore
	#blockdata -2 means copy without change
	#blockdata -3 means copy and convert the mc facedir value to mt facedir
	#blockdata -4 is for stairs to support upside down ones

	(1  , -1, "default:stone"),
	(2  , -1, "default:dirt_with_grass"),
	(3  , -1, "default:dirt"),
	(4  , -1, "default:cobble"),
	(5  ,  3, "default:junglewood"),
	(5  , -1, "default:wood"),
	(6  ,  3, "default:junglesapling"),
	(6  , -1, "default:sapling"),
	(7  , -1, "default:nyancat_rainbow"), # FIXME Bedrock
	(8  , -1, "default:water_flowing"),
	(9  , -1, "default:water_source"),
	(10 , -1, "default:lava_flowing"),
	(11 , -1, "default:lava_source"),
	(12 , -1, "default:sand"),
	(13 , -1, "default:gravel"),
	(14 , -1, "default:stone_with_gold"),
	(15 , -1, "default:stone_with_iron"),
	(16 , -1, "default:stone_with_coal"),
	(17 ,  3, "default:jungletree"),
	(17 , -1, "default:tree"),
	(18 ,  3, "default:jungleleaves"),
	(18 , -1, "default:leaves"),
	(20 , -1, "default:glass"),
	(21 , -1, "default:stone_with_copper"),
	(22 , -1, "default:copperblock"),
	(24 ,  1, "default:sandstonebrick"),
	(24 , -1, "default:sandstone"),
	(31 ,  0, "default:dry_shrub"),
	(31 ,  1, "default:grass_4"),
	(31 ,  2, "default:grass_3"),
	(31 , -1, "default:grass_1"),
	(32 , -1, "default:dry_shrub"),
	(35 ,  0, "wool:white"),
	(35 ,  1, "wool:orange"),
	(35 ,  4, "wool:yellow"),
	(35 ,  5, "wool:green"),
	(35 ,  6, "wool:pink"),
	(35 ,  7, "wool:dark_grey"),
	(35 ,  8, "wool:grey"),
	(35 ,  9, "wool:cyan"),
	(35 , 10, "wool:violet"),
	(35 , 11, "wool:blue"),
	(35 , 12, "wool:brown"),
	(35 , 13, "wool:dark_green"),
	(35 , 14, "wool:red"),
	(35 , 15, "wool:black"),
	(37 , -1, "flowers:dandelion_yellow"),
	(38 , -1, "flowers:rose"),
	(41 , -1, "default:goldblock"),
	(42 , -1, "default:steelblock"),
	(43 ,  1, "default:sandstone"),
	(43 ,  2, "default:wood"),
	(43 ,  3, "default:cobble"),
	(43 ,  4, "default:brick"),
	(43 ,  5, "default:stonebrick"),
	(44 ,  0, "stairs:slab_stone"),
	(44 ,  1, "stairs:slab_sandstone"),
	(44 ,  2, "stairs:slab_wood"),
	(44 ,  3, "stairs:slab_cobble"),
	(44 ,  4, "stairs:slab_brick"),
	(44 ,  5, "stairs:slab_stonebrick"),
	(44 ,  8, "stairs:slab_stoneupside_down"),
	(44 ,  9, "stairs:slab_sandstoneupside_down"),
	(44 , 10, "stairs:slab_woodupside_down"),
	(44 , 11, "stairs:slab_cobbleupside_down"),
	(44 , 12, "stairs:slab_brickupside_down"),
	(44 , 13, "stairs:slab_stonebrickupside_down"),
	(45 , -1, "default:brick"),
	(47 , -1, "default:bookshelf"),
	(48 , -1, "default:mossycobble"),
	(49 , -1, "default:obsidian"),
	(50 , -3, "default:torch"),
	(51 , -1, "fire:basic_flame"),
	(53 , -4, "stairs:stair_wood"),
	(54 , -1, "default:chest"),
	(56 , -1, "default:stone_with_diamond"),
	(57 , -1, "default:diamondblock"),
	(61 , -1, "default:furnace"),
	(62 , -1, "default:furnace_active"),
	(63 , -1, "default:sign_wood"),
	(64 , -1, "doors:door_wood_t_1"),
	(65 , -1, "default:ladder"),
	(66 , -1, "default:rail"),
	(67 , -4, "stairs:stair_cobble"),
	(68 , -3, "default:sign_wood"),
	(71 , -1, "doors:door_steel_t_1"),
	(78 , -1, "default:snow"),
	(79 , -1, "default:ice"),
	(80 , -1, "default:snowblock"),
	(81 , -1, "default:cactus"),
	(82 , -1, "default:clay"),
	(83 , -1, "default:papyrus"),
	(85 , -1, "default:fence_wood"),
	(98 , -1, "default:stonebrick"),
	(108, -4, "stairs:stair_brick"),
	(109, -3, "stairs:stair_stonebrick"),
	(125,  3, "default:junglewood"),
	(125, -1, "default:wood"),
	(126,  3, "stairs:slab_junglewood"),
	(126, -1, "stairs:slab_wood"),
	(128, -4, "stairs:stair_sandstone"),
	(129, -1, "default:stone_with_mese"),
	(133, -1, "default:mese"),
	(134, -4, "stairs:stair_wood"),
	(135, -4, "stairs:stair_wood"),
	(136, -4, "stairs:stair_junglewood"),

	#Mesecons section
	# Reference: https://github.com/Jeija/minetest-mod-mesecons/blob/master/mesecons_alias/init.lua
	(25 , -1, "mesecons_noteblock:noteblock", "mesecons"),
	(29 , -3, "mesecons_pistons:piston_sticky_off", "mesecons"),
	(33 , -3, "mesecons_pistons:piston_normal_off", "mesecons"),
	(55 , -1, "mesecons:wire_00000000_off", "mesecons"),
	(69 , -3, "mesecons_walllever:wall_lever_off", "mesecons"),
	(70 , -1, "mesecons_pressureplates:pressure_plate_stone_off", "mesecons"),
	(72 , -1, "mesecons_pressureplates:pressure_plate_wood_off", "mesecons"),
	(73 , -1, "default:stone_with_mese", "mesecons"),
	(74 , -1, "default:stone_with_mese", "mesecons"),
	(75 , -3, "mesecons_torch:torch_off", "mesecons"),
	(76 , -3, "mesecons_torch:torch_on", "mesecons"),
	(77 , -3, "mesecons_button:button_off", "mesecons"),
	(93 , -3, "mesecons_delayer:delayer_off_1", "mesecons"),
	(94 , -3, "mesecons_delayer:delayer_on_1", "mesecons"),
	(123, -1, "mesecons_lightstone_red_off", "mesecons"),
	(124, -1, "mesecons_lightstone_red_on", "mesecons"),
	(137, -1, "mesecons_commandblock:commandblock_off", "mesecons"),
	(151, -1, "mesecons_solarpanel:solar_panel_off", "mesecons"),
	(152, -1, "default:mese", "mesecons"),
	
	#Nether section
	# Reference: https://github.com/PilzAdam/nether/blob/master/init.lua
	(43 ,  6, "nether:brick", "nether"),
	(87 , -1, "nether:rack", "nether"),
	(88 , -1, "nether:sand", "nether"),
	(89 , -1, "nether:glowstone", "nether"),
	(90 , -3, "nether:portal", "nether"),

	#Riesenpilz Section
	# Reference: https://github.com/HybridDog/riesenpilz/blob/master/init.lua
	(39 , -1, "riesenpilz:brown", "riesenpilz"),
	(40 , -1, "riesenpilz:red", "riesenpilz"),
	(99 , -3, "riesenpilz:head_brown", "riesenpilz"),
	(100, -3, "riesenpilz:head_brown", "riesenpilz"),
]

inputs = (
	("Output filename", "string"),
	("Enabled Mods", "label"),
	("Mesecons", ("False", "True")),
	("Nether", ("False", "True")),
	("Riesenpilz", ("False", "True")),
)

def mc2mtFacedir(blockdata):
	#Minetest
	# x+ = 2
	# x- = 3
	# z+ = 1
	# z- = 0
	#Minecraft
	# x+ = 3
	# x- = 1
	# z+ = 0
	# z- = 2
	tbl = {
		3: 2,
		1: 3,
		0: 1,
		2: 0,
	}
	return tbl.get(blockdata, 0)

def mc2mtstairs(tpl):
	if tpl[1] >= 4:
		return (tpl[0] + "upside_down", mc2mtFacedir(tpl[1] - 4))
	else:
		return (tpl[0], mc2mtFacedir(tpl[1]))


def findConversion(blockid, blockdata, mods):
	if blockid == 0:
		return None
	for cnv in conversionTable:
		if blockid != cnv[0]:
			continue
		if len(cnv) >= 4:
			if mods.get(cnv[3], False) == False:
				continue 
		if cnv[1] == -1:
			return (cnv[2], 0)
		elif cnv[1] == -2:
			return (cnv[2], blockdata)
		elif cnv[1] == -3:
			return (cnv[2], mc2mtFacedir(blockdata))
		elif cnv[1] == -4:
			return mc2mtstairs((cnv[2], blockdata))
		elif cnv[1] != blockdata:
			continue
		return (cnv[2], 0)
	return None

def perform(level, box, options):
	try:
		f = open("../" + options["Output filename"] + ".we", 'w')
	except:
		raise

	origin = (
		box.minx + int((box.maxx - box.minx) / 2),
		box.miny + int((box.maxy - box.miny) / 2),
		box.minz + int((box.maxz - box.minz) / 2),
	)
	
	mods = {}
	for arg in options.keys():
		if options[arg] == "True":
			mods[arg.lower()] = True
	
	for x in xrange(box.minx, box.maxx):
		for z in xrange(box.minz, box.maxz):
			for y in xrange(box.miny, box.maxy):
				c = findConversion(level.blockAt(x, y, z), level.blockDataAt(x, y, z), mods)
				if c == None:
					continue
				calcpos = (x - origin[0], y - origin[1], z - origin[2])
				fmttpl = calcpos + (c[0], level.blockLightAt(x, y, z), c[1])
				f.write("%d %d %d %s %d %d\n" % fmttpl)

	f.close()

