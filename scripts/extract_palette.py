#!/usr/bin/env python3
"""Extract dominant colors from an image with Pillow + scikit-learn.

Usage:
    python scripts/extract_palette.py input.jpg --colors 6
    python scripts/extract_palette.py input.png --colors 8 --json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image
from sklearn.cluster import KMeans


def rgb_to_hex(rgb: np.ndarray) -> str:
    r, g, b = [int(round(v)) for v in rgb]
    return f"#{r:02X}{g:02X}{b:02X}"


def luminance(rgb: np.ndarray) -> float:
    r, g, b = rgb / 255.0
    return float(0.2126 * r + 0.7152 * g + 0.0722 * b)


def extract_palette(path: Path, colors: int, sample_size: int = 256):
    image = Image.open(path).convert("RGB")
    image.thumbnail((sample_size, sample_size))
    pixels = np.asarray(image, dtype=np.float32).reshape(-1, 3)

    # Remove almost-transparent-style white/black outliers only when they are rare.
    model = KMeans(n_clusters=colors, n_init="auto", random_state=42)
    labels = model.fit_predict(pixels)
    centers = model.cluster_centers_
    counts = np.bincount(labels, minlength=colors)
    shares = counts / counts.sum()

    order = np.argsort(shares)[::-1]
    result = []
    for rank, idx in enumerate(order, start=1):
        rgb = centers[idx]
        result.append(
            {
                "rank": rank,
                "hex": rgb_to_hex(rgb),
                "rgb": [int(round(v)) for v in rgb],
                "share": round(float(shares[idx]), 4),
                "luminance": round(luminance(rgb), 4),
            }
        )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract dominant image colors")
    parser.add_argument("image", type=Path)
    parser.add_argument("--colors", type=int, default=6)
    parser.add_argument("--sample-size", type=int, default=256)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    palette = extract_palette(args.image, args.colors, args.sample_size)
    if args.as_json:
        print(json.dumps({"image": str(args.image), "palette": palette}, indent=2))
        return

    for item in palette:
        print(
            f"{item['rank']:>2}. {item['hex']}  "
            f"rgb={tuple(item['rgb'])}  share={item['share']:.2%}"
        )


if __name__ == "__main__":
    main()
