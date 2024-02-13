import os
import sys
import click

from reader import click_odb, click

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from odb_helper import place_pin

@click.command()
@click_odb
def io_place(reader):

    print(reader.block.getBTerms())

    # Terminal name mapping
    bterm_map = {b.getName(): b for b in reader.block.getBTerms()}

    names = [key for key in bterm_map]
    
    print(names)

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
        'E1BEG[0]', 'E1BEG[1]', 'E1BEG[2]', 'E1BEG[3]',
        'E2BEG[0]', 'E2BEG[1]', 'E2BEG[2]', 'E2BEG[3]', 'E2BEG[4]', 'E2BEG[5]', 'E2BEG[6]', 'E2BEG[7]',
        'E2BEGb[0]', 'E2BEGb[1]', 'E2BEGb[2]', 'E2BEGb[3]', 'E2BEGb[4]', 'E2BEGb[5]', 'E2BEGb[6]', 'E2BEGb[7]',
        'EE4BEG[0]', 'EE4BEG[1]', 'EE4BEG[2]', 'EE4BEG[3]', 'EE4BEG[4]', 'EE4BEG[5]', 'EE4BEG[6]', 'EE4BEG[7]', 'EE4BEG[8]', 'EE4BEG[9]', 'EE4BEG[10]', 'EE4BEG[11]', 'EE4BEG[12]', 'EE4BEG[13]', 'EE4BEG[14]', 'EE4BEG[15]',
        'E6BEG[0]', 'E6BEG[1]', 'E6BEG[2]', 'E6BEG[3]', 'E6BEG[4]', 'E6BEG[5]', 'E6BEG[6]', 'E6BEG[7]', 'E6BEG[8]', 'E6BEG[9]', 'E6BEG[10]', 'E6BEG[11]',
        
        'W1END[0]', 'W1END[1]', 'W1END[2]', 'W1END[3]',
        'W2MID[0]', 'W2MID[1]', 'W2MID[2]', 'W2MID[3]', 'W2MID[4]', 'W2MID[5]', 'W2MID[6]', 'W2MID[7]',
        'W2END[0]', 'W2END[1]', 'W2END[2]', 'W2END[3]', 'W2END[4]', 'W2END[5]', 'W2END[6]', 'W2END[7]',
        'WW4END[0]', 'WW4END[1]', 'WW4END[2]', 'WW4END[3]', 'WW4END[4]', 'WW4END[5]', 'WW4END[6]', 'WW4END[7]', 'WW4END[8]', 'WW4END[9]', 'WW4END[10]', 'WW4END[11]', 'WW4END[12]', 'WW4END[13]', 'WW4END[14]', 'WW4END[15]',
        'W6END[0]', 'W6END[1]', 'W6END[2]', 'W6END[3]', 'W6END[4]', 'W6END[5]', 'W6END[6]', 'W6END[7]', 'W6END[8]', 'W6END[9]', 'W6END[10]', 'W6END[11]'
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

    pin_interdistance = 3500

    # Place fabric pins
    for i, pin in enumerate(pins_fabric_north):
        place_pin(die_area, layer_fabric, bterm_map.pop(pin), pin_interdistance * (i+1), 'N')

    for i, pin in enumerate(pins_fabric_east):
        place_pin(die_area, layer_fabric, bterm_map.pop(pin), pin_interdistance * (i+1), 'E')
        
    for i, pin in enumerate(pins_fabric_south):
        place_pin(die_area, layer_fabric, bterm_map.pop(pin), pin_interdistance * (i+1), 'S')
        
    for i, pin in enumerate(pins_fabric_west):
        place_pin(die_area, layer_fabric, bterm_map.pop(pin), pin_interdistance * (i+1), 'W')

    # Place configuration pins
    for i, pin in enumerate(pins_config_in):
        place_pin(die_area, layer_config, bterm_map.pop(pin), pin_interdistance * (i+1), 'S')
    
    for i, pin in enumerate(pins_config_out):
        place_pin(die_area, layer_config, bterm_map.pop(pin), pin_interdistance * (i+1), 'N')

if __name__ == "__main__":
    io_place()
