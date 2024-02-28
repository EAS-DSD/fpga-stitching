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

colors = ['#22d2f7', '#e3607a', '#14d301']

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
    fig, ax = plt.subplots(figsize=(15*0.4,7*0.4)) 

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
    error_sea_of_gates_low = [abs(min([time - data_sea_of_gates[i] for time in time_sog[fabric]])) for i, fabric in enumerate(fabric_sizes)]
    error_sea_of_gates_high = [max([time - data_sea_of_gates[i] for time in time_sog[fabric]]) for i, fabric in enumerate(fabric_sizes)]
    
    error_fabric_stitching_low = [abs(min([time - data_fabric_stitching[i] for time in time_stitch[fabric]])) for i, fabric in enumerate(fabric_sizes)]
    error_fabric_stitching_high = [max([time - data_fabric_stitching[i] for time in time_stitch[fabric]]) for i, fabric in enumerate(fabric_sizes)]
    
    error_harden_tiles_low = [abs(min([time - data_harden_tiles[i] for time in time_tiles])) for i, fabric in enumerate(fabric_sizes)]
    error_harden_tiles_high = [max([time - data_harden_tiles[i] for time in time_tiles]) for i, fabric in enumerate(fabric_sizes)]

    print(data_sea_of_gates)
    print(data_fabric_stitching)
    print(data_harden_tiles)
    
    print(error_sea_of_gates_low)
    print(error_fabric_stitching_low)
    print(error_harden_tiles_low)
    
    print(error_sea_of_gates_high)
    print(error_fabric_stitching_high)
    print(error_harden_tiles_high)

    # Set position of bar on X axis 
    br1 = np.arange(len(data_sea_of_gates)) 
    br2 = [x + barWidth for x in br1]

    # Make the plot
    plt.bar(br1, data_sea_of_gates, color=colors[0], width=barWidth,
            edgecolor='black', label='Sea of Gates', yerr=(error_sea_of_gates_low, error_sea_of_gates_high))
    plt.bar(br2, data_harden_tiles, color=colors[1], width=barWidth,
            edgecolor='black', label='Tiles Hardening', yerr=(error_harden_tiles_low, error_harden_tiles_high))
    plt.bar(br2, data_fabric_stitching, color=colors[2], width=barWidth,
            edgecolor='black', label='Fabric Stitching', yerr=(error_harden_tiles_low, error_harden_tiles_high), bottom=data_harden_tiles)

    # inset axes....
    x1, x2, y1, y2 = -barWidth, barWidth*6, 0, 25  # subregion of the original image
    axins = ax.inset_axes([0.15, 0.2, 0.4, 0.4], xlim=(x1, x2), ylim=(y1, y2), xticklabels=[])

    axins.bar(br1, data_sea_of_gates, color=colors[0], width=barWidth,
            edgecolor='black', label='Sea of Gates', yerr=(error_sea_of_gates_low, error_sea_of_gates_high))
    axins.bar(br2, data_harden_tiles, color=colors[1], width=barWidth,
            edgecolor='black', label='Tiles Hardening', yerr=(error_harden_tiles_low, error_harden_tiles_high))
    axins.bar(br2, data_fabric_stitching, color=colors[2], width=barWidth,
            edgecolor='black', label='Fabric Stitching', yerr=(error_harden_tiles_low, error_harden_tiles_high), bottom=data_harden_tiles)

    ax.indicate_inset_zoom(axins, edgecolor="black")

    axins.set_xticks([])
    axins.grid()
    
    # this locator puts ticks at regular intervals
    loc = plticker.MultipleLocator(base=10.0)
    axins.yaxis.set_major_locator(loc)

    # Adding Xticks
    plt.ylabel('Time in Minutes')
    plt.xticks([r + barWidth/2 for r in range(len(data_sea_of_gates))], 
            ['Small 1x1 CLB', 'Medium 5x5 CLB', 'Large 10x10 CLB'])
     
    ax.legend(loc='upper left', fancybox=True)#, fontsize="10")
    
    # this locator puts ticks at regular intervals
    loc = plticker.MultipleLocator(base=40.0)
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
    fig, ax = plt.subplots(figsize=(15*0.4,7*0.4)) 

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
    error_sea_of_gates_low = [abs(min([ram - data_sea_of_gates[i] for ram in ram_sog[fabric]])) for i, fabric in enumerate(fabric_sizes)]
    error_sea_of_gates_high = [max([ram - data_sea_of_gates[i] for ram in ram_sog[fabric]]) for i, fabric in enumerate(fabric_sizes)]
    
    error_fabric_stitching_low = [abs(min([ram - data_fabric_stitching[i] for ram in ram_stitch[fabric]])) for i, fabric in enumerate(fabric_sizes)]
    error_fabric_stitching_high = [max([ram - data_fabric_stitching[i] for ram in ram_stitch[fabric]]) for i, fabric in enumerate(fabric_sizes)]
    
    error_harden_tiles_low = [abs(min([ram - data_harden_tiles[i] for ram in ram_tiles])) for i, fabric in enumerate(fabric_sizes)]
    error_harden_tiles_high = [max([ram - data_harden_tiles[i] for ram in ram_tiles]) for i, fabric in enumerate(fabric_sizes)]
    
    print(data_sea_of_gates)
    print(data_fabric_stitching)
    print(data_harden_tiles)
    
    print(error_sea_of_gates_low)
    print(error_fabric_stitching_low)
    print(error_harden_tiles_low)
    
    print(error_sea_of_gates_high)
    print(error_fabric_stitching_high)
    print(error_harden_tiles_high)
    
    # Set position of bar on X axis 
    br1 = np.arange(len(data_sea_of_gates)) 
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]

    # Make the plot
    ax.bar(br1, data_sea_of_gates, color = colors[0], width = barWidth, 
            edgecolor ='black', label ='Sea of Gates', yerr = [error_sea_of_gates_low, error_sea_of_gates_high])
            
    ax.bar(br2, data_harden_tiles, color = colors[1], width = barWidth, 
            edgecolor ='black', label ='Tiles Hardening', yerr = (error_harden_tiles_low, error_harden_tiles_high))
            
    ax.bar(br3, data_fabric_stitching, color = colors[2], width = barWidth, 
            edgecolor ='black', label ='Fabric Stitching', yerr = (error_fabric_stitching_low, error_fabric_stitching_high))

    # Adding Xticks
    plt.ylabel('RAM Usage in GiB') 
    plt.xticks([r + barWidth for r in range(len(data_sea_of_gates))], 
            ['Small 1x1 CLB', 'Medium 5x5 CLB', 'Large 10x10 CLB'])

    ax.legend(loc='upper left', fancybox=True)
    
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
    
    all_data_time = [ [batch_measurements[key][-sample-1]['elapsed_time_perf_counter'] / 60 for sample in range(samples)] for key in batch_measurements]
    all_data_ram = [ [batch_measurements[key][-sample-1]['max_memory']['RUSAGE_CHILDREN'] / (1024**2) for sample in range(samples)] for key in batch_measurements]
    all_data_area = [ [round(float(batch_measurements[key][-sample-1]['design__die__bbox'].split(' ')[2])**2 / 1000_000, 2) for sample in range(samples)] for key in batch_measurements]

    print(all_data_time)
    print(all_data_ram)
    print(all_data_area)
    
    data_time = [np.mean(data_array) for data_array in all_data_time]
    data_ram  = [np.mean(data_array) for data_array in all_data_ram]
    data_area = [np.mean(data_array) for data_array in all_data_area]
    
    error_time = [np.std(data_array) for data_array in all_data_time]
    
    error_time_low = [abs(min([data - data_time[i] for data in data_array])) for i, data_array in enumerate(all_data_time)]
    error_time_high = [max([data - data_time[i] for data in data_array]) for i, data_array in enumerate(all_data_time)]

    error_ram  = [np.std(data_array) for data_array in all_data_ram]
    
    error_ram_low = [abs(min([data - data_ram[i] for data in data_array])) for i, data_array in enumerate(all_data_ram)]
    error_ram_high = [max([data - data_ram[i] for data in data_array]) for i, data_array in enumerate(all_data_ram)]
    
    error_area = [np.std(data_array) for data_array in all_data_area]

    # No change in area possible, else floating porint imprecision
    error_area_low = [0]*len(data_area)#[abs(min([data - data_area[i] for data in data_array])) for i, data_array in enumerate(all_data_area)]
    error_area_high = [0]*len(data_area)#[max([data - data_area[i] for data in data_array]) for i, data_array in enumerate(all_data_area)]

    print(data_time)
    print(data_ram)
    print(data_area)
    
    print(error_time_low)
    print(error_ram_low)
    print(error_area_low)
    
    print(error_time_high)
    print(error_ram_high)
    print(error_area_high)

    keys = [key for key in batch_measurements]

    fig, ax = plt.subplots(3, figsize=(15*0.4,7*0.7)) 

    p1, = ax[0].plot(keys, data_time, color=colors[0], linestyle='dashed', marker='^', markeredgecolor='white',
                   markerfacecolor=colors[0], markersize=8, label="Time in Minutes")
    p2, = ax[1].plot(keys, data_ram, color=colors[1], linestyle='dashed', marker='o', markeredgecolor='white',
                   markerfacecolor=colors[1], markersize=8, label="RAM Usage in GiB")
    p3, = ax[2].plot(keys, data_area, color=colors[2], linestyle='dashed', marker='s', markeredgecolor='white',
                   markerfacecolor=colors[2], markersize=8, label="Die Area in mm²")
    
    ax[0].errorbar(keys, data_time, yerr = (error_time_low, error_time_high), fmt="none", color=colors[0])
    ax[1].errorbar(keys, data_ram, yerr = (error_ram_low, error_ram_high), fmt="none", color=colors[1])
    ax[2].errorbar(keys, data_area, yerr = (error_area_low, error_area_high), fmt="none", color=colors[2])
    
    ax[0].set(ylabel="Time in Minutes")
    ax[1].set(ylabel="RAM Usage in GiB")
    ax[2].set(xlabel="Fabric Size in CLB", ylabel="Die Area in mm²")
    
    ax[0].yaxis.label.set_color(p1.get_color())
    ax[1].yaxis.label.set_color(p2.get_color())
    ax[2].yaxis.label.set_color(p3.get_color())
    
    ax[0].tick_params(axis='y', colors=p1.get_color())
    ax[1].tick_params(axis='y', colors=p2.get_color())
    ax[2].tick_params(axis='y', colors=p3.get_color())
    
    ax[0].yaxis.set_major_locator(plticker.MultipleLocator(base=5.0))
    ax[1].yaxis.set_major_locator(plticker.MultipleLocator(base=2.0))
    ax[2].yaxis.set_major_locator(plticker.MultipleLocator(base=20.0))
    
    ax[0].set_ylim([-2.5, 20])
    ax[1].set_ylim([0, 9])
    ax[2].set_ylim([-5, 65])
    
    ax[0].grid()
    ax[1].grid()
    ax[2].grid()
    
    fig.align_labels()
    
    ax[0].set_xticklabels([])
    ax[1].set_xticklabels([])
    
    ax[0].set_xticks(keys)
    ax[1].set_xticks(keys)

    keys_labels = [str(key)+'×'+str(key) for key in keys]
    plt.xticks(ticks=keys, labels=keys_labels, rotation=70)

    plt.subplots_adjust(hspace=0.13)

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
        
        overhead = round((sti_area - sog_area) / sog_area * 100.0, 2)
        
        print(f'{size} | {sog_area} | {sti_area} | {overhead}%')

def main():
    load_measurements()

    bar_chart_time()
    bar_chart_ram()
    diagram_batch()
    
    print_area()

if __name__ == "__main__":
    main()
