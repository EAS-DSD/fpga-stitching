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

def bar_chart_time():
    # set width of bar 
    barWidth = 0.25
    fig, ax = plt.subplots(figsize=(16*0.7,9*0.7)) 
     
    # set height of bar 
    sea_of_gates = [
        sea_of_gates_measurements['fabric_small'][-1]['elapsed_time_perf_counter'] / 60,
        sea_of_gates_measurements['fabric_medium'][-1]['elapsed_time_perf_counter'] / 60,
        sea_of_gates_measurements['fabric_large'][-1]['elapsed_time_perf_counter']  / 60
    ]
    fabric_stitching = [
        fabric_stitching_measurements['fabric_small'][-1]['elapsed_time_perf_counter'] / 60,
        fabric_stitching_measurements['fabric_medium'][-1]['elapsed_time_perf_counter'] / 60,
        fabric_stitching_measurements['fabric_large'][-1]['elapsed_time_perf_counter'] / 60
    ]
    harden_tiles = harden_tiles_measurements[-1]['elapsed_time_perf_counter'] / 60
     
    # Set position of bar on X axis 
    br1 = np.arange(len(sea_of_gates)) 
    br2 = [x + barWidth for x in br1]

    colors = ['#BBBBBB', '#707070', '#303030']

    # Make the plot
    plt.bar(br1, sea_of_gates, color =colors[0], width = barWidth, 
            edgecolor ='black', label ='sea_of_gates', yerr = 3)
            
    plt.bar(br2, harden_tiles, color =colors[1], width = barWidth, 
            edgecolor ='black', label ='harden_tiles', yerr = 2)
            
    plt.bar(br2, fabric_stitching, color =colors[2], width = barWidth, 
            edgecolor ='black', label ='fabric_stitching', yerr = 1, bottom=harden_tiles) 
     
    # Adding Xticks 
    plt.xlabel('Time for Completion', fontweight ='bold', fontsize = 15) 
    plt.ylabel('Time in Minutes', fontweight ='bold', fontsize = 15) 
    plt.xticks([r + barWidth for r in range(len(sea_of_gates))], 
            ['small 1x1 CLB', 'medium 5x5 CLB', 'large 10x10 CLB'])
     
    ax.legend(loc='upper left', fontsize="14", fancybox=True)
    
    # this locator puts ticks at regular intervals
    loc = plticker.MultipleLocator(base=10.0)
    ax.yaxis.set_major_locator(loc)
    
    ax.set_axisbelow(True)
    ax.grid(color='gray', axis='y')
    ylim = ax.get_ylim()
    ax.set_ylim((ylim[0]+5, ylim[1]+5))
    plt.show()
    
    os.makedirs('diagrams/', exist_ok=True)
    fig.savefig('diagrams/bar_chart_time.svg', bbox_inches='tight')

def bar_chart_ram():

    # set width of bar 
    barWidth = 0.25
    fig, ax = plt.subplots(figsize=(16*0.7,9*0.7)) 

    # set height of bar 
    sea_of_gates = [
        sea_of_gates_measurements['fabric_small'][-1]['max_memory']['RUSAGE_CHILDREN'] / (1000**2),
        sea_of_gates_measurements['fabric_medium'][-1]['max_memory']['RUSAGE_CHILDREN'] / (1000**2),
        sea_of_gates_measurements['fabric_large'][-1]['max_memory']['RUSAGE_CHILDREN'] / (1000**2)
    ]
    fabric_stitching = [
        fabric_stitching_measurements['fabric_small'][-1]['max_memory']['RUSAGE_CHILDREN'] / (1000**2),
        fabric_stitching_measurements['fabric_medium'][-1]['max_memory']['RUSAGE_CHILDREN'] / (1000**2),
        fabric_stitching_measurements['fabric_large'][-1]['max_memory']['RUSAGE_CHILDREN'] / (1000**2)
    ]
    harden_tiles = harden_tiles_measurements[-1]['max_memory']['RUSAGE_CHILDREN'] / (1000**2)
     
    # Set position of bar on X axis 
    br1 = np.arange(len(sea_of_gates)) 
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]

    colors = ['#BBBBBB', '#707070', '#303030']

    # Make the plot
    plt.bar(br1, sea_of_gates, color = colors[0], width = barWidth, 
            edgecolor ='black', label ='sea_of_gates')#, yerr = 1)
            
    plt.bar(br2, harden_tiles, color = colors[1], width = barWidth, 
            edgecolor ='black', label ='harden_tiles')#, yerr = 2)
            
    plt.bar(br3, fabric_stitching, color = colors[2], width = barWidth, 
            edgecolor ='black', label ='fabric_stitching')#, yerr = 1) 
     
    # Adding Xticks 
    plt.xlabel('Max RAM Usage', fontweight ='bold', fontsize = 15) 
    plt.ylabel('RAM Usage in Gigabyte', fontweight ='bold', fontsize = 15) 
    plt.xticks([r + barWidth for r in range(len(sea_of_gates))], 
            ['small 1x1 CLB', 'medium 5x5 CLB', 'large 10x10 CLB'])

    ax.legend(loc='upper left', fontsize="14", fancybox=True)
    
    # this locator puts ticks at regular intervals
    loc = plticker.MultipleLocator(base=1.0)
    ax.yaxis.set_major_locator(loc)
    
    ax.set_axisbelow(True)
    ax.grid(color='gray', axis='y')
    ylim = ax.get_ylim()
    ax.set_ylim((ylim[0]-0.5, ylim[1]+0.1))
    plt.show()
    
    os.makedirs('diagrams/', exist_ok=True)
    fig.savefig('diagrams/bar_chart_ram.svg', bbox_inches='tight')


def diagram_batch():

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
                batch_measurements[key].append(json.load(f))
    
    data_time = [batch_measurements[key][0]['elapsed_time_perf_counter'] for key in batch_measurements]
    data_ram = [batch_measurements[key][0]['max_memory']['RUSAGE_CHILDREN'] / (1000**2) for key in batch_measurements]
    data_area = [round(float(batch_measurements[key][0]['design__die__bbox'].split(' ')[2])**2 / 1000_000, 2) for key in batch_measurements]
        
    key = [key for key in batch_measurements]

    fig, ax1 = plt.subplots(figsize=(16*0.7,9*0.7))
    fig.subplots_adjust(right=0.75)

    colors = ['#303030', '#707070', '#BBBBBB']

    ax2 = ax1.twinx()
    ax3 = ax1.twinx()

    ax2.spines.right.set_position(("axes", 1.0))
    ax3.spines.right.set_position(("axes", 1.2))

    p1, = ax1.plot(key, data_time, color=colors[0], linestyle='dashed', marker='^', markeredgecolor='white', markerfacecolor=colors[0], markersize=12, label="Time in Minutes")
    p2, = ax2.plot(key, data_ram, color=colors[1], linestyle='dashed', marker='o', markeredgecolor='white', markerfacecolor=colors[1], markersize=12, label="RAM Usage in Gigabyte")
    p3, = ax3.plot(key, data_area, color=colors[2], linestyle='dashed', marker='s', markeredgecolor='white', markerfacecolor=colors[2], markersize=12, label="Die Area in um²")
    
    ax1.set(xlabel="Fabric Size in CLB", ylabel="Time in Minutes")
    ax2.set(ylabel="RAM Usage in Gigabyte")
    ax3.set(ylabel="Die Area in um²")
    
    ax1.legend(handles=[p1, p2, p3], loc='upper left', fontsize="14", fancybox=True)

    ax1.set_axisbelow(True)
    plt.show()

    os.makedirs('diagrams/', exist_ok=True)
    fig.savefig('diagrams/diagram_batch.svg', bbox_inches='tight')

def print_area():
    
    print('Fabric | Sea of Gates | Stitching')
    
    for size in fabric_sizes:
    
        sog_width = sea_of_gates_measurements[size][0]['design__die__bbox'].split(' ')[2] # um
        sog_height = sea_of_gates_measurements[size][0]['design__die__bbox'].split(' ')[3] # um

        sog_area = round(float(sog_width) * float(sog_height) / 1000_000, 2)

        sti_width = fabric_stitching_measurements[size][0]['design__die__bbox'].split(' ')[2] # um
        sti_height = fabric_stitching_measurements[size][0]['design__die__bbox'].split(' ')[3] # um

        sti_area = round(float(sti_width) * float(sti_height) / 1000_000, 2)
        
        print(f'{size} | {sog_area} | {sti_area}')

def main():
    load_measurements()
    
    print(sea_of_gates_measurements)

    bar_chart_time()
    
    bar_chart_ram()
    
    diagram_batch()
    
    print_area()

if __name__ == "__main__":
    main()
