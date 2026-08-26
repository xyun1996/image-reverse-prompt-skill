from pathlib import Path

import numpy as np
from PIL import Image
from sklearn.cluster import KMeans


def _hex(rgb: list[int]) -> str:
    return "#" + "".join(f"{v:02X}" for v in rgb)


def extract_palette(image_path: Path, num_colors: int = 6) -> dict:
    image = Image.open(image_path).convert("RGB")
    image.thumbnail((256, 256))
    pixels = np.asarray(image).reshape(-1, 3)
    model = KMeans(n_clusters=num_colors, n_init="auto", random_state=42)
    labels = model.fit_predict(pixels)
    centers = model.cluster_centers_.round().astype(int)
    counts = np.bincount(labels, minlength=num_colors)
    total = counts.sum()
    rows = []
    for idx in np.argsort(counts)[::-1]:
        rgb = centers[idx].tolist()
        rows.append({"hex": _hex(rgb), "rgb": rgb, "share": float(counts[idx] / total)})
    return {"image": str(image_path), "colors": rows}
