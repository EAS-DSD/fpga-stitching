#!/usr/bin/env python3

# Copyright (c) 2024 Leo Moser <leomoser99@gmail.com>
# SPDX-License-Identifier: Apache-2.0

import generate_fabrics

config_template = """FabricBegin
{fabric}
FabricEnd
ParametersBegin
ConfigBitMode,frame_based,# default is FlipFlopChain,,frame_based
GenerateDelayInSwitchMatrix,80
MultiplexerStyle,custom,#,custom,generic
SuperTileEnable,TRUE,#,TRUE,FALSE

Tile,../Tile/LUT4AB/LUT4AB.csv
Tile,../Tile/N_term_single/N_term_single.csv
Tile,../Tile/S_term_single/S_term_single.csv
Tile,../Tile/N_IO/N_IO.csv
Tile,../Tile/E_IO/E_IO.csv
Tile,../Tile/S_IO/S_IO.csv
Tile,../Tile/W_IO/W_IO.csv

ParametersEnd
"""

def main(width=100, height=100, filename='configs/fabric_custom.csv'):
    
    fabric = ''
    fabric += f'NULL,{"N_term_single,"*width}NULL\n'
    
    for _ in range(height):
        fabric += f'W_IO,{"LUT4AB,"*width}E_IO\n'

    fabric += f'NULL,{"S_term_single,"*width}NULL\n'

    with open(filename, 'w') as f:
        f.write(config_template.format(fabric=fabric))

if __name__ == "__main__":

    fabric_sizes = [1,2,3,4,5,7,9,11,13,15,20,25,30]

    for i in fabric_sizes:
        main(i, i, f'configs/fabric{i}x{i}.csv')
        generate_fabrics.gen_fabric(f'configs/fabric{i}x{i}.csv', f'fabrics_nl/fabric{i}x{i}.v', 'Tile/')
