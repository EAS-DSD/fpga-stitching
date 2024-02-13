# FABulous and OpenLane 2

## Prerequisites

### FABulous

Clone the FABulous repository using:

	git clone https://github.com/FPGA-Research-Manchester/FABulous

Commit: `84edbe54954fa7d0fde93d727626acc0d0a60727`

Setup a virtual environment in Python and install the required packages as described in the `README`.

### OpenLane 2

Clone the OpenLane 2 repository using:

	git clone https://github.com/efabless/openlane2

Commit: `aef54ecd99f158610a1ce95534f7d9365e48914e`

Install and setup Nix as explained in the [documentation](https://openlane2.readthedocs.io/en/latest/getting_started/common/nix_installation/index.html).

Whenever you need to use OpenLane 2, first invoke `nix-shell` from within the OpenLane 2 repository.

## Build the Fabrics

Make sure to enable the FABulous virtual environment, now call:

	make generate_fabrics

The fabrics are generated under `output/`.

## 1. Sea of Gates - Harden the Whole Fabric

Invoke the `nix-shell` from within the OpenLane 2 repo.

Now inside this repository, call:

	make sea_of_gates_fabrics

## 2. Fabric Stitching with Custom Placement and Custom Routing TODO

Invoke the `nix-shell` from within the OpenLane 2 repo.

First, the tiles must be hardened individually. Inside this repository, call:

	make harden_tiles

After the tiles are hardened as macros, call:

	make stitch_fabrics

## Cleanup

To remove intermediate files:

	make clean

To remove the macros:

	make clean_macros