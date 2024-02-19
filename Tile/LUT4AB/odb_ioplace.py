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
    layer_fabric = reader.tech.findLayer("met4")
    layer_config = reader.tech.findLayer("met3")
    
    # Note: all begins all correct, all ends are opposite
    
    print([f'N1BEG[{bit}]' for bit in range(4)])
    
    pins_fabric_north = list(itertools.chain(
        [
            'UserCLKo',
            'Co'
        ],
        [f'N1BEG[{bit}]' for bit in range(4)],
        [f'N2BEG[{bit}]' for bit in range(8)],
        [f'N2BEGb[{bit}]' for bit in range(8)],
        [f'N4BEG[{bit}]' for bit in range(16)],
        [f'NN4BEG[{bit}]' for bit in range(16)],
        
        [f'S1END[{bit}]' for bit in range(4)],
        [f'S2MID[{bit}]' for bit in range(8)],
        [f'S2END[{bit}]' for bit in range(8)],
        [f'S4END[{bit}]' for bit in range(16)],
        [f'SS4END[{bit}]' for bit in range(16)]
    ))
    
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
    
    pins_fabric_east = list(itertools.chain(
        [f'E1BEG[{bit}]' for bit in range(4)],
        [f'E2BEG[{bit}]' for bit in range(8)],
        [f'E2BEGb[{bit}]' for bit in range(8)],
        [f'EE4BEG[{bit}]' for bit in range(16)],
        [f'E6BEG[{bit}]' for bit in range(12)],
        
        [f'W1END[{bit}]' for bit in range(4)],
        [f'W2MID[{bit}]' for bit in range(8)],
        [f'W2END[{bit}]' for bit in range(8)],
        [f'WW4END[{bit}]' for bit in range(16)],
        [f'W6END[{bit}]' for bit in range(12)]
    ))
    
    pins_fabric_west = list(itertools.chain(
        [f'E1END[{bit}]' for bit in range(4)],
        [f'E2MID[{bit}]' for bit in range(8)],
        [f'E2END[{bit}]' for bit in range(8)],
        [f'EE4END[{bit}]' for bit in range(16)],
        [f'E6END[{bit}]' for bit in range(12)],
        
        [f'W1BEG[{bit}]' for bit in range(4)],
        [f'W2BEG[{bit}]' for bit in range(8)],
        [f'W2BEGb[{bit}]' for bit in range(8)],
        [f'WW4BEG[{bit}]' for bit in range(16)],
        [f'W6BEG[{bit}]' for bit in range(12)]
    ))

    pins_framedata_in = [f'FrameData[{bit}]' for bit in range(32)]
    
    pins_framedata_out = [f'FrameData_O[{bit}]' for bit in range(32)]
    
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
    
    bterms_framedata_in = []
    for pin in pins_framedata_in:
        bterms_framedata_in.append(bterm_map.pop(pin))
    place_pins_central(die_area, layer_config, bterms_framedata_in, 'W')
    
    bterms_framestrobe_out = []
    for pin in pins_framedata_out:
        bterms_framestrobe_out.append(bterm_map.pop(pin))
    place_pins_central(die_area, layer_config, bterms_framestrobe_out, 'E')

if __name__ == "__main__":
    io_place()
