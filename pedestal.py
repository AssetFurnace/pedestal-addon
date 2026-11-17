#!/usr/bin/env python3
"""Build a round stepped pedestal and export it as a GLB.

Run inside Blender:

    blender -b -P pedestal.py -- <out-dir> --height 0.6 --width 0.4 --steps 3

The result is written to `<out-dir>/<out-dir-name>.glb`.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse arguments that appear after the `--` separator."""
    argv = argv if argv is not None else sys.argv
    try:
        split = argv.index("--")
        own = argv[split + 1 :]
    except ValueError:
        own = argv[1:]

    parser = argparse.ArgumentParser(description="Build a round stepped pedestal")
    parser.add_argument("out", type=Path, help="output directory")
    parser.add_argument("--height", type=float, default=0.6, help="total height in metres")
    parser.add_argument("--width", type=float, default=0.4, help="bottom width in metres")
    parser.add_argument("--steps", type=int, default=3, help="number of steps")
    return parser.parse_args(own)


def clear_scene() -> None:
    """Remove every object, mesh and material from the current scene."""
    import bpy

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for block in list(bpy.data.meshes) + list(bpy.data.materials):
        bpy.data.block_remove(block)


def build_pedestal(height: float, width: float, steps: int):
    """Create a stepped cylinder in the current scene and return the top object."""
    import bpy

    if steps < 1:
        raise ValueError("steps must be at least 1")
    if height <= 0 or width <= 0:
        raise ValueError("height and width must be positive")

    step_height = height / steps
    radius_step = (width / 2) / steps
    bpy.ops.mesh.primitive_cylinder_add(radius=width / 2, depth=step_height, location=(0, 0, step_height / 2))
    bottom = bpy.context.active_object
    bottom.name = "pedestal_step_0"

    for i in range(1, steps):
        radius = width / 2 - i * radius_step
        z = i * step_height + step_height / 2
        bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=step_height, location=(0, 0, z))
        step = bpy.context.active_object
        step.name = f"pedestal_step_{i}"

    # The top step is the one we just created, or the bottom one if single step.
    return bpy.context.active_object


def export_glb(out_dir: Path) -> Path:
    """Export the current scene as a GLB named after the output folder."""
    import bpy

    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{out_dir.name}.glb"
    bpy.ops.export_scene.gltf(
        filepath=str(path),
        export_format="GLB",
        export_yup=True,
        export_apply=True,
    )
    return path


def main(argv: list[str] | None = None) -> Path:
    args = parse_args(argv)
    clear_scene()
    build_pedestal(args.height, args.width, args.steps)
    return export_glb(args.out)


if __name__ == "__main__":
    main()
