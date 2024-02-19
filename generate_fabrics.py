#!/usr/bin/env python3

import os
import sys

os.environ["FAB_ROOT"] = '/home/leo/Projects/FABulous'
sys.path.append('/home/leo/Projects/FABulous')

from FABulous import *

def do_gen_tile(fabricGen, projectDir, args):
        "Generate the given tile with the switch matrix and configuration memory"
        logger.info(f"Generating tile {' '.join(args)}")
        for t in args:

            # Gen switch matrix
            fabricGen.setWriterOutputFile(f"{projectDir}/{t}/{t}_switch_matrix.v")
            fabricGen.genSwitchMatrix(t)

            # Gen config mem
            fabricGen.setWriterOutputFile(f"{projectDir}/{t}/{t}_ConfigMem.v")
            fabricGen.genConfigMem(t, f"{projectDir}/{t}/{t}_ConfigMem.csv")

            logger.info(f"Generating tile {t}")
            # Gen tile
            fabricGen.setWriterOutputFile(f"{projectDir}/{t}/{t}.v")
            fabricGen.genTile(t)
            logger.info(f"Generated tile {t}")

        logger.info("Tile generation complete")


def gen_fabric(csv_file, output_file, tile_path):
    my_fabric = FABulous(VerilogWriter(), csv_file)

    # TODO Should this not check that the tiles are available in Tile/ ?
    #tileByPath = [f.name for f in os.scandir(f"{projectDir}/Tile/") if f.is_dir()]
    tileByFabric = list(my_fabric.fabric.tileDic.keys())
    superTileByFabric = list(my_fabric.fabric.superTileDic.keys())
    #allTile = list(set(tileByPath) & set(tileByFabric + superTileByFabric))
    allTile = list(set(tileByFabric + superTileByFabric))

    print(f'Tiles used by fabric: {allTile}')

    do_gen_tile(my_fabric, tile_path, allTile)
    
    my_fabric.setWriterOutputFile(output_file) # my_fabric.fabric.name
    my_fabric.genFabric()

def main():
    os.makedirs("fabrics_nl/", exist_ok=True)

    gen_fabric('configs/fabric_small.csv', 'fabrics_nl/fabric_small.v', 'Tile/')
    gen_fabric('configs/fabric_medium.csv', 'fabrics_nl/fabric_medium.v', 'Tile/')
    gen_fabric('configs/fabric_large.csv', 'fabrics_nl/fabric_large.v', 'Tile/')

if __name__ == "__main__":
    main()
