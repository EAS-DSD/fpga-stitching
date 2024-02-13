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

    pins_fabric_north = [
        'UserCLKo'
    ]

    pins_fabric_south = [
        'UserCLK'
    ]

    pins_fabric_east = [
    
    ]

    pins_fabric_west = [
        'E1END[0]', 'E1END[1]', 'E1END[2]', 'E1END[3]',
        'E2MID[0]', 'E2MID[1]', 'E2MID[2]', 'E2MID[3]', 'E2MID[4]', 'E2MID[5]', 'E2MID[6]', 'E2MID[7]',
        'E2END[0]', 'E2END[1]', 'E2END[2]', 'E2END[3]', 'E2END[4]', 'E2END[5]', 'E2END[6]', 'E2END[7]',
        'EE4END[0]', 'EE4END[1]', 'EE4END[2]', 'EE4END[3]', 'EE4END[4]', 'EE4END[5]', 'EE4END[6]', 'EE4END[7]', 'EE4END[8]', 'EE4END[9]', 'EE4END[10]', 'EE4END[11]', 'EE4END[12]', 'EE4END[13]', 'EE4END[14]', 'EE4END[15]',
        'E6END[0]', 'E6END[1]', 'E6END[2]', 'E6END[3]', 'E6END[4]', 'E6END[5]', 'E6END[6]', 'E6END[7]', 'E6END[8]', 'E6END[9]', 'E6END[10]', 'E6END[11]',
    
        'W1BEG[0]', 'W1BEG[1]', 'W1BEG[2]', 'W1BEG[3]',
        'W2BEG[0]', 'W2BEG[1]', 'W2BEG[2]', 'W2BEG[3]', 'W2BEG[4]', 'W2BEG[5]', 'W2BEG[6]', 'W2BEG[7]',
        'W2BEGb[0]', 'W2BEGb[1]', 'W2BEGb[2]', 'W2BEGb[3]', 'W2BEGb[4]', 'W2BEGb[5]', 'W2BEGb[6]', 'W2BEGb[7]',
        'WW4BEG[0]', 'WW4BEG[1]', 'WW4BEG[2]', 'WW4BEG[3]', 'WW4BEG[4]', 'WW4BEG[5]', 'WW4BEG[6]', 'WW4BEG[7]', 'WW4BEG[8]', 'WW4BEG[9]', 'WW4BEG[10]', 'WW4BEG[11]', 'WW4BEG[12]', 'WW4BEG[13]', 'WW4BEG[14]', 'WW4BEG[15]',
        'W6BEG[0]', 'W6BEG[1]', 'W6BEG[2]', 'W6BEG[3]', 'W6BEG[4]', 'W6BEG[5]', 'W6BEG[6]', 'W6BEG[7]', 'W6BEG[8]', 'W6BEG[9]', 'W6BEG[10]', 'W6BEG[11]'
    ]

    pins_config_in = [
        'FrameData[0]', 'FrameData[1]', 'FrameData[2]', 'FrameData[3]', 'FrameData[4]', 'FrameData[5]', 'FrameData[6]', 'FrameData[7]', 'FrameData[8]', 'FrameData[9]', 'FrameData[10]', 'FrameData[11]', 'FrameData[12]', 'FrameData[13]', 'FrameData[14]', 'FrameData[15]', 'FrameData[16]', 'FrameData[17]', 'FrameData[18]', 'FrameData[19]', 'FrameData[20]', 'FrameData[21]', 'FrameData[22]', 'FrameData[23]', 'FrameData[24]', 'FrameData[25]', 'FrameData[26]', 'FrameData[27]', 'FrameData[28]', 'FrameData[29]', 'FrameData[30]', 'FrameData[31]',

        'FrameStrobe[0]', 'FrameStrobe[1]', 'FrameStrobe[2]', 'FrameStrobe[3]', 'FrameStrobe[4]', 'FrameStrobe[5]', 'FrameStrobe[6]', 'FrameStrobe[7]', 'FrameStrobe[8]', 'FrameStrobe[9]', 'FrameStrobe[10]', 'FrameStrobe[11]', 'FrameStrobe[12]', 'FrameStrobe[13]', 'FrameStrobe[14]', 'FrameStrobe[15]', 'FrameStrobe[16]', 'FrameStrobe[17]', 'FrameStrobe[18]', 'FrameStrobe[19]'
    ]
    
    pins_config_out = [
        'FrameData_O[0]', 'FrameData_O[1]', 'FrameData_O[2]', 'FrameData_O[3]', 'FrameData_O[4]', 'FrameData_O[5]', 'FrameData_O[6]', 'FrameData_O[7]', 'FrameData_O[8]', 'FrameData_O[9]', 'FrameData_O[10]', 'FrameData_O[11]', 'FrameData_O[12]', 'FrameData_O[13]', 'FrameData_O[14]', 'FrameData_O[15]', 'FrameData_O[16]', 'FrameData_O[17]', 'FrameData_O[18]', 'FrameData_O[19]', 'FrameData_O[20]', 'FrameData_O[21]', 'FrameData_O[22]', 'FrameData_O[23]', 'FrameData_O[24]', 'FrameData_O[25]', 'FrameData_O[26]', 'FrameData_O[27]', 'FrameData_O[28]', 'FrameData_O[29]', 'FrameData_O[30]', 'FrameData_O[31]',

        'FrameStrobe_O[0]', 'FrameStrobe_O[1]', 'FrameStrobe_O[2]', 'FrameStrobe_O[3]', 'FrameStrobe_O[4]', 'FrameStrobe_O[5]', 'FrameStrobe_O[6]', 'FrameStrobe_O[7]', 'FrameStrobe_O[8]', 'FrameStrobe_O[9]', 'FrameStrobe_O[10]', 'FrameStrobe_O[11]', 'FrameStrobe_O[12]', 'FrameStrobe_O[13]', 'FrameStrobe_O[14]', 'FrameStrobe_O[15]', 'FrameStrobe_O[16]', 'FrameStrobe_O[17]', 'FrameStrobe_O[18]', 'FrameStrobe_O[19]'
    ]

    pins_io = ['A_I_top', 'A_O_top', 'A_T_top', 'B_I_top', 'B_O_top', 'B_T_top']

    pins_config_top = ['A_config_C_bit0', 'A_config_C_bit1', 'A_config_C_bit2', 'A_config_C_bit3', 'B_config_C_bit0', 'B_config_C_bit1', 'B_config_C_bit2', 'B_config_C_bit3']

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
    
    # Place I/O pins
    bterms_io = []
    for pin in pins_io:
        bterms_io.append(bterm_map.pop(pin))
    place_pins_central(die_area, layer_fabric, bterms_io, 'E')

    # Place top config pins
    bterms_config_top = []
    for i, pin in enumerate(pins_config_top):
        bterms_config_top.append(bterm_map.pop(pin))
    place_pins_central(die_area, layer_config, bterms_config_top, 'E')

if __name__ == "__main__":
    io_place()
