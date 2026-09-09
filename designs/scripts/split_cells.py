import os
import klayout.db as db

pdk_root = os.getenv("PDK_ROOT") or ""
pdk = os.getenv("PDK") or ""
gds_name = "sg13g2_io.gds"
input_gds = "/".join([pdk_root,
                      pdk,
                      "libs.ref/sg13g2_io/gds",
                      gds_name])
output_dir = "split_cells"
os.makedirs(output_dir, exist_ok=True)

# 1. Read source layout
src_layout = db.Layout()
src_layout.read(input_gds)

# 2. Find true top-level cells (cells not instantiated by any other cell)
top_cells = src_layout.top_cells()
print(f"Found {len(top_cells)} top-level cell(s) in {input_gds}:")

for src_cell in top_cells:
    cell_name = src_cell.name
    print(f" -> Extracting: {cell_name}")

    # Create destination layout container
    dst_layout = db.Layout()
    dst_layout.dbu = src_layout.dbu

    # Create root cell in target layout
    dst_cell = dst_layout.create_cell(cell_name)

    # Map target cell (first) to source cell (second) and create full subcell mapping
    mapping = db.CellMapping()
    mapping.for_single_cell_full(dst_cell, src_cell)

    # Copy shapes and instances recursively into target layout
    dst_layout.copy_tree_shapes(src_layout, mapping)

    # Save isolated cell to file
    out_path = os.path.join(output_dir, f"{cell_name}.gds")
    dst_layout.write(out_path)
    print(f"    Saved: {out_path}")

print("\nDone splitting cells.")
