default: all

all: harden_tiles fabric_stitching sea_of_gates
.PHONY: all

harden_tiles:
	python3 ol2_harden_tiles.py
.PHONY: harden_tiles

generate_fabrics:
	python3 generate_fabrics.py
.PHONY: generate_fabrics

sea_of_gates_fabrics: sea_of_gates_fabric_small sea_of_gates_fabric_medium sea_of_gates_fabric_large
.PHONY: sea_of_gates_fabrics

sea_of_gates_fabric_small:
	python3 ol2_sea_of_gates.py "Tile" "fabric_small" "fabrics_nl"
.PHONY: sea_of_gates_fabric_small

sea_of_gates_fabric_medium:
	python3 ol2_sea_of_gates.py "Tile" "fabric_medium" "fabrics_nl"
.PHONY: sea_of_gates_fabric_medium

sea_of_gates_fabric_large:
	python3 ol2_sea_of_gates.py "Tile" "fabric_large" "fabrics_nl"
.PHONY: sea_of_gates_fabric_large

stitch_fabrics: stitch_fabric_small stitch_fabric_medium stitch_fabric_large
.PHONY: stitch_fabrics

stitch_fabric_small:
	python3 ol2_fabric_stitching.py "Tile" "fabric_small" "fabrics_nl" 2 2
.PHONY: stitch_fabric_small

stitch_fabric_medium:
	python3 ol2_fabric_stitching.py "Tile" "fabric_medium" "fabrics_nl" 5 5
.PHONY: stitch_fabric_medium

stitch_fabric_large:
	python3 ol2_fabric_stitching.py "Tile" "fabric_large" "fabrics_nl" 15 15
.PHONY: stitch_fabric_large


clean:
	rm -f abc.history
	rm -rf openlane_run/
	rm -rf runs/
	rm -f Tile/E_IO/abc.history
	rm -rf Tile/E_IO/openlane_run/
	rm -rf Tile/E_IO/runs/
	rm -f Tile/W_IO/abc.history
	rm -rf Tile/W_IO/openlane_run/
	rm -rf Tile/W_IO/runs/
	rm -f Tile/LUT4AB/abc.history
	rm -rf Tile/LUT4AB/openlane_run/
	rm -rf Tile/LUT4AB/runs/
	rm -f Tile/N_term_single/abc.history
	rm -rf Tile/N_term_single/openlane_run/
	rm -rf Tile/N_term_single/runs/
	rm -f Tile/S_term_single/abc.history
	rm -rf Tile/S_term_single/openlane_run/
	rm -rf Tile/S_term_single/runs/

.PHONY: clean

clean_macros:
	rm -rf Tile/E_IO/macro/
	rm -rf Tile/W_IO/macro/
	rm -rf Tile/LUT4AB/macro/
	rm -rf Tile/N_term_single/macro/
	rm -rf Tile/S_term_single/macro/
	
.PHONY: clean_macros
