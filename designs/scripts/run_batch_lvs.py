import os
import glob
import subprocess
import sys
import argparse

# --- Configuration ---
pdk_root = os.getenv("PDK_ROOT") or ""
pdk = os.getenv("PDK") or ""

SPLIT_CELLS_DIR = "split_cells"
OUTPUT_NETLIST_DIR = "extracted_netlists"
IHP_LVS_DECK = "/".join([pdk_root, pdk, "libs.tech/klayout/tech/lvs", "sg13g2.lvs"])

# Set PDK_ROOT if using SkyWater 130nm or GF180MCU
# LVS_DECK = os.path.expandvars("$PDK_ROOT/sky130A/libs.tech/klayout/lvs/sky130.lvs")
parser = argparse.ArgumentParser(description="Batch KLayout LVS Netlist Extraction for IHP SG13G2")
parser.add_argument(
    "-i", "--input-dir",
    default=SPLIT_CELLS_DIR,
    help="Directory containing input GDS files (default: split_cells)"
)
parser.add_argument(
    "-o", "--output-dir",
    default=OUTPUT_NETLIST_DIR,
    help="Directory to save extracted SPICE netlists (default: extractected)"
)
parser.add_argument(
    "--lvs-deck",
    default=IHP_LVS_DECK,
    help="Path to IHP sg13g2.lvs script"
)

args = parser.parse_args()

split_cells_dir = args.input_dir
output_netlist_dir = args.output_dir
ihp_lvs_deck = args.lvs_deck

os.makedirs(output_netlist_dir, exist_ok=True)

# Find all GDS files in the target directory
gds_files = glob.glob(os.path.join(split_cells_dir, "*.gds"))

if not gds_files:
    print(f"No GDS files found in '{split_cells_dir}'. Exiting.")
    sys.exit(1)

print(f"Found {len(gds_files)} cell(s) to process.\n" + "-"*40)

for gds_path in gds_files:
    cell_name = os.path.splitext(os.path.basename(gds_path))[0]
    output_netlist = os.path.abspath(os.path.join(output_netlist_dir, f"{cell_name}.cir"))
    abs_gds_path = os.path.abspath(gds_path)
    
    print(f"Extracting Netlist for: {cell_name}")

    cmd = [
        "klayout",
        "-b",                                         # Headless batch mode
        "-r", ihp_lvs_deck,                           # Path to sg13g2.lvs
        "-rd", f"input={abs_gds_path}",               # <--- Match line 34: $input
        "-rd", f"topcell={cell_name}",                # <--- Match line 34: $topcell
        "-rd", f"target_netlist={output_netlist}",    # <--- Match line 78: $target_netlist
        "-rd", "net_only=true",
        "-rd", "run_mode=deep"
    ]

    try:
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"  [SUCCESS] -> Saved to {output_netlist}")
    except subprocess.CalledProcessError as e:
        print(f"  [ERROR] Extraction failed for {cell_name}:")
        print(e.stderr)

print("=" * 50)
print("IHP SG13G2 batch netlist extraction complete.")
