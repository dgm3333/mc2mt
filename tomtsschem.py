# Minetest MTS schematic exporter MCEdit filter
# by sfan5

import zlib
import struct
import sys
import os
import time
from thread import start_new_thread, allocate_lock

displayName = "Export to Minetest MTS schematic"

#Reference MC: http://hydra-media.cursecdn.com/minecraft.gamepedia.com/8/8c/DataValuesBeta.png
#Reference MT:
# https://github.com/minetest/minetest_game/blob/master/mods/default/nodes.lua
# https://github.com/minetest/minetest_game/blob/master/mods/wool/init.lua
# https://github.com/minetest/minetest_game/blob/master/mods/stairs/init.lua
# https://github.com/minetest/minetest_game/blob/master/mods/flowers/init.lua
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
	(38 ,  0, "flowers:rose"),
	(38 ,  4, "flowers:tulip"),
	(38 ,  5, "flowers:tulip"),
	(38 ,  6, "flowers:tulip"),
	(38 ,  7, "flowers:tulip"),
	(38 ,  8, "flowers:dandelion_white"),
	(38 , -1, "flowers:geranium"), # Convert all other flowers to a geranium
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
	# Reference: https://github.com/Jeija/minetest-mod-mesecons
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
]

inputs = (
	("Output filename", "string"),
	("Compression level (1=fastest, 9=best)", ("7", "1", "2", "3", "4", "5", "6", "8", "9")),
	("Enabled Mods", "label"),
	("Mesecons", ("No", "Yes")),
	("Nether", ("No", "Yes")),
)

numconverted = 0
numconverted_lastsec = 0
numconverted_lastsec_lock = allocate_lock()
nps_thread_exit = False

def nps_thread():
	global numconverted, numconverted_lastsec, numconverted_lastsec_lock
	while not nps_thread_exit:
		time.sleep(1)
		numconverted_lastsec_lock.acquire()
		numconverted_lastsec = numconverted
		numconverted_lastsec_lock.release()

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
	global numconverted, numconverted_lastsec, numconverted_lastsec_lock
	def getnodeid(arr, nn):
		if not nn in arr:
			arr.append(nn)
		return arr.index(nn)
	def crout():
		# zlib object, compressed data
		return [zlib.compressobj(1), ""]
	def wrout(where, what):
		where[1] += where[0].compress(what)
	def retrout(where):
		cd = where[1] + where[0].flush()
		del where[0]
		return zlib.decompress(cd)

	try:
		f = open(options["Output filename"] + ".mts", 'w')
	except:
		raise

	size = (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)
	complvl = int(options["Compression level (1=fastest, 9=best)"])
	print("Saving file at: %s/%s.mts" % (os.getcwd(), options["Output filename"]))

	mods = {}
	for arg in options.keys():
		if options[arg] == "Yes":
			mods[arg.lower()] = True

	nodenames = []
	outdata1 = crout()
	outdata2 = crout()

	numnodes = size[0] * size[1] * size[2]
	print_pc_interval = numnodes * 0.0025
	print_counter = 0
	nps_avg = 0
	start_new_thread(nps_thread, ())
	start = time.time()
	sys.stdout.write("\n")

	for z in xrange(box.minz, box.maxz):
		for y in xrange(box.miny, box.maxy):
			for x in xrange(box.minx, box.maxx):
				c = findConversion(level.blockAt(x, y, z), level.blockDataAt(x, y, z), mods)
				if c == None:
					wrout(outdata1, struct.pack("!H", getnodeid(nodenames, "air")))
					wrout(outdata2, "\x00")
				else:
					wrout(outdata1, struct.pack("!H", getnodeid(nodenames, c[0])))
					wrout(outdata2, chr(c[1]))
				print_counter += 1
				numconverted += 1
				if print_counter >= print_pc_interval:
					numconverted_lastsec_lock.acquire()
					nps_avg = (nps_avg + (numconverted - numconverted_lastsec)) / 2
					sys.stdout.write(
						"\r%0.2f%% done, %d nodes / sec, ETA: %d sec(s)       "
						% (
							(float(numconverted) / numnodes) * 100,
							nps_avg,
							float(numnodes) / nps_avg,
						)
					)
					numconverted_lastsec_lock.release()
					sys.stdout.flush()
					print_counter = 0

	compr = zlib.compressobj(complvl)
	outdata = ""
	outdata += compr.compress(retrout(outdata1))
	outdata += compr.compress("\xff" * numnodes)
	outdata += compr.compress(retrout(outdata2))
	outdata += compr.flush()
	del compr
	end = time.time()
	sys.stdout.write("\rFinished in %0.3f seconds!" % (end-start,))
	sys.stdout.flush()

	f.write("MTSM")
	f.write(struct.pack("!HHHH", 3, size[0], size[1], size[2]))
	for i in range(size[1]):
		f.write(chr(0xff))
	f.write(struct.pack("!H", len(nodenames)))
	for nn in nodenames:
		f.write(struct.pack("!H", len(nn)) + nn)
	f.write(outdata)
	f.close()
