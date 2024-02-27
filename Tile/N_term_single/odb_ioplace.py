import os
import sys
import click
import itertools

from reader import click_odb, click

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from odb_helper import place_pin, place_pins_central

@click.command()
@click_odb
def io_place(reader):

    # Terminal name mapping
    bterm_map = {b.getName(): b for b in reader.block.getBTerms()}

    # Find die & layers
    die_area = reader.block.getDieArea()
    layer_fabric = reader.tech.findLayer("met3")
    layer_config = reader.tech.findLayer("met2")
    
    pins_fabric_north = [
        'UserCLKo'
    ]
    
    pins_fabric_south = list(itertools.chain(
        [
            'UserCLK',
            'Ci',
        ],
        [f'N1END[{bit}]' for bit in range(4)],
        [f'N2MID[{bit}]' for bit in range(8)],
        [f'N2END[{bit}]' for bit in range(8)],
        [f'N4END[{bit}]' for bit in range(16)],
        [f'NN4END[{bit}]' for bit in range(16)],
        
        [f'S1BEG[{bit}]' for bit in range(4)],
        [f'S2BEG[{bit}]' for bit in range(8)],
        [f'S2BEGb[{bit}]' for bit in range(8)],
        [f'S4BEG[{bit}]' for bit in range(16)],
        [f'SS4BEG[{bit}]' for bit in range(16)]
    ))
    
    pins_fabric_east = [
    
    ]

    pins_fabric_west = [

    ]

    pins_framestrobe_in = [f'FrameStrobe[{bit}]' for bit in range(20)]
    
    pins_framestrobe_out = [f'FrameStrobe_O[{bit}]' for bit in range(20)]

    # Place fabric pins
    bterms_north = []
    for pin in pins_fabric_north:
        bterms_north.append(bterm_map.pop(pin))
    place_pins_central(die_area, layer_fabric, bterms_north, 'N')

    bterms_east = []
    for pin in pins_fabric_east:
        bterms_east.append(bterm_map.pop(pin))
    place_pins_central(die_area, layer_fabric, bterms_east, 'E')
    
    bterms_south = []
    for pin in pins_fabric_south:
        bterms_south.append(bterm_map.pop(pin))
    place_pins_central(die_area, layer_fabric, bterms_south, 'S')
    
    bterms_west = []
    for pin in pins_fabric_west:
        bterms_west.append(bterm_map.pop(pin))
    place_pins_central(die_area, layer_fabric, bterms_west, 'W')

    # Place configuration pins
    bterms_framestrobe_in = []
    for pin in pins_framestrobe_in:
        bterms_framestrobe_in.append(bterm_map.pop(pin))
    place_pins_central(die_area, layer_config, bterms_framestrobe_in, 'S')
    
    bterms_framestrobe_out = []
    for pin in pins_framestrobe_out:
        bterms_framestrobe_out.append(bterm_map.pop(pin))
    place_pins_central(die_area, layer_config, bterms_framestrobe_out, 'N')

if __name__ == "__main__":
    io_place()
