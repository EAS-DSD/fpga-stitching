#!/usr/bin/env python3

# Copyright (c) 2024 Leo Moser <leomoser99@gmail.com>
# SPDX-License-Identifier: Apache-2.0

import ol2_fabric_stitching

if __name__ == "__main__":

    fabric_sizes = [1,2,3,4,5,7,9,11,13,15,20,25,30]

    for i in fabric_sizes:
        ol2_fabric_stitching.main('Tile/', f'fabric{i}x{i}', 'fabrics_nl/', i, i)
