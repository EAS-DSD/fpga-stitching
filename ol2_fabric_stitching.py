#!/usr/bin/env python3

# Copyright (c) 2024 Leo Moser <leomoser99@gmail.com>
# SPDX-License-Identifier: Apache-2.0

import os
import sys
import time
import argparse
import resource

from common import TILE_WIDTH, TILE_HEIGHT, SPACING, HALO_SPACING

from typing import List, Type

from openlane.flows.misc import OpenInKLayout
from openlane.flows.misc import OpenInOpenROAD
from openlane.flows.sequential import SequentialFlow
from openlane.steps.odb import OdbpyStep
from openlane.steps import (
    Step,
    Yosys,
    OpenROAD,
    Magic,
    Misc,
    KLayout,
    Odb,
    Netgen,
    Checker,
)

class TopFlow(SequentialFlow):

    Steps: List[Type[Step]] = [
        Yosys.JsonHeader,
        Yosys.Synthesis,
        Checker.YosysUnmappedCells,
        Checker.YosysSynthChecks,
        OpenROAD.CheckSDCFiles,
        OpenROAD.Floorplan,
        #Odb.ApplyDEFTemplate,
        Odb.SetPowerConnections,
        Odb.ManualMacroPlacement,
        OpenROAD.IOPlacement,
        OpenROAD.GlobalPlacement,
        Odb.AddPDNObstructions,
        OpenROAD.GeneratePDN,
        Odb.RemovePDNObstructions,
        Checker.PowerGridViolations,
        OpenROAD.DetailedPlacement,
        #CustomRoute,
        OpenROAD.GlobalRouting,
        OpenROAD.DetailedRouting,
        Checker.TrDRC,
        Odb.ReportDisconnectedPins,
        Checker.DisconnectedPins,
        Odb.ReportWireLength,
        Checker.WireLength,
        OpenROAD.RCX,
        OpenROAD.STAPostPNR,
        OpenROAD.IRDropReport,
        Magic.StreamOut,
        KLayout.StreamOut,
        Magic.WriteLEF,
        KLayout.XOR,
        Checker.XOR,
        Magic.DRC,
        KLayout.DRC,
        Checker.MagicDRC,
        Checker.KLayoutDRC,
        Magic.SpiceExtraction,
        Checker.IllegalOverlap,
        Netgen.LVS,
        Checker.LVS,
        Checker.SetupViolations,
        Checker.HoldViolations,
        Misc.ReportManufacturability
    ]

def main(tiles_path, fabric_name, output_dir, FABRIC_NUM_TILES_X=2, FABRIC_NUM_TILES_Y=2):
    
    t_process = time.process_time()
    t_perf_counter = time.perf_counter()

    fabric_path = os.path.join(output_dir, f'{fabric_name}.v')

    # Get environment variables
    PDK_ROOT          = os.getenv('PDK_ROOT')
    PDK               = os.getenv('PDK_ROOT', 'sky130A')
    SCL               = os.getenv('SCL')
    OPEN_IN_KLAYOUT   = os.getenv('OPEN_IN_KLAYOUT')
    OPEN_IN_OPENROAD  = os.getenv('OPEN_IN_OPENROAD')
    NO_CHECKS         = os.getenv('NO_CHECKS')

    if NO_CHECKS:
        TopFlow.Steps.remove(OpenROAD.STAPostPNR)
        TopFlow.Steps.remove(KLayout.XOR)
        TopFlow.Steps.remove(Checker.XOR)
        TopFlow.Steps.remove(Magic.DRC)
        TopFlow.Steps.remove(KLayout.DRC)
        TopFlow.Steps.remove(Checker.MagicDRC)
        TopFlow.Steps.remove(Checker.KLayoutDRC)
        TopFlow.Steps.remove(Magic.SpiceExtraction)
        TopFlow.Steps.remove(Checker.IllegalOverlap)
        TopFlow.Steps.remove(Netgen.LVS)
        TopFlow.Steps.remove(Checker.LVS)

    verilog_files = [
        fabric_path
    ]
    
    # TODO PDN connections?
    
    # Create macro configurations
    macro_names = ['LUT4AB', 'E_IO', 'W_IO', 'N_term_single', 'S_term_single']
    macros = {}
    
    for macro_name in macro_names:
        macros[macro_name] = {
            'gds': [ f'{tiles_path}/{macro_name}/macro/gds/{macro_name}.gds'],
            'lef': [ f'{tiles_path}/{macro_name}/macro/lef/{macro_name}.lef'],
            'nl': [ f'{tiles_path}/{macro_name}/macro/nl/{macro_name}.nl.v'],
            'spef': {
                'min_*': [ f'{tiles_path}/{macro_name}/macro/spef/{macro_name}.min.spef' ],
                'nom_*': [ f'{tiles_path}/{macro_name}/macro/spef/{macro_name}.nom.spef' ],
                'max_*': [ f'{tiles_path}/{macro_name}/macro/spef/{macro_name}.max.spef' ],
            },
            'instances': { }
        }
    
    # Place macros
    TILE_WIDTH_SMALL  = TILE_WIDTH//2
    TILE_HEIGHT_SMALL = TILE_HEIGHT//2
    
    FABRIC_WIDTH  = FABRIC_NUM_TILES_X * (TILE_WIDTH + SPACING) + 2 * (TILE_WIDTH_SMALL + SPACING) + 2 * HALO_SPACING - SPACING
    FABRIC_HEIGHT = FABRIC_NUM_TILES_Y * (TILE_HEIGHT + SPACING) + 2 * (TILE_HEIGHT_SMALL + SPACING) + 2 * HALO_SPACING - SPACING

    for x in range(FABRIC_NUM_TILES_X):
        macros['N_term_single']['instances'][f'Tile_X{x+1}Y{0}_N_term_single'] = {
            'location': [
                HALO_SPACING + TILE_WIDTH_SMALL + SPACING + (TILE_WIDTH + SPACING) * x,
                HALO_SPACING + TILE_HEIGHT_SMALL + SPACING + (TILE_HEIGHT + SPACING) * FABRIC_NUM_TILES_Y
            ],
            'orientation': 'N',
        }

    for x in range(FABRIC_NUM_TILES_X):
        macros['S_term_single']['instances'][f'Tile_X{x+1}Y{FABRIC_NUM_TILES_Y + 1}_S_term_single'] = {
            'location': [
                HALO_SPACING + TILE_WIDTH_SMALL + SPACING + (TILE_WIDTH + SPACING) * x,
                HALO_SPACING
            ],
            'orientation': 'N',
        }

    for y in range(FABRIC_NUM_TILES_Y):
        macros['E_IO']['instances'][f'Tile_X{FABRIC_NUM_TILES_X + 1}Y{y+1}_E_IO'] = {
            'location': [
                HALO_SPACING + TILE_WIDTH_SMALL + SPACING + (TILE_WIDTH + SPACING) * FABRIC_NUM_TILES_X,
                HALO_SPACING + TILE_HEIGHT_SMALL + SPACING + (TILE_HEIGHT + SPACING) * (FABRIC_NUM_TILES_Y - 1 - y)
            ],
            'orientation': 'N',
        }

    for y in range(FABRIC_NUM_TILES_Y):
        macros['W_IO']['instances'][f'Tile_X{0}Y{y+1}_W_IO'] = {
            'location': [
                HALO_SPACING,
                HALO_SPACING + TILE_HEIGHT_SMALL + SPACING + (TILE_HEIGHT + SPACING) * (FABRIC_NUM_TILES_Y - 1 - y)
            ],
            'orientation': 'N',
        }

    for y in range(FABRIC_NUM_TILES_Y):
        for x in range(FABRIC_NUM_TILES_X):
            macros['LUT4AB']['instances'][f'Tile_X{x+1}Y{y+1}_LUT4AB'] = {
                'location': [
                    HALO_SPACING + TILE_WIDTH_SMALL + SPACING + (TILE_WIDTH + SPACING) * x,
                    HALO_SPACING + TILE_HEIGHT_SMALL + SPACING + (TILE_HEIGHT + SPACING) * (FABRIC_NUM_TILES_Y - 1 - y)
                ],
                'orientation': 'N',
            }

    #print(macros)

    flow_cfg = {
        "DESIGN_NAME": "eFPGA",
        
        "VERILOG_FILES": verilog_files,

        # Floorplanning
        "DIE_AREA"           : [0, 0, FABRIC_WIDTH, FABRIC_HEIGHT],
        "FP_SIZING"          : "absolute",

        # Macros
        "MACROS": macros,
        # "PDN_MACRO_CONNECTIONS" = [] TODO

        #"PDN_MACRO_CONNECTIONS": ["Tile_X1Y0_N_term_single VPWR VGND VPWR VGND"],

        # Power Distribution Network
        "FP_PDN_MULTILAYER" : True,
        "FP_PDN_ENABLE_RAILS" : False,
        "FP_PDN_VOFFSET" : 10,
        "FP_PDN_HOFFSET" : 10,
        "FP_PDN_VSPACING" : 15,
        "FP_PDN_HSPACING" : 15,
        "FP_PDN_VPITCH" : 50,
        "FP_PDN_HPITCH" : 50,
        
        # Routing
        "GRT_ALLOW_CONGESTION"  : True,
        "GRT_REPAIR_ANTENNAS"   : False,
        "RT_MAX_LAYER"          : "met4",
        
        "CLOCK_PORT": "",#"UserCLK",
        "CLOCK_PERIOD": 0,#10,
        
        #"MAX_FANOUT_CONSTRAINT": 6,
    }

    os.makedirs(os.path.join('runs/fabric_stitching/', fabric_name), exist_ok=True)

    # Choose which flow to run
    flow_class = TopFlow
    if OPEN_IN_KLAYOUT:
        flow_class = OpenInKLayout
    if OPEN_IN_OPENROAD:
        flow_class = OpenInOpenROAD

    # Run flow
    flow = flow_class(
        flow_cfg,
        design_dir = os.path.join('runs/fabric_stitching/', fabric_name),
        pdk_root   = PDK_ROOT,
        pdk        = PDK,
        scl        = SCL
    )

    flow.start(last_run = OPEN_IN_KLAYOUT or OPEN_IN_OPENROAD)

    elapsed_time_process = time.process_time() - t_process
    elapsed_time_perf_counter = time.perf_counter() - t_perf_counter
    
    if OPEN_IN_KLAYOUT or OPEN_IN_OPENROAD:
        return # skip writing measurements
    
    # Write measurement data
    resources = {
        'max_memory' : {},
        'user_time' : {},
        'system_time' : {},
        
        'elapsed_time_process' : elapsed_time_process,
        'elapsed_time_perf_counter' : elapsed_time_perf_counter
    }
    
    resources['max_memory']['RUSAGE_SELF'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    resources['max_memory']['RUSAGE_CHILDREN'] = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    resources['max_memory']['RUSAGE_THREAD'] = resource.getrusage(resource.RUSAGE_THREAD).ru_maxrss
    
    resources['user_time']['RUSAGE_SELF'] = resource.getrusage(resource.RUSAGE_SELF).ru_utime
    resources['user_time']['RUSAGE_CHILDREN'] = resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime
    resources['user_time']['RUSAGE_THREAD'] = resource.getrusage(resource.RUSAGE_THREAD).ru_utime
    
    resources['system_time']['RUSAGE_SELF'] = resource.getrusage(resource.RUSAGE_SELF).ru_stime
    resources['system_time']['RUSAGE_CHILDREN'] = resource.getrusage(resource.RUSAGE_CHILDREN).ru_stime
    resources['system_time']['RUSAGE_THREAD'] = resource.getrusage(resource.RUSAGE_THREAD).ru_stime

    print(resources)
    
    os.makedirs('measurements/fabric_stitching/', exist_ok=True)
    
    with open(f'measurements/fabric_stitching/{fabric_name}.txt', 'w') as f:
        f.write(str(resources))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("tiles_path", type=str, help="Path to tiles folder")
    parser.add_argument("fabric_name", type=str, help="Name of fabric")
    parser.add_argument("fabric_path", type=str, help="Path to fabric_nl folder")
    parser.add_argument("fabric_width", type=int, help="Width of fabric (number of CLBs)")
    parser.add_argument("fabric_height", type=int, help="Height of fabric (number of CLBs)")
    args = parser.parse_args()
    
    main(args.tiles_path, args.fabric_name, args.fabric_path, args.fabric_width, args.fabric_height)
