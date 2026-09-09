import os
import argparse
import klayout.db as db


def rescale_layout_to_dbu(src_layout, target_dbu):
    """Rescales src_layout in-place to match target_dbu."""
    if abs(src_layout.dbu - target_dbu) < 1e-12:
        return src_layout

    scale_factor = src_layout.dbu / target_dbu
    print(f"    [DBU MISMATCH] Rescaling layout from {src_layout.dbu} um to {target_dbu} um (Factor: {scale_factor})")

    # Integer complex transformation for scaling
    trans = db.ICplxTrans(scale_factor, 0.0, False, 0, 0)
    src_layout.transform(trans)
    src_layout.dbu = target_dbu

    return src_layout


def generate_xor_layout(layout_a, layout_b):
    """Generates an XOR layout container containing mismatch polygons."""
    out_layout = db.Layout()
    out_layout.dbu = layout_a.dbu
    out_top = out_layout.create_cell("XOR_TOP")

    top_a = layout_a.top_cells()[0]
    top_b = layout_b.top_cells()[0]

    layers_a = {(info.layer, info.datatype) for info in layout_a.layer_infos()}
    layers_b = {(info.layer, info.datatype) for info in layout_b.layer_infos()}
    all_layers = layers_a.union(layers_b)

    for layer_num, datatype in all_layers:
        info = db.LayerInfo(layer_num, datatype)
        idx_a = layout_a.find_layer(info)
        idx_b = layout_b.find_layer(info)

        region_a = db.Region(top_a.begin_shapes_rec(idx_a)) if idx_a != -1 else db.Region()
        region_b = db.Region(top_b.begin_shapes_rec(idx_b)) if idx_b != -1 else db.Region()

        xor_region = region_a ^ region_b

        if not xor_region.is_empty():
            out_layer_idx = out_layout.insert_layer(info)
            out_top.shapes(out_layer_idx).insert(xor_region)

    return out_layout


def run_klayout_xor(path_a, path_b, out_path):
    """Reads layouts, normalizes DBU, and runs LayoutDiff."""
    layout_a = db.Layout()
    layout_a.read(path_a)

    layout_b = db.Layout()
    layout_b.read(path_b)

    # Normalize layout_b DBU to match layout_a DBU if necessary
    if abs(layout_a.dbu - layout_b.dbu) > 1e-12:
        layout_b = rescale_layout_to_dbu(layout_b, layout_a.dbu)

    diff = db.LayoutDiff()
    diff.exact = True
    diff.ignore_text = True

    # FIX: Correct LayoutDiff.compare signature (Layout a, Layout b)
    is_same = diff.compare(layout_a, layout_b)

    if not is_same:
        # Generate and save the XOR difference GDS when a mismatch is found
        xor_layout = generate_xor_layout(layout_a, layout_b)
        xor_layout.write(out_path)
        return True

    return False

def run_pure_polygon_xor(path_a, path_b, out_path):
    """Performs geometric-only XOR ignoring cell names and metadata."""
    layout_a = db.Layout()
    layout_a.read(path_a)

    layout_b = db.Layout()
    layout_b.read(path_b)

    target_dbu = layout_a.dbu

    # Normalize layout_b DBU to layout_a DBU if necessary
    if abs(layout_b.dbu - target_dbu) > 1e-12:
        scale_factor = layout_b.dbu / target_dbu
        trans = db.ICplxTrans(scale_factor, 0.0, False, 0, 0)
        layout_b.transform(trans)
        layout_b.dbu = target_dbu

    top_a = layout_a.top_cells()[0]
    top_b = layout_b.top_cells()[0]

    # Collect all unique layer/datatype pairs across both layouts
    layers_a = {(info.layer, info.datatype) for info in layout_a.layer_infos()}
    layers_b = {(info.layer, info.datatype) for info in layout_b.layer_infos()}
    all_layers = layers_a.union(layers_b)

    out_layout = db.Layout()
    out_layout.dbu = target_dbu
    out_top = out_layout.create_cell("XOR_TOP")

    has_differences = False

    for layer_num, datatype in all_layers:
        info = db.LayerInfo(layer_num, datatype)
        idx_a = layout_a.find_layer(info)
        idx_b = layout_b.find_layer(info)

        # Collect flat recursive shapes for this layer
        region_a = db.Region(top_a.begin_shapes_rec(idx_a)) if idx_a != -1 else db.Region()
        region_b = db.Region(top_b.begin_shapes_rec(idx_b)) if idx_b != -1 else db.Region()

        # Perform boolean XOR on physical polygons
        xor_region = region_a ^ region_b

        if not xor_region.is_empty():
            has_differences = True
            out_layer_idx = out_layout.insert_layer(info)
            out_top.shapes(out_layer_idx).insert(xor_region)

    if has_differences:
        out_layout.write(out_path)
        return True

    return False


def main():
    parser = argparse.ArgumentParser(description="Batch XOR using KLayout LayoutDiff with DBU normalization.")
    parser.add_argument("-a", "--dir-a", required=True, help="Path to first GDS directory")
    parser.add_argument("-b", "--dir-b", required=True, help="Path to second GDS directory")
    parser.add_argument("-o", "--out-dir", default="xor_results", help="Path to output directory")

    args = parser.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    files_a = {f for f in os.listdir(args.dir_a) if f.endswith(".gds")}
    files_b = {f for f in os.listdir(args.dir_b) if f.endswith(".gds")}
    common_files = sorted(list(files_a.intersection(files_b)))

    if not common_files:
        print(f"No common .gds files found between '{args.dir_a}' and '{args.dir_b}'.")
        return

    print(f"Found {len(common_files)} common GDS file(s). Running LayoutDiff...\n" + "=" * 50)

    for gds_filename in common_files:
        path_a = os.path.join(args.dir_a, gds_filename)
        path_b = os.path.join(args.dir_b, gds_filename)
        out_path = os.path.join(args.out_dir, f"diff_{gds_filename}")

        print(f"Processing: {gds_filename}")
        diff_found = run_pure_polygon_xor(path_a, path_b, out_path)

        if diff_found:
            print(f"  [MISMATCH DETECTED] -> Diff saved to {out_path}")
        else:
            print("  [MATCH OK] -> Layouts are identical.")

    print("=" * 50)
    print("Batch LayoutDiff complete.")


if __name__ == "__main__":
    main()
