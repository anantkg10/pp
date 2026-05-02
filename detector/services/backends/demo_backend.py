from __future__ import annotations

import numpy as np
from PIL import Image
from django.conf import settings

from ..schemas import InferenceResult
from .shared import DISCLAIMER, center_weight, largest_region, location_summary, suppress_borders


class DemoBackend:
    backend_name = "demo_heuristic"

    def predict(self, image: Image.Image, notes: list[str] | None = None) -> InferenceResult:
        array = np.asarray(image, dtype=np.float32) / 255.0
        contrast = float(array.std())
        weighted = center_weight(array)
        threshold = min(0.93, float(weighted.mean() + weighted.std() * 1.6))
        mask = weighted >= threshold
        mask = suppress_borders(mask)

        bbox, contour, area_percent = largest_region(mask)
        tumor_detected = bbox["width"] > 0 and area_percent > 0.2 and contrast > 0.05

        if tumor_detected:
            predicted_type = self._guess_tumor_type(bbox, image.width, image.height, area_percent)
            confidence = min(0.95, max(0.57, 0.55 + area_percent / 18))
            location = location_summary(bbox, image.width, image.height)
            size_summary = f"Highlighted region covers about {area_percent:.2f}% of the image area."
        else:
            predicted_type = "No strong tumor signal"
            confidence = 0.41
            location = "No stable focal region found."
            size_summary = "No tumor-sized highlight passed the current threshold."

        low_confidence = confidence < settings.MRI_CONFIDENCE_WARNING_THRESHOLD
        return InferenceResult(
            tumor_detected=tumor_detected,
            predicted_type=predicted_type,
            confidence=round(confidence, 2),
            backend=self.backend_name,
            bbox=bbox,
            contour=contour,
            area_percent=round(area_percent, 2),
            location_summary=location,
            size_summary=size_summary,
            disclaimer=DISCLAIMER,
            low_confidence=low_confidence,
            notes=notes or [],
        )

    def _guess_tumor_type(self, bbox: dict, width: int, height: int, area_percent: float) -> str:
        center_x = bbox["x"] + bbox["width"] / 2
        center_y = bbox["y"] + bbox["height"] / 2
        peripheral = center_x < width * 0.28 or center_x > width * 0.72
        central_low = width * 0.35 < center_x < width * 0.65 and center_y > height * 0.55
        if central_low and area_percent < 5.0:
            return "Pituitary-like pattern"
        if peripheral and area_percent < 8.0:
            return "Meningioma-like pattern"
        return "Glioma-like pattern"
