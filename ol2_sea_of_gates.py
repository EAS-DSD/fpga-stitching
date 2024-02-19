#!/usr/bin/env python3

# Copyright (c) 2024 Leo Moser <leomoser99@gmail.com>
# SPDX-License-Identifier: Apache-2.0

import os
import sys
import time
import json
import argparse
import resource

from openlane.flows.classic import Classic
from openlane.flows.misc import OpenInKLayout
from openlane.flows.misc import OpenInOpenROAD
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

def main(tiles_path, fabric_name, output_dir):

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
        Classic.Steps.remove(OpenROAD.STAPostPNR)
        Classic.Steps.remove(KLayout.XOR)
        Classic.Steps.remove(Checker.XOR)
        Classic.Steps.remove(Magic.DRC)
        Classic.Steps.remove(KLayout.DRC)
        Classic.Steps.remove(Checker.MagicDRC)
        Classic.Steps.remove(Checker.KLayoutDRC) 

    verilog_files = [
        "custom.v",
        "models_pack.v",
        f"{fabric_path}",
        f"{tiles_path}/E_IO/Config_access.v",
        f"{tiles_path}/E_IO/IO_1_bidirectional_frame_config_pass.v",
        f"{tiles_path}/E_IO/E_IO.v",
        f"{tiles_path}/E_IO/E_IO_switch_matrix.v",
        f"{tiles_path}/E_IO/E_IO_ConfigMem.v",
        f"{tiles_path}/W_IO/W_IO.v",
        f"{tiles_path}/W_IO/W_IO_switch_matrix.v",
        f"{tiles_path}/W_IO/W_IO_ConfigMem.v",
        f"{tiles_path}/N_term_single/N_term_single.v",
        f"{tiles_path}/N_term_single/N_term_single_switch_matrix.v",
        f"{tiles_path}/S_term_single/S_term_single.v",
        f"{tiles_path}/S_term_single/S_term_single_switch_matrix.v",
        f"{tiles_path}/LUT4AB/LUT4AB.v",
        f"{tiles_path}/LUT4AB/LUT4AB_switch_matrix.v",
        f"{tiles_path}/LUT4AB/LUT4AB_ConfigMem.v",
        f"{tiles_path}/LUT4AB/MUX8LUT_frame_config_mux.v",
        f"{tiles_path}/LUT4AB/LUT4c_frame_config_dffesr.v"
    ]

    flow_cfg = {
        "DESIGN_NAME": "eFPGA",
        "VERILOG_FILES": verilog_files,
        "RUN_LINTER": False,
        "CLOCK_PORT": "",#"UserCLK",
        "CLOCK_PERIOD": 0,#10,
        "MAX_FANOUT_CONSTRAINT": 6,
        "FP_CORE_UTIL": 40,
        "PL_TARGET_DENSITY_PCT": 50,
    }

    os.makedirs(os.path.join('runs/sea_of_gates/', fabric_name), exist_ok=True)

    # Choose which flow to run
    flow_class = Classic
    if OPEN_IN_KLAYOUT:
        flow_class = OpenInKLayout
    if OPEN_IN_OPENROAD:
        flow_class = OpenInOpenROAD 
    
    # Run flow
    flow = flow_class(
        flow_cfg,
        design_dir = os.path.join('runs/sea_of_gates/', fabric_name),
        pdk_root   = PDK_ROOT,
        pdk        = PDK,
        scl        = SCL
    )

    flow.start(last_run = OPEN_IN_KLAYOUT or OPEN_IN_OPENROAD)

    elapsed_time_process = time.process_time() - t_process
    elapsed_time_perf_counter = time.perf_counter() - t_perf_counter
    
    if OPEN_IN_KLAYOUT or OPEN_IN_OPENROAD:
        return # skip writing measurements
    
    # Get area from metrics.json
    file_list = sorted(os.listdir(os.path.join('runs/sea_of_gates/', fabric_name, 'runs/')))
    output_dir = file_list[-1]
    json_path = os.path.join('runs/sea_of_gates/', fabric_name, 'runs/', output_dir, 'final/metrics.json')
    print(json_path)
    assert(os.path.isfile(json_path))
    with open(json_path, 'r') as f:
        json_data = json.load(f)
    
    # Write measurement data
    resources = {
        'max_memory' : {},
        'user_time' : {},
        'system_time' : {},
        
        'elapsed_time_process' : elapsed_time_process,
        'elapsed_time_perf_counter' : elapsed_time_perf_counter,
        
        'design__die__bbox' : json_data['design__die__bbox']
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
    
    os.makedirs('measurements/sea_of_gates/', exist_ok=True)
    
    with open(f'measurements/sea_of_gates/{fabric_name}.txt', 'w') as f:
        f.write(str(resources))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("tiles_path", type=str, help="Path to tiles folder")
    parser.add_argument("fabric_name", type=str, help="Name of fabric")
    parser.add_argument("fabric_path", type=str, help="Path to fabric_nl folder")
    args = parser.parse_args()

    main(args.tiles_path, args.fabric_name, args.fabric_path)
