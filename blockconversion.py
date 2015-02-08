# this code based on Minecraft to Minetest WE schematic MCEdit filter by sfan5
# modified by dgm3333

#Reference MC: http://media-mcw.cursecdn.com/8/8c/DataValuesBeta.png
#Reference MT:
# https://github.com/minetest/common/blob/master/mods/default/init.lua
# https://github.com/minetest/common/blob/master/mods/wool/init.lua
# https://github.com/minetest/common/blob/master/mods/stairs/init.lua
#Mesecons
# Reference: https://github.com/Jeija/minetest-mod-mesecons/blob/master/mesecons_alias/init.lua
#Nether
# Reference: https://github.com/PilzAdam/nether/blob/master/init.lua
#Riesenpilz
# Reference: https://github.com/HybridDog/riesenpilz/blob/master/init.lua

MC2MTdict = {
    #blockdata -1 means ignore
    #blockdata -2 means copy without change
    #blockdata -3 means copy and convert the mc facedir value to mt facedir
    #blockdata -4 is for stairs to support upside down ones

#   ID.dat   Minecraft Name       MC ID#  blockdata   minetest-nodename
    000.99:['Air',				     0,      -1,	  'default:air','',														''],
    001.99:['Stone',				 1,		 -1,	  'default:stone',														''],
    002.99:['Grass',				 2,		 -1,	  'default:dirt_with_grass',														''],
    003.99:['Dirt', 				 3,		 -1,	  'default:dirt',														''],
    004.99:['Cobblestone',			 4,		 -1,	  'default:cobble',														''],
    005.03:['WoodenPlank',			 5,		  3,	  'default:junglewood',														''],
    005.99:['WoodenPlank',			 5,		 -1,	  'default:wood',														''],
    006.03:['Sapling',				 6,		  3,	  'default:junglesapling',														''],
    006.99:['Sapling',				 6,		 -1,	  'default:sapling',														''],
    007.99:['Bedrock',				 7,		 -1,	  'default:stone',														''],
    008.99:['WaterFlo', 			 8,		 -1,	  'default:water_flowing',														''],
    009.99:['Water',				 9,		 -1,	  'default:water_source',														''],
    010.99:['LavaFlo',				 10,	 -1,	  'default:lava_flowing',														''],
    011.99:['Lava', 				 11,	 -1,	  'default:lava_source',														''],
    012.99:['Sand', 				 12,	 -1,	  'default:sand',														''],
    013.99:['Gravel',				 13,	 -1,	  'default:gravel',														''],
    014.99:['GoldOre',				 14,	 -1,	  'default:stone_with_gold',														''],
    015.99:['IronOre',				 15,	 -1,	  'default:stone_with_iron',														''],
    016.99:['CoalOre',				 16,	 -1,	  'default:stone_with_coal',														''],
    017.03:['Wood', 				 17,	  3,	  'default:jungletree',														''],
    017.99:['Wood', 				 17,	 -1,	  'default:tree',														''],
    018.03:['Leaves',				 18,	  3,	  'default:jungleleaves',														''],
    018.99:['Leaves',				 18,	 -1,	  'default:leaves',														''],
    019.00:['Sponge',				 19,	  0,	  '??',														''],
    020.99:['Glass',				 20,	 -1,	  'default:glass',														''],
    021.99:['LapisLazuliOre',		 21,	 -1,	  'default:stone_with_copper',								''],
    022.99:['LapisLazuliBlock', 	 22,	 -1,	  'default:copperblock',									''],
    023.00:['Dispenser',			 23,	  0,	  '??',														''],
    024.99:['Sandstone',			 24,	  1,	  'default:sandstonebrick',									''],
    024.99:['Sandstone',			 24,	 -1,	  'default:sandstone',										''],
    025.99:['NoteBlock',			 25,	 -1,	  'mesecons_noteblock:noteblock',                  'mesecons'],
    026.00:['Bed',   				 26,	  0,	  '??',														''],
    027.00:['PwrRail',				 27,	  0,	  '??',														''],
    028.00:['DetRail',				 28,	  0,	  '??',														''],
    029.97:['StickyPiston', 		 29,	 -3,	  'mesecons_pistons:piston_sticky_off',	  'mesecons'],
    030.00:['Cobweb',				 30,	  0,	  '??',														''],
    031.00:['TallGrass',			 31,	  0,	  'default:dry_shrub',														''],
    031.01:['TallGrass',		     31,	  1,	  'default:grass_4',														''],
    031.02:['TallGrass',		     31,	  2,	  'default:grass_3',														''],
    031.99:['TallGrass',		     31,	 -1,	  'default:grass_1',														''],
    032.99:['DeadBush', 			 32,	 -1,	  'default:dry_shrub',														''],
    033.97:['Piston',				 33,	 -3,	  'mesecons_pistons:piston_normal_off',	  'mesecons'],
    034.00:['PistonHead',			 34, 	  0,	  '??',														''],
    035.00:['Wool', 				 35,	  0,	  'wool:white',														''],
    035.01:['Wool', 				 35,	  1,	  'wool:orange',														''],
    035.04:['Wool', 				 35,	  4,	  'wool:yellow',														''],
    035.05:['Wool', 				 35,	  5,	  'wool:green',														''],
    035.06:['Wool', 				 35,	  6,	  'wool:pink',														''],
    035.07:['Wool', 				 35,	  7,	  'wool:dark_grey',														''],
    035.08:['Wool', 				 35,	  8,	  'wool:grey',														''],
    035.09:['Wool', 				 35,	  9,	  'wool:cyan',														''],
    035.10:['Wool', 				 35,	 10,	  'wool:violet',														''],
    035.11:['Wool', 				 35,	 11,	  'wool:blue',														''],
    035.12:['Wool', 				 35,	 12,	  'wool:brown',														''],
    035.13:['Wool', 				 35,	 13,	  'wool:dark_green',														''],
    035.14:['Wool', 				 35,	 14,	  'wool:red',														''],
    035.15:['Wool', 				 35,	 15,	  'wool:black',														''],
    036.00:['??',                    36,	  0,	  '??',														''],
    037.99:['Dandelion',			 37,	 -1,	  'flowers:dandelion_yellow',														''],
    038.99:['Rose', 				 38,	 -1,	  'flowers:rose',														''],
    039.99:['BrownMushrm',			 39,	 -1,	  'riesenpilz:brown',	  'riesenpilz'],
    040.99:['RedMushrm',			 40,	 -1,	  'riesenpilz:red',	  'riesenpilz'],
    041.99:['GoldBlock',			 41,	 -1,	  'default:goldblock',														''],
    042.99:['IronBlock',			 42,	 -1,	  'default:steelblock',														''],
    043.01:['DblSlabs', 			 43,	  1,	  'default:sandstone',														''],
    043.02:['DblSlabs', 			 43,	  2,	  'default:wood',														''],
    043.03:['DblSlabs', 			 43,	  3,	  'default:cobble',														''],
    043.04:['DblSlabs', 			 43,	  4,	  'default:brick',														''],
    043.05:['DblSlabs', 			 43,	  5,	  'default:stonebrick',														''],
    043.06:['DblSlabs', 			 43,	  6,	  'nether:brick',	  'nether'],
    044.00:['Slabs',				 44,	  0,	  'stairs:slab_stone',														''],
    044.01:['Slabs',				 44,	  1,	  'stairs:slab_sandstone',														''],
    044.02:['Slabs',				 44,	  2,	  'stairs:slab_wood',														''],
    044.03:['Slabs',				 44,	  3,	  'stairs:slab_cobble',														''],
    044.04:['Slabs',				 44,	  4,	  'stairs:slab_brick',														''],
    044.05:['Slabs',				 44,	  5,	  'stairs:slab_stonebrick',														''],
    044.08:['Slabs',				 44,	  8,	  'stairs:slab_stoneupside_down',														''],
    044.09:['Slabs',				 44,	  9,	  'stairs:slab_sandstoneupside_down',														''],
    044.10:['Slabs',				 44,	 10,	  'stairs:slab_woodupside_down',														''],
    044.11:['Slabs',				 44,	 11,	  'stairs:slab_cobbleupside_down',														''],
    044.12:['Slabs',				 44,	 12,	  'stairs:slab_brickupside_down',														''],
    044.13:['Slabs',				 44,	 13,	  'stairs:slab_stonebrickupside_down',														''],
    045.99:['BrickBlock',			 45,	 -1,	  'default:brick',														''],
    046.00:['TNT',                   46,	  0,	  '??',														''],
    047.99:['Bookshelf',			 47,	 -1,	  'default:bookshelf',														''],
    048.99:['MossStone',			 48,	 -1,	  'default:mossycobble',														''],
    049.99:['Obsidian', 			 49,	 -1,	  'default:obsidian',														''],
    050.97:['Torch',				 50,	 -3,	  'default:torch',														''],
    051.99:['Fire', 				 51,	 -1,	  'fire:basic_flame',														''],
    052.00:['MonsterSpawner',		 52,	  0,	  '??',														''],
    053.96:['WoodenStairs', 		 53,	 -4,	  'stairs:stair_wood',														''],
    054.99:['Chest',				 54,	 -1,	  'default:chest',														''],
    055.99:['RedStnWire',			 55,	 -1,	  'mesecons:wire_00000000_off',	  'mesecons'],
    056.99:['DiamondOre',			 56,	 -1,	  'default:stone_with_diamond',														''],
    057.99:['DiamondBlock', 		 57,	 -1,	  'default:diamondblock',														''],
    058.00:['CraftingTbl',			 58,	  0,	  '??',														''],
    059.00:['Seeds',				 59,	  0,	  '??',														''],
    060.00:['Farmland', 			 60,	  0,	  '??',														''],
    061.99:['Furnace',				 61,	 -1,	  'default:furnace',														''],
    062.99:['Burnace',				 62,	 -1,	  'default:furnace_active',														''],
    063.99:['SignPost', 			 63,	 -1,	  'default:sign_wood',														''],
    064.99:['WoodDoor', 			 64,	 -1,	  'doors:door_wood_t_1',														''],
    065.99:['Ladder',				 65,	 -1,	  'default:ladder',														''],
    066.99:['Rail', 				 66,	 -1,	  'default:rail',														''],
    067.96:['CobbleStairs', 		 67,	 -4,	  'stairs:stair_cobble',														''],
    068.97:['WallSign', 			 68,	 -3,	  'default:sign_wood',														''],
    069.97:['Lever',				 69,	 -3,	  'mesecons_walllever:wall_lever_off',        	  'mesecons'],
    070.99:['StnPressPlate',		 70,	 -1,	  'mesecons_pressureplates:pressure_plate_stone_off', 'mesecons'],
    071.99:['IronDoor', 			 71,	 -1,	  'doors:door_steel_t_1',									''],
    072.99:['WdnPressPlate',		 72,	 -1,	  'mesecons_pressureplates:pressure_plate_wood_off',  'mesecons'],
    073.99:['RedstOre', 			 73,	 -1,	  'default:stone_with_mese',                   	  'mesecons'],
    074.99:['RedstOreGlowing',		 74,	 -1,	  'default:stone_with_mese',                  	  'mesecons'],
    075.97:['RedstTorchOff',		 75,	 -3,	  'mesecons_torch:torch_off',               	  'mesecons'],
    076.97:['RedstTorchOn', 		 76,	 -3,	  'mesecons_torch:torch_on',                	  'mesecons'],
    077.97:['StoneButton',			 77,	 -3,	  'mesecons_button:button_off',              	  'mesecons'],
    078.99:['Snow', 				 78,	 -1,	  'default:snow',											''],
    079.99:['Ice',                   79,	 -1,	  'default:ice',											''],
    080.99:['SnowBlock',			 80,	 -1,	  'default:snowblock',										''],
    081.99:['Cactus',				 81,	 -1,	  'default:cactus',											''],
    082.99:['ClayBlock',			 82,	 -1,	  'default:clay',											''],
    083.99:['SugarCane',			 83,	 -1,	  'default:papyrus',										''],
    084.00:['Jukebox',				 84,	  0,	  '??',														''],
    085.99:['Fence',				 85,	 -1,	  'default:fence_wood',										''],
    086.00:['Pumpkin',				 86,	  0,	  '??',														''],
    087.99:['Netherrack',			 87,	 -1,	  'nether:rack',                                  	  'nether'],
    088.99:['SoulSand', 			 88,	 -1,	  'nether:sand',                                   	  'nether'],
    089.99:['Glowstone',			 89,	 -1,	  'nether:glowstone',                              	  'nether'],
    090.97:['Portal',				 90,	 -3,	  'nether:portal',                               	  'nether'],
    091.00:['JackOLantern', 		 91,	  0,	  '??',														''],
    092.00:['Cake', 				 92,	  0,	  '??',														''],
    093.97:['RedRepOff',			 93,	 -3,	  'mesecons_delayer:delayer_off_1',            	  'mesecons'],
    094.97:['RedRepOn', 			 94,	 -3,	  'mesecons_delayer:delayer_on_1',             	  'mesecons'],
#    095:['LockedChest',		 95,	  0,	  '??',														''],
#     blocks are non-textured and opaque... unanticipated state?,				 ,				 ,				 ,
    095.00:['StainedGlass', 		 95,	  0,	  '??',														''],
    096.00:['Trapdoor', 			 96,	  0,	  '??',														''],
    097.00:['HiddenSfish',			 97,	  0,	  '??',														''],
    098.99:['StoneBricks',			 98,	 -1,	  'default:stonebrick',										''],
    099.97:['HgRedM',				 99,	 -3,	  'riesenpilz:head_brown',                   	  'riesenpilz'],
    100.97:['HgBrwM',				 100,	 -3,	  'riesenpilz:head_brown',                  	  'riesenpilz'],
    101.00:['IronBars', 			 101,	  0,	  '??',														''],
    102.00:['GlassPane',			 102,	  0,	  '??',														''],
    103.00:['Melon',				 103,	  0,	  '??',														''],
    104.00:['PumpkinStem',   		 104,	  0,	  '??',														''],
    105.00:['MelonStem',			 105,	  0,	  '??',														''],
    106.00:['Vines',				 106,	  0,	  '??',														''],
    107.00:['FenceGate',			 107,	  0,	  '??',														''],
    108.96:['BrickStairs',			 108,	 -4,	  'stairs:stair_brick',										''],
    109.97:['StoneBrickStairs', 	 109,	 -3,	  'stairs:stair_stonebrick',								''],
    110.00:['Mycelium', 			 110,	  0,	  '??',														''],
    111.00:['LilyPad',				 111,	  0,	  '??',														''],
    112.00:['NethrBrick',			 112,	  0,	  '??',														''],
    113.00:['NethrBrickFence',		 113,	  0,	  '??',														''],
    114.00:['NethrBrickStairs', 	 114,	  0,	  '??',														''],
    115.00:['NethrWart',			 115,	  0,	  '??',														''],
    116.00:['EnchantTab',			 116,	  0,	  '??',														''],
    117.00:['BrewStnd', 			 117,	  0,	  '??',														''],
    118.00:['Cauldron', 			 118,	  0,	  '??',														''],
    119.00:['EndPortal',			 119,	  0,	  '??',														''],
    120.00:['EndPortalFrame',		 120,	  0,	  '??',														''],
    121.00:['EndStone', 			 121,	  0,	  '??',														''],
    122.00:['DragonEgg',			 122,	  0,	  '??',														''],
    123.99:['RedstLampOff', 		 123,	 -1,	  'mesecons_lightstone_red_off',               	  'mesecons'],
    124.99:['RedstLampOn',			 124,	 -1,	  'mesecons_lightstone_red_on',             	  'mesecons'],
    125.03:['??',                    125,	  3,	  'default:junglewood',										''],
    125.99:['??',                    125,	 -1,	  'default:wood',											''],
    126.03:['??',                    126,	  3,	  'stairs:slab_junglewood',									''],
    126.99:['??',                    126,	 -1,	  'stairs:slab_wood',										''],
    127.00:['??',                    127,	  0,	  '??',														''],
    128.96:['??',                    128,	 -4,	  'stairs:stair_sandstone',									''],
    129.99:['EmeraldOre',			 129,	 -1,	  'default:stone_with_mese',								''],
    130.00:['??',                    130,	  0,	  '??',														''],
    131.00:['??',                    131,	  0,	  '??',														''],
    132.00:['??',                    132,	  0,	  '??',														''],
    133.99:['EmeraldBlock', 		 133,	 -1,	  'default:mese',											''],
    134.96:['??',                    134,	 -4,	  'stairs:stair_wood',		     							''],
    135.96:['??',                    135,	 -4,	  'stairs:stair_wood',										''],
    136.96:['??',                    136,	 -4,	  'stairs:stair_junglewood',								''],
    137.99:['??',                    137,	 -1,	  'mesecons_commandblock:commandblock_off',	      'mesecons'],
    138.00:['Beacon',				 138,	  0,	  '??',														''],
    151.99:['??',                    151,	 -1,	  'mesecons_solarpanel:solar_panel_off',     	  'mesecons'],
    152.99:['Redstone', 			 152,	 -1,	  'default:mese',                             	  'mesecons'],
    153.00:['NetherQuartzOre',		 153,	  0,	  '??',														''],
    155.00:['Quartz',				 155,	  0,	  '??',														''],
    159.00:['StainedClay',			 159,	  0,	  '??',														''],
    162.00:['Acacia',				 162,	  0,	  '??',														''],
    168.00:['Prismarine',			 168,	  0,	  '??',														''],
    169.00:['SeaLantern',			 169,	  0,	  '??',														''],
    170.00:['HayBale',				 170,	  0,	  '??',														''],
    172.00:['HardenedClay', 		 172,	  0,	  '??',														''],
    173.00:['BlockOfCoal',			 173,	  0,	  '??',														''],
    174.00:['PackedIce',			 174,	  0,	  '??',														''],
    179.00:['RedSandstone', 		 179,	  0,	  '??',                                                     '']
}



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
    for cnv in MC2MTtable:
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

# def perform(level, box, options):
#     try:
#         f = open("../" + options["Output filename"] + ".we", 'w')
#     except:
#         raise
#
#     origin = (
#         box.minx + int((box.maxx - box.minx) / 2),
#         box.miny + int((box.maxy - box.miny) / 2),
#         box.minz + int((box.maxz - box.minz) / 2),
#     )
#
#     mods = {}
#     for arg in options.keys():
#         if options[arg] == "True":
#             mods[arg.lower()] = True
#
#     for x in xrange(box.minx, box.maxx):
#         for z in xrange(box.minz, box.maxz):
#             for y in xrange(box.miny, box.maxy):
#                 c = findConversion(level.blockAt(x, y, z), level.blockDataAt(x, y, z), mods)
#                 if c == None:
#                     continue
#                 calcpos = (x - origin[0], y - origin[1], z - origin[2])
#                 fmttpl = calcpos + (c[0], level.blockLightAt(x, y, z), c[1])
#                 f.write("%d %d %d %s %d %d\n" % fmttpl)
#
#     f.close()
