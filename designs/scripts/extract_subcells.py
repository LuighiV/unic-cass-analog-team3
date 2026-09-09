import os
import klayout.db as db

input_path= "/home/designer/designs/libs/IHP__MPC0349/MPC0349-main/layout/klayout"
gds_name = "user_project_wrapper_updated"
input_gds = input_path +"/"+ gds_name +".gds"
target_top_cell_name = "user_project_wrapper"
output_dir = "outputs/extracted_subcells_updated"
os.makedirs(output_dir, exist_ok=True)

# 1. Load the main layout
src_layout = db.Layout()
src_layout.read(input_gds)

# 2. Find the target top cell
top_cell = src_layout.cell(target_top_cell_name)

if top_cell is None:
    raise ValueError(f"Cell '{target_top_cell_name}' not found in {input_gds}")

print(f"Inspecting child cells placed inside '{target_top_cell_name}'...")

# 3. Collect unique subcells instantiated directly inside top_cell
# Use a set to avoid extracting the same cell multiple times if placed repeatedly
child_cell_indices = set()
for inst in top_cell.each_inst():
    child_cell_indices.add(inst.cell_index)

print(f"Found {len(child_cell_indices)} unique subcell(s) inside {target_top_cell_name}.\n")

# 4. Extract and save each placed subcell using KLayout 0.30.5 syntax
for child_idx in child_cell_indices:
    src_subcell = src_layout.cell(child_idx)
    subcell_name = src_subcell.name
    print(f" -> Extracting subcell: {subcell_name}")

    # Create destination layout container
    dst_layout = db.Layout()
    dst_layout.dbu = src_layout.dbu

    # Create corresponding root cell in destination layout
    dst_cell = dst_layout.create_cell(subcell_name)

    # Replicate entire hierarchy tree under this subcell
    mapping = db.CellMapping()
    mapping.for_single_cell_full(dst_cell, src_subcell)
    dst_layout.copy_tree_shapes(src_layout, mapping)

    # Save to file
    out_path = os.path.join(output_dir, f"{subcell_name}.gds")
    dst_layout.write(out_path)
    print(f"    Saved: {out_path}")

print("\nDone extracting placed subcells.")
