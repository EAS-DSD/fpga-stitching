#!/usr/bin/env python3

# Copyright (c) 2024 Leo Moser <leomoser99@gmail.com>
# SPDX-License-Identifier: Apache-2.0

import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

fabric_sizes = ['fabric_small', 'fabric_medium', 'fabric_large']
sea_of_gates_measurements = {'fabric_small' : [], 'fabric_medium' : [], 'fabric_large' : []}
fabric_stitching_measurements = {'fabric_small' : [], 'fabric_medium' : [], 'fabric_large' : []}
harden_tiles_measurements = []

def load_measurements():

    assert(os.path.isdir('measurements/harden_tiles/'))

    harden_tiles_files = sorted(os.listdir('measurements/harden_tiles/'))

    for file in harden_tiles_files:
            with open(os.path.join('measurements/harden_tiles/', file), 'r') as f:
                harden_tiles_measurements.append(json.load(f))

    for size in fabric_sizes:
        assert(os.path.isdir(os.path.join('measurements/sea_of_gates/', size)))
        assert(os.path.isdir(os.path.join('measurements/fabric_stitching/', size)))

        sea_of_gates_files = sorted(os.listdir(os.path.join('measurements/sea_of_gates/', size)))
        fabric_stitching_files = sorted(os.listdir(os.path.join('measurements/fabric_stitching/', size)))

        for file in sea_of_gates_files:
            with open(os.path.join('measurements/sea_of_gates/', size, file), 'r') as f:
                sea_of_gates_measurements[size].append(json.load(f))
        
        for file in fabric_stitching_files:
            with open(os.path.join('measurements/fabric_stitching/', size, file), 'r') as f:
                fabric_stitching_measurements[size].append(json.load(f))

    print(sea_of_gates_measurements)
    print(fabric_stitching_measurements)
    print(harden_tiles_measurements)

def bar_chart_time(samples=3):
    # set width of bar 
    barWidth = 0.25
    fig, ax = plt.subplots(figsize=(15*0.8,7*0.8)) 

    # Calculate mean value and stddev
    time_sog = {'fabric_small': [], 'fabric_medium': [], 'fabric_large': []}
    time_stitch = {'fabric_small': [], 'fabric_medium': [], 'fabric_large': []}
    time_tiles = []
    
    for i in range(samples):
        for size in fabric_sizes:
            time_sog[size].append(sea_of_gates_measurements[size][-i-1]['elapsed_time_perf_counter'] / 60)
            time_stitch[size].append(fabric_stitching_measurements[size][-i-1]['elapsed_time_perf_counter'] / 60)
        time_tiles.append(harden_tiles_measurements[-i-1]['elapsed_time_perf_counter'] / 60)

    print(time_sog)
    print(time_stitch)
    print(time_tiles)

    # Data
    data_sea_of_gates = [
        np.mean(time_sog['fabric_small']),
        np.mean(time_sog['fabric_medium']),
        np.mean(time_sog['fabric_large'])
    ]
    data_fabric_stitching = [
        np.mean(time_stitch['fabric_small']),
        np.mean(time_stitch['fabric_medium']),
        np.mean(time_stitch['fabric_large'])
    ]
    data_harden_tiles = [np.mean(time_tiles)]*3
    
    # Error
    error_sea_of_gates = [
        np.std(time_sog['fabric_small']),
        np.std(time_sog['fabric_medium']),
        np.std(time_sog['fabric_large'])
    ]
    error_fabric_stitching = [
        np.std(time_stitch['fabric_small']),
        np.std(time_stitch['fabric_medium']),
        np.std(time_stitch['fabric_large'])
    ]
    error_harden_tiles = [np.std(time_tiles)]*3

    print(data_sea_of_gates)
    print(data_fabric_stitching)
    print(data_harden_tiles)
    
    print(error_sea_of_gates)
    print(error_fabric_stitching)
    print(error_harden_tiles)

    # Set position of bar on X axis 
    br1 = np.arange(len(data_sea_of_gates)) 
    br2 = [x + barWidth for x in br1]

    colors = ['#23d6fc', '#e3607a', '#14d301']

    # Make the plot
    plt.bar(br1, data_sea_of_gates, color=colors[0], width=barWidth,
            edgecolor='black', label='Sea of Gates', yerr=error_sea_of_gates)

    plt.bar(br2, data_harden_tiles, color=colors[1], width=barWidth,
            edgecolor='black', label='Tiles Hardening', yerr=error_harden_tiles)

    plt.bar(br2, data_fabric_stitching, color=colors[2], width=barWidth,
            edgecolor='black', label='Fabric Stitching', yerr=error_harden_tiles, bottom=data_harden_tiles) 

    # Adding Xticks
    plt.ylabel('Time in Minutes', fontweight ='bold', fontsize = 15) 
    plt.xticks([r + barWidth/2 for r in range(len(data_sea_of_gates))], 
            ['Small 1x1 CLB', 'Medium 5x5 CLB', 'Large 10x10 CLB'])
     
    ax.legend(loc='upper left', fontsize="14", fancybox=True)
    
    # this locator puts ticks at regular intervals
    loc = plticker.MultipleLocator(base=10.0)
    ax.yaxis.set_major_locator(loc)
    
    ax.set_axisbelow(True)
    ax.grid(color='gray', axis='y')
    ylim = ax.get_ylim()
    ax.set_ylim((0, ylim[1]+5))
    plt.show()
    
    os.makedirs('diagrams/', exist_ok=True)
    fig.savefig('diagrams/bar_chart_time.svg', bbox_inches='tight')

def bar_chart_ram(samples=3):

    # set width of bar 
    barWidth = 0.25
    fig, ax = plt.subplots(figsize=(15*0.8,7*0.8)) 

    # Calculate mean value and stddev
    ram_sog = {'fabric_small': [], 'fabric_medium': [], 'fabric_large': []}
    ram_stitch = {'fabric_small': [], 'fabric_medium': [], 'fabric_large': []}
    ram_tiles = []
    
    for i in range(samples):
        for size in fabric_sizes:
            ram_sog[size].append(sea_of_gates_measurements[size][-i-1]['max_memory']['RUSAGE_CHILDREN'] / (1024**2))
            ram_stitch[size].append(fabric_stitching_measurements[size][-i-1]['max_memory']['RUSAGE_CHILDREN'] / (1024**2))
        ram_tiles.append(harden_tiles_measurements[-i-1]['max_memory']['RUSAGE_CHILDREN'] / (1024**2))

    # Data
    data_sea_of_gates = [
        np.mean(ram_sog['fabric_small']),
        np.mean(ram_sog['fabric_medium']),
        np.mean(ram_sog['fabric_large'])
    ]
    data_fabric_stitching = [
        np.mean(ram_stitch['fabric_small']),
        np.mean(ram_stitch['fabric_medium']),
        np.mean(ram_stitch['fabric_large'])
    ]
    data_harden_tiles = [np.mean(ram_tiles)]*3
    
    # Error
    error_sea_of_gates = [
        np.std(ram_sog['fabric_small']),
        np.std(ram_sog['fabric_medium']),
        np.std(ram_sog['fabric_large'])
    ]
    error_fabric_stitching = [
        np.std(ram_stitch['fabric_small']),
        np.std(ram_stitch['fabric_medium']),
        np.std(ram_stitch['fabric_large'])
    ]
    error_harden_tiles = [np.std(ram_tiles)]*3
    
    print(data_sea_of_gates)
    print(data_fabric_stitching)
    print(data_harden_tiles)
    
    print(error_sea_of_gates)
    print(error_fabric_stitching)
    print(error_harden_tiles)
    
    # Set position of bar on X axis 
    br1 = np.arange(len(data_sea_of_gates)) 
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]

    colors = ['#23d6fc', '#e3607a', '#14d301']

    # Make the plot
    plt.bar(br1, data_sea_of_gates, color = colors[0], width = barWidth, 
            edgecolor ='black', label ='Sea of Gates', yerr = error_sea_of_gates)
            
    plt.bar(br2, data_harden_tiles, color = colors[1], width = barWidth, 
            edgecolor ='black', label ='Tiles Hardening', yerr = error_harden_tiles)
            
    plt.bar(br3, data_fabric_stitching, color = colors[2], width = barWidth, 
            edgecolor ='black', label ='Fabric Stitching', yerr = error_fabric_stitching) 
     
    # Adding Xticks
    plt.ylabel('RAM Usage in GiB', fontweight ='bold', fontsize = 15) 
    plt.xticks([r + barWidth for r in range(len(data_sea_of_gates))], 
            ['Small 1x1 CLB', 'Medium 5x5 CLB', 'Large 10x10 CLB'])

    ax.legend(loc='upper left', fontsize="14", fancybox=True)
    
    # this locator puts ticks at regular intervals
    loc = plticker.MultipleLocator(base=1.0)
    ax.yaxis.set_major_locator(loc)
    
    ax.set_axisbelow(True)
    ax.grid(color='gray', axis='y')
    ylim = ax.get_ylim()
    ax.set_ylim((0, ylim[1]+0.1))
    plt.show()
    
    os.makedirs('diagrams/', exist_ok=True)
    fig.savefig('diagrams/bar_chart_ram.svg', bbox_inches='tight')


def diagram_batch(samples=3):

    fabrics = sorted(os.listdir('measurements/fabric_stitching/'))
    
    fabrics = [fabric for fabric in fabrics if 'x' in fabric]
    
    # helper function to perform sort
    def num_sort(test_string):
        return int(test_string.removeprefix('fabric').split('x')[0])

    # calling function
    fabrics.sort(key=num_sort)
    
    print(fabrics)
    
    batch_measurements = {}

    for size in fabrics:
        key = int(size.removeprefix('fabric').split('x')[0])
        batch_measurements[key] = []
    
        assert(os.path.isdir(os.path.join('measurements/fabric_stitching/', size)))

        fabric_stitching_files = sorted(os.listdir(os.path.join('measurements/fabric_stitching/', size)))

        for file in fabric_stitching_files:
            with open(os.path.join('measurements/fabric_stitching/', size, file), 'r') as f:
                data = json.load(f)
                batch_measurements[key].append(data.copy())
    
    all_data_time = [ [batch_measurements[key][-sample-1]['elapsed_time_perf_counter'] for sample in range(samples)] for key in batch_measurements]
    all_data_ram = [ [batch_measurements[key][-sample-1]['max_memory']['RUSAGE_CHILDREN'] / (1024**2) for sample in range(samples)] for key in batch_measurements]
    all_data_area = [ [round(float(batch_measurements[key][-sample-1]['design__die__bbox'].split(' ')[2])**2 / 1000_000, 2) for sample in range(samples)] for key in batch_measurements]

    print(all_data_time)
    print(all_data_ram)
    print(all_data_area)
    
    data_time = [np.mean(data_array) for data_array in all_data_time]
    data_ram  = [np.mean(data_array) for data_array in all_data_ram]
    data_area = [np.mean(data_array) for data_array in all_data_area]
    
    error_time = [np.std(data_array) for data_array in all_data_time]
    error_ram  = [np.std(data_array) for data_array in all_data_ram]
    error_area = [np.std(data_array) for data_array in all_data_area]

    print(data_time)
    print(data_ram)
    print(data_area)
    
    print(error_time)
    print(error_ram)
    print(error_area)

    keys = [key for key in batch_measurements]

    fig, ax1 = plt.subplots(figsize=(15*0.8,7*0.8)) 
    fig.subplots_adjust(right=0.75)

    colors = ['#23d6fc', '#e3607a', '#14d301']

    ax2 = ax1.twinx()
    ax3 = ax1.twinx()

    ax2.spines.right.set_position(("axes", 1.0))
    ax3.spines.right.set_position(("axes", 1.2))

    p1, = ax1.plot(keys, data_time, color=colors[0], linestyle='dashed', marker='^', markeredgecolor='white',
                   markerfacecolor=colors[0], markersize=12, label="Time in Minutes")
    p2, = ax2.plot(keys, data_ram, color=colors[1], linestyle='dashed', marker='o', markeredgecolor='white',
                   markerfacecolor=colors[1], markersize=12, label="RAM Usage in GiB")
    p3, = ax3.plot(keys, data_area, color=colors[2], linestyle='dashed', marker='s', markeredgecolor='white',
                   markerfacecolor=colors[2], markersize=12, label="Die Area in mm²")
    
    ax1.errorbar(keys, data_time, yerr = error_time, fmt="none", color=colors[0])
    ax2.errorbar(keys, data_ram, yerr = error_ram, fmt="none", color=colors[1])
    ax3.errorbar(keys, data_area, yerr = error_area, fmt="none", color=colors[2])
    
    ax1.set(xlabel="Fabric Size in CLB", ylabel="Time in Minutes")
    ax2.set(ylabel="RAM Usage in GiB")
    ax3.set(ylabel="Die Area in mm²")
    
    ax1.yaxis.label.set_color(p1.get_color())
    ax2.yaxis.label.set_color(p2.get_color())
    ax3.yaxis.label.set_color(p3.get_color())
    
    ax1.tick_params(axis='y', colors=p1.get_color())
    ax2.tick_params(axis='y', colors=p2.get_color())
    ax3.tick_params(axis='y', colors=p3.get_color())
    
    keys_labels = [str(key)+'×'+str(key) for key in keys]
    plt.xticks(ticks=keys, labels=keys_labels)
    
    ax1.legend(handles=[p1, p2, p3], loc='upper left', fontsize="14", fancybox=True)

    ax1.set_axisbelow(True)
    plt.show()

    os.makedirs('diagrams/', exist_ok=True)
    fig.savefig('diagrams/diagram_batch.svg', bbox_inches='tight')

def print_area():
    
    print('Fabric | Sea of Gates | Stitching')
    
    for size in fabric_sizes:
    
        sog_width = sea_of_gates_measurements[size][-1]['design__die__bbox'].split(' ')[2] # um
        sog_height = sea_of_gates_measurements[size][-1]['design__die__bbox'].split(' ')[3] # um

        sog_area = round(float(sog_width) * float(sog_height) / 1000_000, 2)

        sti_width = fabric_stitching_measurements[size][-1]['design__die__bbox'].split(' ')[2] # um
        sti_height = fabric_stitching_measurements[size][-1]['design__die__bbox'].split(' ')[3] # um

        sti_area = round(float(sti_width) * float(sti_height) / 1000_000, 2)
        
        print(f'{size} | {sog_area} | {sti_area}')

def main():
    load_measurements()

    bar_chart_time()
    bar_chart_ram()
    #diagram_batch()
    
    print_area()

if __name__ == "__main__":
    main()
