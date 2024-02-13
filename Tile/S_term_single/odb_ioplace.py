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
        'UserCLKo',
        
        'Co',
    
        'N1BEG[0]', 'N1BEG[1]', 'N1BEG[2]', 'N1BEG[3]',
        'N2BEG[0]', 'N2BEG[1]', 'N2BEG[2]', 'N2BEG[3]', 'N2BEG[4]', 'N2BEG[5]', 'N2BEG[6]', 'N2BEG[7]',
        'N2BEGb[0]', 'N2BEGb[1]', 'N2BEGb[2]', 'N2BEGb[3]', 'N2BEGb[4]', 'N2BEGb[5]', 'N2BEGb[6]', 'N2BEGb[7]',
        'N4BEG[0]', 'N4BEG[1]', 'N4BEG[2]', 'N4BEG[3]', 'N4BEG[4]', 'N4BEG[5]', 'N4BEG[6]', 'N4BEG[7]', 'N4BEG[8]', 'N4BEG[9]', 'N4BEG[10]', 'N4BEG[11]', 'N4BEG[12]', 'N4BEG[13]', 'N4BEG[14]', 'N4BEG[15]',
        'NN4BEG[0]', 'NN4BEG[1]', 'NN4BEG[2]', 'NN4BEG[3]', 'NN4BEG[4]', 'NN4BEG[5]', 'NN4BEG[6]', 'NN4BEG[7]', 'NN4BEG[8]', 'NN4BEG[9]', 'NN4BEG[10]', 'NN4BEG[11]', 'NN4BEG[12]', 'NN4BEG[13]', 'NN4BEG[14]', 'NN4BEG[15]',
        
        'S1END[0]', 'S1END[1]', 'S1END[2]', 'S1END[3]',
        'S2MID[0]', 'S2MID[1]', 'S2MID[2]', 'S2MID[3]', 'S2MID[4]', 'S2MID[5]', 'S2MID[6]', 'S2MID[7]',
        'S2END[0]', 'S2END[1]', 'S2END[2]', 'S2END[3]', 'S2END[4]', 'S2END[5]', 'S2END[6]', 'S2END[7]',
        'S4END[0]', 'S4END[1]', 'S4END[2]', 'S4END[3]', 'S4END[4]', 'S4END[5]', 'S4END[6]', 'S4END[7]', 'S4END[8]', 'S4END[9]', 'S4END[10]', 'S4END[11]', 'S4END[12]', 'S4END[13]', 'S4END[14]', 'S4END[15]',
        'SS4END[0]', 'SS4END[1]', 'SS4END[2]', 'SS4END[3]', 'SS4END[4]', 'SS4END[5]', 'SS4END[6]', 'SS4END[7]', 'SS4END[8]', 'SS4END[9]', 'SS4END[10]', 'SS4END[11]', 'SS4END[12]', 'SS4END[13]', 'SS4END[14]', 'SS4END[15]'
    ]
    
    pins_fabric_south = [
        'UserCLK'
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
