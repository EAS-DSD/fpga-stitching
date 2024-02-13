import os
import sys
import click

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
    
    pins_fabric_north = [
        'UserCLKo'
    ]
    
    pins_fabric_south = [
        'UserCLK',
        
        'Ci',
        
        'N1END[0]', 'N1END[1]', 'N1END[2]', 'N1END[3]',
        'N2MID[0]', 'N2MID[1]', 'N2MID[2]', 'N2MID[3]', 'N2MID[4]', 'N2MID[5]', 'N2MID[6]', 'N2MID[7]',
        'N2END[0]', 'N2END[1]', 'N2END[2]', 'N2END[3]', 'N2END[4]', 'N2END[5]', 'N2END[6]', 'N2END[7]',
        'N4END[0]', 'N4END[1]', 'N4END[2]', 'N4END[3]', 'N4END[4]', 'N4END[5]', 'N4END[6]', 'N4END[7]', 'N4END[8]', 'N4END[9]', 'N4END[10]', 'N4END[11]', 'N4END[12]', 'N4END[13]', 'N4END[14]', 'N4END[15]',
        'NN4END[0]', 'NN4END[1]', 'NN4END[2]', 'NN4END[3]', 'NN4END[4]', 'NN4END[5]', 'NN4END[6]', 'NN4END[7]', 'NN4END[8]', 'NN4END[9]', 'NN4END[10]', 'NN4END[11]', 'NN4END[12]', 'NN4END[13]', 'NN4END[14]', 'NN4END[15]',
    
        'S1BEG[0]', 'S1BEG[1]', 'S1BEG[2]', 'S1BEG[3]',
        'S2BEG[0]', 'S2BEG[1]', 'S2BEG[2]', 'S2BEG[3]', 'S2BEG[4]', 'S2BEG[5]', 'S2BEG[6]', 'S2BEG[7]',
        'S2BEGb[0]', 'S2BEGb[1]', 'S2BEGb[2]', 'S2BEGb[3]', 'S2BEGb[4]', 'S2BEGb[5]', 'S2BEGb[6]', 'S2BEGb[7]',
        'S4BEG[0]', 'S4BEG[1]', 'S4BEG[2]', 'S4BEG[3]', 'S4BEG[4]', 'S4BEG[5]', 'S4BEG[6]', 'S4BEG[7]', 'S4BEG[8]', 'S4BEG[9]', 'S4BEG[10]', 'S4BEG[11]', 'S4BEG[12]', 'S4BEG[13]', 'S4BEG[14]', 'S4BEG[15]',
        'SS4BEG[0]', 'SS4BEG[1]', 'SS4BEG[2]', 'SS4BEG[3]', 'SS4BEG[4]', 'SS4BEG[5]', 'SS4BEG[6]', 'SS4BEG[7]', 'SS4BEG[8]', 'SS4BEG[9]', 'SS4BEG[10]', 'SS4BEG[11]', 'SS4BEG[12]', 'SS4BEG[13]', 'SS4BEG[14]', 'SS4BEG[15]'
    ]
    
    pins_fabric_east = [
    
    ]

    pins_fabric_west = [

    ]

    pins_config_in = [
        'FrameStrobe[0]', 'FrameStrobe[1]', 'FrameStrobe[2]', 'FrameStrobe[3]', 'FrameStrobe[4]', 'FrameStrobe[5]', 'FrameStrobe[6]', 'FrameStrobe[7]', 'FrameStrobe[8]', 'FrameStrobe[9]', 'FrameStrobe[10]', 'FrameStrobe[11]', 'FrameStrobe[12]', 'FrameStrobe[13]', 'FrameStrobe[14]', 'FrameStrobe[15]', 'FrameStrobe[16]', 'FrameStrobe[17]', 'FrameStrobe[18]', 'FrameStrobe[19]'
    ]
    
    pins_config_out = [
        'FrameStrobe_O[0]', 'FrameStrobe_O[1]', 'FrameStrobe_O[2]', 'FrameStrobe_O[3]', 'FrameStrobe_O[4]', 'FrameStrobe_O[5]', 'FrameStrobe_O[6]', 'FrameStrobe_O[7]', 'FrameStrobe_O[8]', 'FrameStrobe_O[9]', 'FrameStrobe_O[10]', 'FrameStrobe_O[11]', 'FrameStrobe_O[12]', 'FrameStrobe_O[13]', 'FrameStrobe_O[14]', 'FrameStrobe_O[15]', 'FrameStrobe_O[16]', 'FrameStrobe_O[17]', 'FrameStrobe_O[18]', 'FrameStrobe_O[19]'
    ]

    pin_interdistance = 3500

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
    bterms_config_in = []
    for pin in pins_config_in:
        bterms_config_in.append(bterm_map.pop(pin))
    place_pins_central(die_area, layer_config, bterms_config_in, 'S')
    
    bterms_config_out = []
    for pin in pins_config_out:
        bterms_config_out.append(bterm_map.pop(pin))
    place_pins_central(die_area, layer_config, bterms_config_out, 'N')

if __name__ == "__main__":
    io_place()
