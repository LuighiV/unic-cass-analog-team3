# Scripts Directory

This directory contains utility scripts and configuration files for IC design tools and workflows.

## Klayout Library Management Plugin

### klayout_lib_manager.py
This script is a KLayout plugin for automatic library management and GDS file loading. The plugin
- Scans `~/designs/libs` for all `.gds` files
- Automatically registers a dedicated library for each gds file.
- Provides a "Reload Libraries" menu action (Ctrl+R)
- Saves library registry to `libs.json` for tracking

**Usage**
- Drag and instantiate cells from the library dropdown, don't use import gds.
- Edit gds files in different panels.
- To update the layout for all hierarchies, save the edited gds file, and click "Reload Libraries" in the menu bar.

An alias is defined in `designs/.designinit` to load the library managment plugin by default.
```bash
alias klayout='klayout -rm $DESIGNS/scripts/klayout_lib_manager.py -e'
```
Launch Klayout with:
```
klayout
```

## Notes
- The `scripts` directory is part of the system `PATH` and all the executable scripts can be invoked anywhere in the design space.
- Klayout lib manager script was originally taken from https://github.com/Jianxun/iic-osic-tools-project-template/tree/main by Jianxun Zhu <zhujianxun.bupt@gmail.com> adapted for the UNICASS environment.
