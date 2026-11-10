"""Sample signed isosurfaces from the five Lion cubegen files (requires NumPy)."""

import gzip
import json
import sys
from pathlib import Path

import numpy as np


ISOVALUE = 0.02
FILES = ("bb-beta4", "alter-beta4", "bb-alpha5", "alter-alpha5", "alter-alpha4")


def read_cube(path):
    lines = path.read_text(encoding="ascii").splitlines()
    count, *origin = map(float, lines[2].split()[:4])
    axes = np.array([line.split() for line in lines[3:6]], dtype=float)
    shape = tuple(axes[:, 0].astype(int))
    axes = axes[:, 1:]
    atoms = np.array([line.split() for line in lines[6:6 + abs(int(count))]], dtype=float)
    start = 6 + len(atoms)
    if count < 0:
        if lines[start].split()[0] != "1":
            raise ValueError(f"{path} must contain one orbital.")
        start += 1
    field = np.fromstring(" ".join(lines[start:]), sep=" ").reshape(shape)
    return atoms, np.array(origin), axes, field


def sample_surface(field, origin, axes, sign):
    field = sign * field
    gradients = np.stack(np.gradient(field), axis=-1)
    positions = []
    normals = []
    for axis in range(3):
        left = [slice(None)] * 3
        right = left.copy()
        left[axis] = slice(None, -1)
        right[axis] = slice(1, None)
        a, b = field[tuple(left)], field[tuple(right)]
        start = np.argwhere((a >= ISOVALUE) != (b >= ISOVALUE))
        end = start.copy()
        end[:, axis] += 1
        t = (ISOVALUE - field[tuple(start.T)]) / (field[tuple(end.T)] - field[tuple(start.T)])
        coords = start.astype(float)
        coords[:, axis] += t
        gradient = (1 - t[:, None]) * gradients[tuple(start.T)] + t[:, None] * gradients[tuple(end.T)]
        normal = -gradient @ np.linalg.inv(axes).T
        positions.append(origin + coords @ axes)
        normals.append(normal / np.linalg.norm(normal, axis=1, keepdims=True))
    samples = np.column_stack((np.concatenate(positions), np.concatenate(normals)))
    if not len(samples):
        raise ValueError("The requested isovalue does not intersect the cube.")
    return samples.round(3).tolist()


def main(cube_dir):
    panels = []
    for name in FILES:
        atoms, origin, axes, field = read_cube(cube_dir / f"{name}.cube")
        panels.append({
            "atoms": atoms[:, [0, 2, 3, 4]].tolist(),
            "positive": sample_surface(field, origin, axes, 1),
            "negative": sample_surface(field, origin, axes, -1),
        })
    target = Path(__file__).resolve().parent / "data/orbital-surfaces.json.gz"
    encoded = json.dumps({"isovalue": ISOVALUE, "panels": panels}, separators=(",", ":")).encode()
    target.write_bytes(gzip.compress(encoded, mtime=0))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
