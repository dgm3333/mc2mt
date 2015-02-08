import os
#import bpy

from struct import unpack   #, error as StructError
import nbtreader, mcregionreader
import blockconversion
from mineregion import OPTIONS, EXCLUDED_BLOCKS, BLOCKDATA, REPORTING, unknownBlockIDs, WORLD_ROOT
##..yuck: they're immutable and don't return properly except for the dict-type ones. Get rid of this in next cleanup.

from math import floor

MC2MTdict2 = {
    #blockdata -1 means ignore
    #blockdata -2 means copy without change
    #blockdata -3 means copy and convert the mc facedir value to mt facedir
    #blockdata -4 is for stairs to support upside down ones

#   ID.dat   Minecraft Name       MC ID#  blockdata   minetest-nodename
    0    :['Air',                     0,      -1,      'default:air','',                                                        ''],
    1    :['Stone',                 1,         -1,      'default:stone',                                                        ''],
    2    :['Grass',                 2,         -1,      'default:dirt_with_grass',                                                        ''],
    3    :['Dirt',                  3,         -1,      'default:dirt',                                                        ''],
    4    :['Cobblestone',             4,         -1,      'default:cobble',                                                        ''],
    5    :['WoodenPlank',             5,          3,      'default:junglewood',                                                        ''],
    5    :['WoodenPlank',             5,         -1,      'default:wood',                                                        ''],
    6    :['Sapling',                 6,          3,      'default:junglesapling',                                                        ''],
    6    :['Sapling',                 6,         -1,      'default:sapling',                                                        ''],
    7    :['Bedrock',                 7,         -1,      'default:stone',                                                        ''],
    8    :['WaterFlo',              8,         -1,      'default:water_flowing',                                                        ''],
    9    :['Water',                 9,         -1,      'default:water_source',                                                        ''],
    10    :['LavaFlo',                 10,     -1,      'default:lava_flowing',                                                        ''],
    11    :['Lava',                  11,     -1,      'default:lava_source',                                                        ''],
    12    :['Sand',                  12,     -1,      'default:sand',                                                        ''],
    13    :['Gravel',                 13,     -1,      'default:gravel',                                                        ''],
    14    :['GoldOre',                 14,     -1,      'default:stone_with_gold',                                                        ''],
    15    :['IronOre',                 15,     -1,      'default:stone_with_iron',                                                        ''],
    16    :['CoalOre',                 16,     -1,      'default:stone_with_coal',                                                        ''],
    17    :['Wood',                  17,      3,      'default:jungletree',                                                        ''],
    17    :['Wood',                  17,     -1,      'default:tree',                                                        ''],
    18    :['Leaves',                 18,      3,      'default:jungleleaves',                                                        ''],
    18    :['Leaves',                 18,      3,      'default:jungleleaves',                                                        ''],
    18    :['Leaves',                 18,     -1,      'default:leaves',                                                        ''],
    19    :['Sponge',                 19,      0,      '??',                                                        ''],
    20    :['Glass',                 20,     -1,      'default:glass',                                                        ''],
    21    :['LapisLazuliOre',         21,     -1,      'default:stone_with_copper',                                ''],
    22    :['LapisLazuliBlock',      22,     -1,      'default:copperblock',                                    ''],
    23    :['Dispenser',             23,      0,      '??',                                                        ''],
    24    :['Sandstone',             24,      1,      'default:sandstonebrick',                                    ''],
    24    :['Sandstone',             24,     -1,      'default:sandstone',                                        ''],
    25    :['NoteBlock',             25,     -1,      'mesecons_noteblock:noteblock',                  'mesecons'],
    26    :['Bed',                    26,      0,      '??',                                                        ''],
    27    :['PwrRail',                 27,      0,      '??',                                                        ''],
    28    :['DetRail',                 28,      0,      '??',                                                        ''],
    29    :['StickyPiston',          29,     -3,      'mesecons_pistons:piston_sticky_off',      'mesecons'],
    30    :['Cobweb',                 30,      0,      '??',                                                        ''],
    31    :['TallGrass',             31,      0,      'default:dry_shrub',                                                        ''],
    31    :['TallGrass',             31,      1,      'default:grass_4',                                                        ''],
    31    :['TallGrass',             31,      2,      'default:grass_3',                                                        ''],
    31    :['TallGrass',             31,     -1,      'default:grass_1',                                                        ''],
    32    :['DeadBush',              32,     -1,      'default:dry_shrub',                                                        ''],
    33    :['Piston',                 33,     -3,      'mesecons_pistons:piston_normal_off',      'mesecons'],
    34    :['PistonHead',             34,       0,      '??',                                                        ''],
    35    :['Wool',                  35,      0,      'wool:white',                                                        ''],
    35    :['Wool',                  35,      1,      'wool:orange',                                                        ''],
    35    :['Wool',                  35,      4,      'wool:yellow',                                                        ''],
    35    :['Wool',                  35,      5,      'wool:green',                                                        ''],
    35    :['Wool',                  35,      6,      'wool:pink',                                                        ''],
    35    :['Wool',                  35,      7,      'wool:dark_grey',                                                        ''],
    35    :['Wool',                  35,      8,      'wool:grey',                                                        ''],
    35    :['Wool',                  35,      9,      'wool:cyan',                                                        ''],
    35    :['Wool',                  35,     10,      'wool:violet',                                                        ''],
    35    :['Wool',                  35,     11,      'wool:blue',                                                        ''],
    35    :['Wool',                  35,     12,      'wool:brown',                                                        ''],
    35    :['Wool',                  35,     13,      'wool:dark_green',                                                        ''],
    35    :['Wool',                  35,     14,      'wool:red',                                                        ''],
    35    :['Wool',                  35,     15,      'wool:black',                                                        ''],
    36    :['??',                    36,      0,      '??',                                                        ''],
    37    :['Dandelion',             37,     -1,      'flowers:dandelion_yellow',                                                        ''],
    38    :['Rose',                  38,     -1,      'flowers:rose',                                                        ''],
    39    :['BrownMushrm',             39,     -1,      'riesenpilz:brown',      'riesenpilz'],
    40    :['RedMushrm',             40,     -1,      'riesenpilz:red',      'riesenpilz'],
    41    :['GoldBlock',             41,     -1,      'default:goldblock',                                                        ''],
    42    :['IronBlock',             42,     -1,      'default:steelblock',                                                        ''],
    43    :['DblSlabs',              43,      1,      'default:sandstone',                                                        ''],
    43    :['DblSlabs',              43,      2,      'default:wood',                                                        ''],
    43    :['DblSlabs',              43,      3,      'default:cobble',                                                        ''],
    43    :['DblSlabs',              43,      4,      'default:brick',                                                        ''],
    43    :['DblSlabs',              43,      5,      'default:stonebrick',                                                        ''],
    43    :['DblSlabs',              43,      6,      'nether:brick',      'nether'],
    44    :['Slabs',                 44,      0,      'stairs:slab_stone',                                                        ''],
    44    :['Slabs',                 44,      1,      'stairs:slab_sandstone',                                                        ''],
    44    :['Slabs',                 44,      2,      'stairs:slab_wood',                                                        ''],
    44    :['Slabs',                 44,      3,      'stairs:slab_cobble',                                                        ''],
    44    :['Slabs',                 44,      4,      'stairs:slab_brick',                                                        ''],
    44    :['Slabs',                 44,      5,      'stairs:slab_stonebrick',                                                        ''],
    44    :['Slabs',                 44,      8,      'stairs:slab_stoneupside_down',                                                        ''],
    44    :['Slabs',                 44,      9,      'stairs:slab_sandstoneupside_down',                                                        ''],
    44    :['Slabs',                 44,     10,      'stairs:slab_woodupside_down',                                                        ''],
    44    :['Slabs',                 44,     11,      'stairs:slab_cobbleupside_down',                                                        ''],
    44    :['Slabs',                 44,     12,      'stairs:slab_brickupside_down',                                                        ''],
    44    :['Slabs',                 44,     13,      'stairs:slab_stonebrickupside_down',                                                        ''],
    45    :['BrickBlock',             45,     -1,      'default:brick',                                                        ''],
    46    :['TNT',                   46,      0,      '??',                                                        ''],
    47    :['Bookshelf',             47,     -1,      'default:bookshelf',                                                        ''],
    48    :['MossStone',             48,     -1,      'default:mossycobble',                                                        ''],
    49    :['Obsidian',              49,     -1,      'default:obsidian',                                                        ''],
    50    :['Torch',                 50,     -3,      'default:torch',                                                        ''],
    51    :['Fire',                  51,     -1,      'fire:basic_flame',                                                        ''],
    52    :['MonsterSpawner',         52,      0,      '??',                                                        ''],
    53    :['WoodenStairs',          53,     -4,      'stairs:stair_wood',                                                        ''],
    54    :['Chest',                 54,     -1,      'default:chest',                                                        ''],
    55    :['RedStnWire',             55,     -1,      'mesecons:wire_00000000_off',      'mesecons'],
    56    :['DiamondOre',             56,     -1,      'default:stone_with_diamond',                                                        ''],
    57    :['DiamondBlock',          57,     -1,      'default:diamondblock',                                                        ''],
    58    :['CraftingTbl',             58,      0,      '??',                                                        ''],
    59    :['Seeds',                 59,      0,      '??',                                                        ''],
    60    :['Farmland',              60,      0,      '??',                                                        ''],
    61    :['Furnace',                 61,     -1,      'default:furnace',                                                        ''],
    62    :['Burnace',                 62,     -1,      'default:furnace_active',                                                        ''],
    63    :['SignPost',              63,     -1,      'default:sign_wood',                                                        ''],
    64    :['WoodDoor',              64,     -1,      'doors:door_wood_t_1',                                                        ''],
    65    :['Ladder',                 65,     -1,      'default:ladder',                                                        ''],
    66    :['Rail',                  66,     -1,      'default:rail',                                                        ''],
    67    :['CobbleStairs',          67,     -4,      'stairs:stair_cobble',                                                        ''],
    68    :['WallSign',              68,     -3,      'default:sign_wood',                                                        ''],
    69    :['Lever',                 69,     -3,      'mesecons_walllever:wall_lever_off',              'mesecons'],
    70    :['StnPressPlate',         70,     -1,      'mesecons_pressureplates:pressure_plate_stone_off', 'mesecons'],
    71    :['IronDoor',              71,     -1,      'doors:door_steel_t_1',                                    ''],
    72    :['WdnPressPlate',         72,     -1,      'mesecons_pressureplates:pressure_plate_wood_off',  'mesecons'],
    73    :['RedstOre',              73,     -1,      'default:stone_with_mese',                         'mesecons'],
    74    :['RedstOreGlowing',         74,     -1,      'default:stone_with_mese',                        'mesecons'],
    75    :['RedstTorchOff',         75,     -3,      'mesecons_torch:torch_off',                     'mesecons'],
    76    :['RedstTorchOn',          76,     -3,      'mesecons_torch:torch_on',                      'mesecons'],
    77    :['StoneButton',             77,     -3,      'mesecons_button:button_off',                    'mesecons'],
    78    :['Snow',                  78,     -1,      'default:snow',                                            ''],
    79    :['Ice',                   79,     -1,      'default:ice',                                            ''],
    80    :['SnowBlock',             80,     -1,      'default:snowblock',                                        ''],
    81    :['Cactus',                 81,     -1,      'default:cactus',                                            ''],
    82    :['ClayBlock',             82,     -1,      'default:clay',                                            ''],
    83    :['SugarCane',             83,     -1,      'default:papyrus',                                        ''],
    84    :['Jukebox',                 84,      0,      '??',                                                        ''],
    85    :['Fence',                 85,     -1,      'default:fence_wood',                                        ''],
    86    :['Pumpkin',                 86,      0,      '??',                                                        ''],
    87    :['Netherrack',             87,     -1,      'nether:rack',                                        'nether'],
    88    :['SoulSand',              88,     -1,      'nether:sand',                                         'nether'],
    89    :['Glowstone',             89,     -1,      'nether:glowstone',                                    'nether'],
    90    :['Portal',                 90,     -3,      'nether:portal',                                     'nether'],
    91    :['JackOLantern',          91,      0,      '??',                                                        ''],
    92    :['Cake',                  92,      0,      '??',                                                        ''],
    93    :['RedRepOff',             93,     -3,      'mesecons_delayer:delayer_off_1',                  'mesecons'],
    94    :['RedRepOn',              94,     -3,      'mesecons_delayer:delayer_on_1',                   'mesecons'],
#    095':['LockedChest',         95,      0,      '??',                                                        ''],
#     blocks are non-textured and opaque... unanticipated state?,                 ,                 ,                 ,
    95    :['StainedGlass',          95,      0,      '??',                                                        ''],
    96    :['Trapdoor',              96,      0,      '??',                                                        ''],
    97    :['HiddenSfish',             97,      0,      '??',                                                        ''],
    98    :['StoneBricks',             98,     -1,      'default:stonebrick',                                        ''],
    99    :['HgRedM',                 99,     -3,      'riesenpilz:head_brown',                         'riesenpilz'],
    100    :['HgBrwM',                 100,     -3,      'riesenpilz:head_brown',                        'riesenpilz'],
    101    :['IronBars',              101,      0,      '??',                                                        ''],
    102    :['GlassPane',             102,      0,      '??',                                                        ''],
    103    :['Melon',                 103,      0,      '??',                                                        ''],
    104    :['PumpkinStem',            104,      0,      '??',                                                        ''],
    105    :['MelonStem',             105,      0,      '??',                                                        ''],
    106    :['Vines',                 106,      0,      '??',                                                        ''],
    107    :['FenceGate',             107,      0,      '??',                                                        ''],
    108    :['BrickStairs',             108,     -4,      'stairs:stair_brick',                                        ''],
    109    :['StoneBrickStairs',      109,     -3,      'stairs:stair_stonebrick',                                ''],
    110    :['Mycelium',              110,      0,      '??',                                                        ''],
    111    :['LilyPad',                 111,      0,      '??',                                                        ''],
    112    :['NethrBrick',             112,      0,      '??',                                                        ''],
    113    :['NethrBrickFence',         113,      0,      '??',                                                        ''],
    114    :['NethrBrickStairs',      114,      0,      '??',                                                        ''],
    115    :['NethrWart',             115,      0,      '??',                                                        ''],
    116    :['EnchantTab',             116,      0,      '??',                                                        ''],
    117    :['BrewStnd',              117,      0,      '??',                                                        ''],
    118    :['Cauldron',              118,      0,      '??',                                                        ''],
    119    :['EndPortal',             119,      0,      '??',                                                        ''],
    120    :['EndPortalFrame',         120,      0,      '??',                                                        ''],
    121    :['EndStone',              121,      0,      '??',                                                        ''],
    122    :['DragonEgg',             122,      0,      '??',                                                        ''],
    123    :['RedstLampOff',          123,     -1,      'mesecons_lightstone_red_off',                     'mesecons'],
    124    :['RedstLampOn',             124,     -1,      'mesecons_lightstone_red_on',                   'mesecons'],
    125    :['??',                    125,      3,      'default:junglewood',                                        ''],
    125    :['??',                    125,     -1,      'default:wood',                                            ''],
    126    :['??',                    126,      3,      'stairs:slab_junglewood',                                    ''],
    126    :['??',                    126,     -1,      'stairs:slab_wood',                                        ''],
    127    :['??',                    127,      0,      '??',                                                        ''],
    128    :['??',                    128,     -4,      'stairs:stair_sandstone',                                    ''],
    129    :['EmeraldOre',             129,     -1,      'default:stone_with_mese',                                ''],
    130    :['??',                    130,      0,      '??',                                                        ''],
    131    :['??',                    131,      0,      '??',                                                        ''],
    132    :['??',                    132,      0,      '??',                                                        ''],
    133    :['EmeraldBlock',          133,     -1,      'default:mese',                                            ''],
    134    :['??',                    134,     -4,      'stairs:stair_wood',                                         ''],
    135    :['??',                    135,     -4,      'stairs:stair_wood',                                        ''],
    136    :['??',                    136,     -4,      'stairs:stair_junglewood',                                ''],
    137    :['??',                    137,     -1,      'mesecons_commandblock:commandblock_off',          'mesecons'],
    138    :['Beacon',                 138,      0,      '??',                                                        ''],
    151    :['??',                    151,     -1,      'mesecons_solarpanel:solar_panel_off',           'mesecons'],
    152    :['Redstone',              152,     -1,      'default:mese',                                   'mesecons'],
    153    :['NetherQuartzOre',         153,      0,      '??',                                                        ''],
    155    :['Quartz',                 155,      0,      '??',                                                        ''],
    159    :['StainedClay',             159,      0,      '??',                                                        ''],
    162    :['Acacia',                 162,      0,      '??',                                                        ''],
    168    :['Prismarine',             168,      0,      '??',                                                        ''],
    169    :['SeaLantern',             169,      0,      '??',                                                        ''],
    170    :['HayBale',                 170,      0,      '??',                                                        ''],
    172    :['HardenedClay',          172,      0,      '??',                                                        ''],
    173    :['BlockOfCoal',             173,      0,      '??',                                                        ''],
    174    :['PackedIce',             174,      0,      '??',                                                        ''],
    179    :['RedSandstone',          179,      0,      '??',                                                     '']
}

class AnvilChunkReader(mcregionreader.ChunkReader):

    #readBlock( bX, bZ (by?) ...  ignoring 'region' boundaries and chunk boundaries? We need an ignore-chunk-boundaries level of abstraction

    def getSingleBlock(chunkXZ, blockXYZ):   #returns the value and extradata bits for a single block of given absolute x,y,z block coords within chunk cx,cz. or None if area not generated.
        #y is value from 0..255
        cx, cy = chunkXZ
        bX,bY,bZ = blockXYZ
        rX = floor(cx / 32) # is this the same as >> 8 ??
        rZ = floor(cz / 32)
        rHdrOffset = ((cx % 32) + (cz % 32) * 32) * 4
        rFile = "r.%d.%d.mca" % (rx, rz)
        if not os.path.exists(rFile):
            return None
        with open(rFile, 'rb') as regionfile:
            regionfile.seek(rheaderoffset)
            cheadr = regionfile.read(4)
            dataoffset = unpack(">i", b'\x00'+cheadr[0:3])[0]
            chunksectorcount = cheadr[3]
            if dataoffset == 0 and chunksectorcount == 0:
                return None #Region exists, but the chunk we're after was never created within it.
            else:
                #possibly check for cached chunk data here, under the cx,cz in a list of already-loaded sets.
                chunkdata = AnvilChunkReader._readChunkData(regionfile, dataoffset, chunksectorcount)
                chunkLvl = chunkdata.value['Level'].value
                sections = chunkLvl['Sections'].value
                #each section is a 16x16x16 piece of chunk, with a Y-byte from 0-15, so that the 'y' value is 16*that + in-section-Y-value
                #some sections can be skipped, so we must iterate to find the right one with the 'Y' we expect.
                bSection = bY / 16
                sect = None
                for section in sections:
                    secY = section.value['Y'].value
                    if secY == bSection:
                        sect = section.value
                if sect is None:
                    return None
                blockData = sec['Blocks'].value    #a TAG_Byte_Array value (bytes object). Blocks is 16x16 bytes
                extraData = sec['Data'].value      #BlockLight, Data and SkyLight are 16x16 "4-bit cell" additional data arrays.
                sY = dY % 16
                blockIndex = (sY * 16 + dZ) * 16 + dX
                blockID = blockData[ blockIndex ]
                return blockID    #, extravalue)
                #NB: this can be made massively more efficient by storing 4 'neighbour chunk' data reads for every chunk properly processed.
                #Don't need to do diagonals, even.




    def readChunk2(self, chunkPosX, chunkPosZ, blockBuffer, zeroAdjX, zeroAdjY):
        # FIXME - implement me!
        return

    def readChunk(self, chunkPosX, chunkPosZ, vertexBuffer):  # aka "readChunkFromRegion" ...
        """Loads chunk located at the X,Z chunk location provided."""

        global REPORTING

        #region containing a given chunk is found thusly: floor of c over 32
        regionX = floor(chunkPosX / 32)
        regionZ = floor(chunkPosZ / 32)

        rheaderoffset = ((chunkPosX % 32) + (chunkPosZ % 32) * 32) * 4

        #print("Reading chunk %d,%d from region %d,%d" %(chunkPosX, chunkPosZ, regionX,regionZ))

        rfileName = "r.%d.%d.mca" % (regionX, regionZ)
        if not os.path.exists(rfileName):
            #Can't load: it doesn't exist!
            print("No such region generated.")
            return

        with open(rfileName, 'rb') as regfile:
            # header for the chunk we want is at...
            #The location in the region file of a chunk at (x, z) (in chunk coordinates) can be found at byte offset 4 * ((x mod 32) + (z mod 32) * 32) in its McRegion file.
            #Its timestamp can be found 4096 bytes later in the file
            regfile.seek(rheaderoffset)
            cheadr = regfile.read(4)
            dataoffset = unpack(">i", b'\x00'+cheadr[0:3])[0]
            chunksectorcount = cheadr[3]

            if dataoffset == 0 and chunksectorcount == 0:
                pass
                #print("Region exists, but chunk has never been created within it.")
            else:
                chunkdata = AnvilChunkReader._readChunkData(regfile, dataoffset, chunksectorcount)  #todo: rename that function!
                #Geometry creation! etc... If surface only, can get heights etc from lightarray?

                #top level tag in NBT is an unnamed TAG_Compound, for some reason, containing a named TAG_Compound "Level"
                chunkLvl = chunkdata.value['Level'].value
                #chunkXPos = chunkLvl['xPos'].value
                #chunkZPos = chunkLvl['zPos'].value
                #print("Reading blocks for chunk: (%d, %d)\n" % (chunkXPos, chunkZPos))
                AnvilChunkReader._readBlocks(chunkLvl, vertexBuffer)
                #print("Loaded chunk %d,%d" % (chunkPosX,chunkPosZ))

                REPORTING['totalchunks'] += 1


    def _readChunkData(bstream, chunkOffset, chunkSectorCount): #rename this!
        #get the datastring out of the file...
        import io, zlib

        #cf = open(fname, 'rb')
        initialPos = bstream.tell()

        cstart = chunkOffset * 4096    #4 kiB
        clen = chunkSectorCount * 4096
        bstream.seek(cstart)    #this bstream is the region file

        chunkHeaderAndData = bstream.read(clen)

        #chunk header stuff is:
        # 4 bytes: length (of remaining data)
        # 1 byte : compression type (1 - gzip - unused; 2 - zlib: it should always be this in actual fact)
        # then the rest, is length-1 bytes of compressed (zlib) NBT data.

        chunkDLength = unpack(">i", chunkHeaderAndData[0:4])[0]
        chunkDCompression = chunkHeaderAndData[4]
        if chunkDCompression != 2:
            print("Not a zlib-compressed chunk!?")
            raise StringError()    #MinecraftSomethingError, perhaps.

        chunkZippedBytes = chunkHeaderAndData[5:]

        #could/should check that chunkZippedBytes is same length as chunkDLength-1.

        #put the regionfile byte stream back to where it started:
        bstream.seek(initialPos)

        #Read the compressed chunk data
        zipper = zlib.decompressobj()
        chunkData = zipper.decompress(chunkZippedBytes)
        chunkDataAsFile = io.BytesIO(chunkData)
        chunkNBT = nbtreader.readNBT(chunkDataAsFile)

        return chunkNBT

    def getSectionBlock(blockLoc, sectionDict):
        """Fetches a block from section NBT data."""
        (bX,bY,bZ) = blockLoc
        secY = bY >> 4  #/ 16
        if secY not in sectionDict:
            return None
        sect = sectionDict[secY]
        sY = bY & 0xf   #mod 16
        bIndex = (sY * 16 + bZ) * 16 + bX
        #bitshift, or run risk of int casts
        dat = sect['Blocks'].value
        return dat[bIndex]

    #Hollow volumes optimisation (version1: in-chunk only)
    def _isExposedBlock(blockCoord, chunkXZ, secBlockData, sectionDict, blockID, skyHighLimit, depthLimit):    #another param: neighbourChunkData[] - a 4-list of NBT stuff...
        (dX,dY,dZ) = blockCoord
        #fail-fast. checks if all ortho adjacent neighbours fall inside this chunk.
        #EASY! Because it's 0-15 for both X and Z. For Y, we're iterating upward,
        #so get the previous value (the block below) passed in.

        if blockID == 18:   #leaves   #and glass? and other exemptions?
            return True

        if dX == 0 or dX == 15 or dY == 0 or dZ == 0 or dZ == 15:
            #get neighbour directly
            return True	#instead, check neigbouring chunks...


        #we can no longer get the block below or above easily as we might be iterating +x, -16x, or +z at any given step.
        if dY == skyHighLimit or dY == depthLimit:
            return True

        ySect = dY / 16     ## all this dividing integers by 16! I ask you! (>> 4)!
        yBoff = dY % 16     ## &= 0x0f
        #if you are on a section boundary, need next section for block above. else

        #GLOBALS (see readBlocks, below)
        CHUNKSIZE_X = 16    #static consts - global?
        CHUNKSIZE_Z = 16
        #new layout goes YZX. improves compression, apparently.
        ##_Y_SHIFT = 7    # 2**7 is 128. use for fast multiply
        ##_YZ_SHIFT = 11    #16 * 128 is 2048, which is 2**11

        #check above (Y+1)
        #either it's in the same section (quick/easy lookup) or it's in another section (still quite easy - next array over)
        #or, it's in another chunk. in which case, check chunkreadcache for the 4 adjacent. Failing this, it's the worse case and
        #we need to read into a whole new chunk data grab.
        if yBoff == 15:
            upBlock = AnvilChunkReader.getSectionBlock((dX,dY+1,dZ), sectionDict)
            if upBlock != blockID:
                return True
        else:
            #get it from current section
            upIndex = ((yBoff+1) * 16 + dZ) * 16 + dX
            upBlock = secBlockData[ upIndex ]
            if upBlock != blockID:
                return True

        #Check below (Y-1):
        if yBoff == 0:
            downBlock = AnvilChunkReader.getSectionBlock((dX,dY-1,dZ), sectionDict)
            if downBlock != blockID:
                return True
        else:
            downIndex = ((yBoff-1) * 16 + dZ) * 16 + dX
            dnBlock = secBlockData[downIndex]
            if dnBlock != blockID:
                return True

        #Have checked above and below; now check all sides. Same section, but maybe different chunks...
        #Check X-1 (leftward)
        leftIndex = (yBoff * 16 + dZ) * 16 + (dX-1)
        #ngbIndex = dY + (dZ << _Y_SHIFT) + ((dX-1) << _YZ_SHIFT)    #Check this lookup in readBlocks, below! Can it go o.o.b.?
        try:
            neighbour = secBlockData[leftIndex]
        except IndexError:
            print("Bogus index cockup: %d. Blockdata len is 16x16x16 bytes (4096)." % leftIndex)
            quit()
        if neighbour != blockID:
            return True

        #Check X+1
        rightIndex = (yBoff * 16 + dZ) * 16 + (dX+1)
        #ngbIndex = dY + (dZ << _Y_SHIFT) + ((dX+1) << _YZ_SHIFT)    #Check this lookup in readBlocks, below! Can it go o.o.b.?
        neighbour = secBlockData[rightIndex]
        if neighbour != blockID:
            return True

        #Check Z-1
        ngbIndex = (yBoff * 16 + (dZ-1)) * 16 + dX
        #ngbIndex = dY + ((dZ-1) << _Y_SHIFT) + (dX << _YZ_SHIFT)    #Check this lookup in readBlocks, below! Can it go o.o.b.?
        neighbour = secBlockData[ngbIndex]
        if neighbour != blockID:
            return True

        #Check Z+1
        ngbIndex = (yBoff * 16 + (dZ+1)) * 16 + dX
        #ngbIndex = dY + ((dZ+1) << _Y_SHIFT) + (dX << _YZ_SHIFT)    #Check this lookup in readBlocks, below! Can it go o.o.b.?
        neighbour = secBlockData[ngbIndex]
        if neighbour != blockID:
            return True

        return False


    #nb: 0 is bottom bedrock, 256 (255?) is top of sky. Sea is 64.
    def _readBlocks(chunkLevelData, vertexBuffer):
        """readBlocks(chunkLevelData) -> takes a named TAG_Compound 'Level' containing a chunk's Anvil Y-Sections, each of which 0-15 has blocks, data, heightmap, xpos,zpos, etc.
    Adds the data points into a 'vertexBuffer' which is a per-named-type dictionary of ????'s. That later is made into Blender geometry via from_pydata."""
        #TODO: also TileEntities and Entities. Entities will generally be an empty list.
        #TileEntities are needed for some things to define fully...

        #TODO: Keep an 'adjacent chunk cache' for neighbourhood is-exposed checks.

        global unknownBlockIDs, OPTIONS, REPORTING

        #chunkLocation = 'xPos' 'zPos' ...
        chunkX = chunkLevelData['xPos'].value
        chunkZ = chunkLevelData['zPos'].value
        biomes = chunkLevelData['Biomes'].value    #yields a TAG_Byte_Array value (bytes object) of len 256 (16x16)
        #heightmap = chunkLevelData['HeightMap'].value
        #'TileEntities' -- surely need this for piston data and stuff, no?

        entities = chunkLevelData['Entities'].value    # load ze sheeps!! # a list of tag-compounds.
        #omitmobs = OPTIONS['omitmobs']
        if not OPTIONS['omitmobs']:
            AnvilChunkReader._loadEntities(entities)

        skyHighLimit = OPTIONS['highlimit']
        depthLimit   = OPTIONS['lowlimit']

        CHUNKSIZE_X = 16
        CHUNKSIZE_Z = 16
        SECTNSIZE_Y = 16

        ##_Y_SHIFT = 7    # 2**7 is 128. use for fast multiply
        ##_YZ_SHIFT = 11    #16 * 128 is 2048, which is 2**11
        sections = chunkLevelData['Sections'].value

        #each section is a 16x16x16 piece of chunk, with a Y-byte from 0-15, so that the 'y' value is 16*that + in-section-Y-value

        #iterate through all block Y values from bedrock to max height (minor step through X,Z.)
        #bearing in mind some can be skipped out.

        #sectionDict => a dictionary of sections, indexed by Y.
        sDict = {}
        for section in sections:
            sY = section.value['Y'].value
            sDict[sY] = section.value

        for section in sections:
            sec = section.value
            secY = sec['Y'].value * SECTNSIZE_Y

            #if (secY + 16) < lowlimit, skip this section. no need to load it.
            if (secY+16 < depthLimit):
                continue

            if (secY > skyHighLimit):
                return

            #Now actually proceed with adding in the section's block data.
            blockData = sec['Blocks'].value    #yields a TAG_Byte_Array value (bytes object). Blocks is 16x16 bytes
            extraData = sec['Data'].value      #BlockLight, Data and SkyLight are 16x16 "4-bit cell" additional data arrays.

            #get starting Y from heightmap, ignoring excess height iterations...
            #heightByte = heightMap[dX + (dZ << 4)]    # z * 16
            #heightByte = 255    #quickFix: start from tip top, for now
            #if heightByte > skyHighLimit:
            #    heightByte = skyHighLimit

            #go y 0 to 16...
            for sy in range(16):
                dY = secY + sy

                if dY < depthLimit:
                    continue
                if dY > skyHighLimit:
                    return

                # dataX will be dX, blender X will be bX.
                for dZ in range(CHUNKSIZE_Z):
                    #print("looping chunk z %d" % dZ)
                    for dX in range(CHUNKSIZE_X):
                        #oneBlockLeft = 0   #data value of the block 1 back to the left (-X) from where we are now. (for neighbour comparisons)
                        #ie microcached 'last item read'. needs tweaked for chunk crossover...

                        ##blockIndex = (dZ << _Y_SHIFT) + (dX << _YZ_SHIFT)  # max number of bytes in a chunk is 32768. this is coming in at 32839 for XYZ: (15,71,8)
                        ##blockIndex = (dZ * 16) + dX
                        #YZX ((y * 16 + z) * 16 + x
                        blockIndex = (sy * 16 + dZ) * 16 + dX
                        blockID = blockData[ blockIndex ]

                        #except IndexError:
                        #    print("X:%d Y:%d Z %d, blockID from before: %d, cx,cz: %d,%d. Blockindex: %d" % (dX,dY,dZ,blockID,chunkX,chunkZ, blockIndex))
                        #    raise IndexError

                        #create this block in the output!
                        if blockID != 0 and blockID not in EXCLUDED_BLOCKS:    # 0 is air
                            REPORTING['blocksread'] += 1

                            #hollowness test:
                            if blockID in BLOCKDATA:
#                                if AnvilChunkReader._isExposedBlock((dX,dY,dZ), (chunkX, chunkZ), blockData, sDict, blockID, skyHighLimit, depthLimit):
                                #TODO: Make better version of this check, counting across chunks and regions.
                                    #Load extra data (if applicable to blockID):
                                    #if it has extra data, grab 4 bits from extraData
                                    datOffset = (int(blockIndex /2))    #divided by 2
                                    datHiBits = blockIndex % 2 #odd or even, will be hi or low nibble
                                    extraDatByte = extraData[datOffset] # should be a byte of which we only want part.
                                    hiMask = 0b11110000
                                    loMask = 0b00001111
                                    extraValue = None
                                    if datHiBits:
                                        #get high 4, and shift right 4.
                                        extraValue = loMask & (extraDatByte >> 4)
                                    else:
                                        #mask hi 4 off.
                                        extraValue = extraDatByte & loMask
                                    #create block in corresponding blockmesh
                                    AnvilChunkReader.createBlock(blockID, (chunkX, chunkZ), (dX,dY,dZ), extraValue, vertexBuffer)
#                                else:
 #                                   REPORTING['blocksdropped'] += 1
                            else:
                                #print("Unrecognised Block ID: %d" % blockID)
                                #createUnknownMeshBlock()
                                unknownBlockIDs.add(blockID)

        #TAG_Byte("Y"): 0
        #TAG_Byte_Array("Blocks"): [4096 bytes array]
        #TAG_Byte_Array("BlockLight"): [2048 bytes array]
        #TAG_Byte_Array("Data"): [2048 bytes array]
        #TAG_Byte_Array("SkyLight"): [2048 bytes array]
        ##TAG_Byte_Array("Add"): [2048 bytes array]     ##Only appears if it's needed!

    def _loadEntities(entities):
        global WORLD_ROOT
        for e in entities:
            eData = e.value

            etypename = eData['id'].value   #eg 'Sheep'
            ename = "en%sMarker" % etypename
            epos = [p.value for p in eData['Pos'].value]   #list[3] of double
            erot = [r.value for r in eData['Rotation'].value]  #list[2] of float ([0] orientation (angle round Z-axis) and [1] 0.00, probably y-tilt.

            #instantiate and rotate-in a placeholder object for this (and add to controlgroup or parent to something handy.)
            #translate to blend coords, too.
            entMarker = bpy.data.objects.new(ename, None)
            #set its coordinates...
            #convert Minecraft coordinate position of player into Blender coords:
            entMarker.location[0] = -epos[2]
            entMarker.location[1] = -epos[0]
            entMarker.location[2] = epos[1]

            #also, set its z-rotation to erot[0]...
            #entMarker.rotation[2] = erot[0]

            bpy.context.scene.objects.link(entMarker)
            entMarker.parent = WORLD_ROOT



##NB! Future blocks will require the Add tag to be checked and mixed in!
#Each section also has a "Add" tag, which is a DataLayer byte array just like
#"Data". The "Add" tag is not included in the converter since the old format
#never had block ids above 255. This extra tag is created whenever a block
#requires it, so the getTile() method needs to check if the array exists and
#then combine it with the default block data. In other words,
#blockId = (add << 8) + baseId.

        # Blocks, Data, Skylight, ... heightmap
        #Blocks contain the block ids; Data contains the extra info: 4 bits of lighting info + 4 bits of 'extra fields'
        # eg Lamp direction, crop wetness, etc.
        # Heightmap gives us quick access to the top surface of everything - ie optimise out iterating through all sky blocks.

        #To access a specific block from either the block or data array from XYZ coordinates, use the following formula:
        # Index = x + (y * Height + z) * Width

        ##Note that the old format is XZY ((x * 16 + z) * 16 + y) and the new format is YZX ((y * 16 + z) * 16 + x)

        #16x16 (256) ints of heightmap data. Each int records the lowest level
        #in each column where the light from the sky is at full strength. Speeds up
        #computing of the SkyLight. Note: This array's indexes are ordered Z,X
        #whereas the other array indexes are ordered X,Z,Y.

        #loadedData -> we buffer everything into lists, then batch-create the
        #vertices later. This makes the model build in Blender many, many times faster

        #list of named, distinct material meshes. add vertices to each, only in batches.
        #Optimisation: 'Hollow volumes': only add if there is at least 1 orthogonal non-same-type neighbour.
        #Aggressive optimisation: only load if there is 1 air orthogonal neighbour (or transparent materials).





#    def mcToBlendCoord(chunkPos, blockPos):
#        """Converts a minecraft chunk X,Z pair and a minecraft ordered X,Y,Z block location triple into a Blender coordinate vector Vx,Vy,Vz.
#    And remember: in Minecraft, Y points to the sky."""

        # Mapping Minecraft coords -> Blender coords
        # In Minecraft, +Z (west) <--- 0 ----> -Z (east), while North is -X and South is +X
        # In Blender, north is +Y, south is-Y, west is -X and east is +X.
        # So negate Z and map it as X, and negate X and map it as Y. It's slightly odd!

#        vx = -(chunkPos[1] << 4) - blockPos[2]
#        vy = -(chunkPos[0] << 4) - blockPos[0]   # -x of chunkpos and -x of blockPos (x,y,z)
#        vz = blockPos[1]    #Minecraft's Y.

#        return Vector((vx,vy,vz))

    def createBlock(blockID, chunkPos, blockPos, extraBlockData, vertBuffer):
        """adds a vertex to the blockmesh for blockID in the relevant location."""
        MTBlockKey = blockID
        print("AnvilChunkReader.createBlock:" + " chunkPos:" + str(chunkPos) + " blockPos:" + str(blockPos) + " blockID:" + str(blockID) 
            + " extraBlockData:" + str(extraBlockData) + " MTBlockKey:" + str(MTBlockKey) + " MTblock:" + MC2MTdict2[MTBlockKey][0] + " --> "+ MC2MTdict2[MTBlockKey][3])


#         print("AnvilChunkReader.createBlock")
#         print("blockID: " + str(blockID))
#         print("chunkPos: " + str(chunkPos))
#         print("blockPos: " + str(blockPos))
#         print("extraBlockData: " + str(extraBlockData))
# 
# #        MTBlockKey = str('00'+str(blockID))[-3:]+'.'+str(100+extraBlockData)[-2:]
#         MTBlockKey = blockID
#         print("MTBlockKey: " + str(MTBlockKey))
# 
#         print("MTblock: " + MC2MTdict2[MTBlockKey][0] + " --> "+ MC2MTdict2[MTBlockKey][3])
# 
#         print("")
#        print("vertBuffer: " + str(vertBuffer))

#         chunkpos is X,Z; blockpos is x,y,z for block.
#         mesh = getMCBlockType(blockID, extraBlockData)  #this could be inefficient. Perhaps create all the types at the start, then STOP MAKING THIS CHECK!
#         if mesh is None:
#             return
#
#         typeName = mesh.name
#         vertex = mcToBlendCoord(chunkPos, blockPos)
#
#         if typeName in vertBuffer:
#             vertBuffer[typeName].append(vertex)
#         else:
#             vertBuffer[typeName] = [vertex]

        #xyz is local to the 'stone' mesh for example. but that's from 0 (world).
        #regionfile can be found from chunkPos.
        #Chunkpos is an X,Z pair.
        #Blockpos is an X,Y,Z triple - within chunk.
