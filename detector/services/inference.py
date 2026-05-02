from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from PIL import Image, ImageOps

from .backends.demo_backend import DemoBackend
from .backends.shared import save_overlay, save_processed_image
from .schemas import InferenceResult


class BrainMRIPredictor:
    def __init__(self, backend_mode: str | None = None):
        self.demo_backend = DemoBackend()

    def run(self, prediction) -> InferenceResult:
        image_path = Path(prediction.upload_image.path)
        image = Image.open(image_path)
        image = ImageOps.exif_transpose(image).convert("L")
        image = ImageOps.autocontrast(image)

        processed_name = save_processed_image(prediction, image)
        prediction.processed_image.name = processed_name

        result = self.demo_backend.predict(image)

        overlay_name = save_overlay(prediction, image, result)
        prediction.overlay_image.name = overlay_name
        return result


def persist_prediction_result(prediction, result: InferenceResult) -> None:
    prediction.tumor_detected = result.tumor_detected
    prediction.predicted_type = result.predicted_type
    prediction.confidence = result.confidence
    prediction.backend = result.backend
    prediction.bbox = result.bbox
    prediction.contour = result.contour
    prediction.area_percent = result.area_percent
    prediction.location_summary = result.location_summary
    prediction.size_summary = result.size_summary
    prediction.disclaimer = result.disclaimer
    prediction.save(
        update_fields=[
            "processed_image",
            "overlay_image",
            "tumor_detected",
            "predicted_type",
            "confidence",
            "backend",
            "bbox",
            "contour",
            "area_percent",
            "location_summary",
            "size_summary",
            "disclaimer",
        ]
    )


def result_to_payload(prediction, result: InferenceResult) -> dict:
    payload = asdict(result)
    payload.update(
        {
            "prediction_id": prediction.pk,
            "original_url": prediction.upload_image.url,
            "processed_url": prediction.processed_image.url if prediction.processed_image else "",
            "overlay_url": prediction.overlay_image.url if prediction.overlay_image else "",
        }
    )
    return payload
