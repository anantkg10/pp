from __future__ import annotations

from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image
from django.conf import settings
from django.core.files.base import ContentFile

from ..overlays import build_overlay_svg

DISCLAIMER = (
    "Prototype result for research and educational use only. "
    "This output is not a diagnosis and must be reviewed by a qualified clinician."
)


def save_processed_image(prediction, image: Image.Image) -> str:
    processed_image = image.convert("RGB")
    buffer = BytesIO()
    processed_image.save(buffer, format="PNG")
    payload = ContentFile(buffer.getvalue())
    filename = f"prediction_{prediction.pk}.png"
    prediction.processed_image.save(filename, payload, save=False)
    return prediction.processed_image.name


def save_overlay(prediction, image: Image.Image, result) -> str:
    output_dir = Path(settings.MEDIA_ROOT) / "overlays"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"prediction_{prediction.pk}.svg"
    build_overlay_svg(
        width=image.width,
        height=image.height,
        contour=result.contour,
        bbox=result.bbox,
        output_path=output_path,
    )
    return f"overlays/prediction_{prediction.pk}.svg"


def center_weight(array: np.ndarray) -> np.ndarray:
    height, width = array.shape
    ys, xs = np.ogrid[:height, :width]
    x_term = ((xs - width / 2) / max(width / 2, 1)) ** 2
    y_term = ((ys - height / 2) / max(height / 2, 1)) ** 2
    radial = np.clip(1.15 - 0.7 * (x_term + y_term), 0.15, 1.15)
    return array * radial


def suppress_borders(mask: np.ndarray) -> np.ndarray:
    trimmed = mask.copy()
    margin_y = max(2, mask.shape[0] // 20)
    margin_x = max(2, mask.shape[1] // 20)
    trimmed[:margin_y, :] = False
    trimmed[-margin_y:, :] = False
    trimmed[:, :margin_x] = False
    trimmed[:, -margin_x:] = False
    return trimmed


def largest_region(mask: np.ndarray) -> tuple[dict, list, float]:
    height, width = mask.shape
    visited = np.zeros_like(mask, dtype=bool)
    best_coords: list[tuple[int, int]] = []

    for y in range(height):
        for x in range(width):
            if not mask[y, x] or visited[y, x]:
                continue
            region = []
            stack = [(y, x)]
            visited[y, x] = True
            while stack:
                cy, cx = stack.pop()
                region.append((cy, cx))
                for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                    if 0 <= ny < height and 0 <= nx < width and mask[ny, nx] and not visited[ny, nx]:
                        visited[ny, nx] = True
                        stack.append((ny, nx))
            if len(region) > len(best_coords):
                best_coords = region

    if not best_coords:
        return {"x": 0, "y": 0, "width": 0, "height": 0}, [], 0.0

    ys = [coord[0] for coord in best_coords]
    xs = [coord[1] for coord in best_coords]
    min_y, max_y = min(ys), max(ys)
    min_x, max_x = min(xs), max(xs)
    bbox = {
        "x": int(min_x),
        "y": int(min_y),
        "width": int(max_x - min_x + 1),
        "height": int(max_y - min_y + 1),
    }
    contour = [
        {"x": int(min_x), "y": int(min_y)},
        {"x": int(max_x), "y": int(min_y)},
        {"x": int(max_x), "y": int(max_y)},
        {"x": int(min_x), "y": int(max_y)},
    ]
    area_percent = len(best_coords) * 100.0 / float(height * width)
    return bbox, contour, area_percent


def location_summary(bbox: dict, width: int, height: int) -> str:
    center_x = bbox["x"] + bbox["width"] / 2
    center_y = bbox["y"] + bbox["height"] / 2
    horizontal = "left" if center_x < width / 3 else "right" if center_x > (2 * width / 3) else "central"
    vertical = "upper" if center_y < height / 3 else "lower" if center_y > (2 * height / 3) else "mid-brain"
    return f"Primary highlight appears in the {vertical} {horizontal} region."
