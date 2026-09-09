import os
import argparse
import sys
import klayout.db as db

# --- Configuration ---
pdk_root = os.getenv("PDK_ROOT") or ""
pdk = os.getenv("PDK") or ""

IO_LIB = "/".join([pdk_root, pdk, "libs.ref/sg13g2_io/gds",
                         "sg13g2_io.gds"])
def cells_are_identical(cell_a, cell_b):
    """
    Checks if two cells are visually and structurally identical in KLayout 0.30.x:
    - Same layer shapes/polygons via Region XOR
    - Same subcell instances (references, placement origins, transformations)
    """
    layout = cell_a.layout()

    # 1. Compare total shape count across all layers
    total_shapes_a = sum(cell_a.shapes(l).size() for l in layout.layer_indexes())
    total_shapes_b = sum(cell_b.shapes(l).size() for l in layout.layer_indexes())
    if total_shapes_a != total_shapes_b:
        return False

    # 2. Compare geometry layer by layer using Region XOR
    for layer_idx in layout.layer_indexes():
        shapes_a = cell_a.shapes(layer_idx)
        shapes_b = cell_b.shapes(layer_idx)
        # Skip empty layers
        if shapes_a.is_empty() and shapes_b.is_empty():
            continue
        region_a = db.Region(shapes_a)
        region_b = db.Region(shapes_b)
        # If boolean XOR is not empty, geometry differs
        if not (region_a ^ region_b).is_empty():
            return False

    # 3. Compare child instance transformations and cell index pointers
    insts_a = sorted([(inst.cell_index, str(inst.trans)) for inst in cell_a.each_inst()])
    insts_b = sorted([(inst.cell_index, str(inst.trans)) for inst in cell_b.each_inst()])
    if insts_a != insts_b:
        return False

    return True

def main():
    parser = argparse.ArgumentParser(
        description="Replace matching subcells in a target GDS with cells from a source GDS using KLayout."
    )
    parser.add_argument("-t", "--target", required=True, help="Path to the target GDS file")
    parser.add_argument("-s", "--source",
                        default=IO_LIB, help="Path to the source GDS file")
    parser.add_argument("-o", "--output", required=True, help="Path for the output GDS file")

    args = parser.parse_args()

    # 1. Load layouts
    print(f"Loading target layout: {args.target}")
    target_layout = db.Layout()
    target_layout.read(args.target)

    print(f"Loading source layout: {args.source}")
    source_layout = db.Layout()
    source_layout.read(args.source)

    replaced_count = 0

    target_cell_name = target_layout.top_cell().name


    # 2. Step 1: Copy tree as before
    print("Step 1: Copying matching cell trees...")
    # Overwrite matching cells
    for source_cell in source_layout.each_cell():
        cell_name = source_cell.name
        if target_layout.has_cell(cell_name):
            target_cell = target_layout.cell(cell_name)
            target_cell.clear()
            target_cell.copy_tree(source_cell)
            print(f"Replaced: {cell_name}")
            replaced_count += 1

    if replaced_count == 0:
        print("No matching cell names found between target and source.")
        sys.exit(0)

    print(f"Successfully replaced {replaced_count} cell(s) and saved to: {args.output}")

    removed_count = 0
    for top_cell in target_layout.top_cells():
        if top_cell.name != target_cell_name:
            print(f"Pruning orphan top tree: {top_cell.name}")
            top_cell.prune_cell()
            removed_count += 1

    print(f"Removed {removed_count} orphan top-level cell trees.")

    # 3. Step 2: Pre-cleaning — Normalize $ cells that have NO base cell
    print("Step 2: Normalizing $ cells with missing base names...")
    renamed_count = 0
    # Sort cell list so $1 comes before $2, $3, etc.
    all_cells = sorted(list(target_layout.each_cell()), key=lambda c: c.name)

    for cell in all_cells:
        cell_name = cell.name
        if "$" in cell_name:
            base_name = cell_name.split("$")[0]
            # If no non-suffix base cell exists yet in the layout, promote this one
            if not target_layout.has_cell(base_name):
                print(f"  - No base cell '{base_name}' found. Renaming '{cell_name}' -> '{base_name}'")
                cell.name = base_name
                renamed_count += 1

    print(f"Normalized {renamed_count} dollar-suffix cell(s) to clean base names.")

    # 4. Step 3: Resolve $1, $2 duplicate cells
    print("Step 3: Checking and replacing identical $ subcells...")
    cleaned_count = 0
    # Iterate through all cells in target layout
    for cell in list(target_layout.each_cell()):
        cell_name = cell.name
        if "$" in cell_name:
            # Extract base name (e.g., 'INV_X1' from 'INV_X1$1')
            base_name = cell_name.split("$")[0]
            if target_layout.has_cell(base_name):
                base_cell = target_layout.cell(base_name)
                # Check if $ cell is identical to base cell
                if cells_are_identical(cell, base_cell):
                    print(f"  - '{cell_name}' matches '{base_name}'. Re-linking and deleting duplicate...")
                    # Redirect all parent references pointing to $ cell back to base_cell
                    for parent_inst in list(cell.each_parent_inst()):
                        parent_cell = target_layout.cell(parent_inst.parent_cell_index())
                        inst = parent_inst.child_inst()
                        # Reassign instance pointer
                        inst.cell_index = base_cell.cell_index()
                    # Delete the $ cell and its unused subtree
                    cell.prune_cell()
                    cleaned_count += 1
                else:
                    print(f"  - WARNING: '{cell_name}' differs from '{base_name}'. Keeping separate for safety.")

    print(f"Cleaned up {cleaned_count} duplicate dollar-suffix subcells.")

    # Write result
    target_layout.write(args.output)

if __name__ == "__main__":
    main()
