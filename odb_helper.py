#!/usr/bin/env python3

# Copyright (c) 2023 Sylvain Munaut <tnt@246tNt.com>
# Copyright (c) 2024 Leo Moser <leomoser99@gmail.com>
# SPDX-License-Identifier: Apache-2.0

import os
import sys
import click

from reader import click_odb, click
import odb

# Place pins centrally, equally spaced on one side
def place_pins_central(die_area, layer, bterms, side='N', margin=10_000, min_grid=5):

    # Nothing to do
    if not len(bterms):
        return

    die_x1 = die_area.xMin()
    die_y1 = die_area.yMin()
    die_x2 = die_area.xMax()
    die_y2 = die_area.yMax()

    die_width = die_x2 - die_x1
    die_height = die_y2 - die_y1
    
    # Size of pin rectangle
    PIN_WIDTH  = 300
    PIN_LENGTH = 1000
    
    # For each bterm
    for index, bterm in enumerate(bterms):
        
        # Create pin
        bpin = odb.dbBPin_create(bterm)
        bpin.setPlacementStatus("PLACED")
        
        # North side
        if side == 'N':
            rect = odb.Rect(0, 0, PIN_WIDTH, PIN_LENGTH)
            
            if len(bterms) == 1:
                side_position = (die_width - 2*margin) // 2
            else:
                side_position = ( (die_width - 2*margin) * index // (len(bterms)-1) )
            side_position = min_grid * round(side_position/min_grid)
            
            # Check for grid alignment
            assert(margin % min_grid == 0)
            assert(side_position % min_grid == 0)
        
            rect.moveTo(
                die_x1 + margin + side_position - PIN_WIDTH // 2,
                die_y2 - PIN_LENGTH
            )

        # East side
        elif side == 'E':
            rect = odb.Rect(0, 0, PIN_LENGTH, PIN_WIDTH)
            
            if len(bterms) == 1:
                side_position = (die_height - 2*margin) // 2
            else:
                side_position = ( (die_height - 2*margin) * index // (len(bterms)-1) )
            side_position = min_grid * round(side_position/min_grid)
            
            # Check for grid alignment
            assert(margin % min_grid == 0)
            assert(side_position % min_grid == 0)
        
            rect.moveTo(
                die_x2 - PIN_LENGTH,
                die_y1 + margin + side_position - PIN_WIDTH // 2,
            )
        
        # South side
        elif side == 'S':
            rect = odb.Rect(0, 0, PIN_WIDTH, PIN_LENGTH)
            
            if len(bterms) == 1:
                side_position = (die_width - 2*margin) // 2
            else:
                side_position = ( (die_width - 2*margin) * index // (len(bterms)-1) )
            side_position = min_grid * round(side_position/min_grid)
            
            # Check for grid alignment
            assert(margin % min_grid == 0)
            assert(side_position % min_grid == 0)
        
            rect.moveTo(
                die_x1 + margin + side_position - PIN_WIDTH // 2,
                die_y1
            )

        # West side
        elif side == 'W':
            rect = odb.Rect(0, 0, PIN_LENGTH, PIN_WIDTH)
            
            if len(bterms) == 1:
                side_position = (die_height - 2*margin) // 2
            else:
                side_position = ( (die_height - 2*margin) * index // (len(bterms)-1) )
            side_position = min_grid * round(side_position/min_grid)
            
            # Check for grid alignment
            assert(margin % min_grid == 0)
            assert(side_position % min_grid == 0)
        
            rect.moveTo(
                die_x1,
                die_y1 + margin + side_position - PIN_WIDTH // 2
            )

        else:
            raise RuntimeError('Invalid pin position')

        # Add to OpenDB
        odb.dbBox_create(bpin, layer, *rect.ll(), *rect.ur())
