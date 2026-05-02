from io import BytesIO

import numpy as np
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import Prediction
from .services.inference import BrainMRIPredictor


def build_test_upload(*, bright_box: bool) -> SimpleUploadedFile:
    array = np.full((128, 128), 28, dtype=np.uint8)
    if bright_box:
        array[16:112, 16:112] = 76
        array[44:82, 70:101] = 240
    image = Image.fromarray(array, mode="L")
    payload = BytesIO()
    image.save(payload, format="PNG")
    return SimpleUploadedFile("mri.png", payload.getvalue(), content_type="image/png")


class InferenceServiceTests(TestCase):
    def test_demo_backend_detects_bright_region(self):
        prediction = Prediction.objects.create(upload_image=build_test_upload(bright_box=True))
        result = BrainMRIPredictor(backend_mode="demo").run(prediction)

        self.assertTrue(result.tumor_detected)
        self.assertGreater(result.area_percent, 0)
        self.assertTrue(result.bbox["width"] > 0)

    def test_demo_backend_handles_empty_scan(self):
        prediction = Prediction.objects.create(upload_image=build_test_upload(bright_box=False))
        result = BrainMRIPredictor(backend_mode="demo").run(prediction)

        self.assertFalse(result.tumor_detected)
        self.assertEqual(result.predicted_type, "No strong tumor signal")


class DetectorViewsTests(TestCase):
    def test_home_page_renders(self):
        response = self.client.get(reverse("detector-home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brain MRI Tumor Detection")

    def test_upload_flow_creates_prediction_and_redirects(self):
        response = self.client.post(
            reverse("detector-home"),
            {"image": build_test_upload(bright_box=True)},
        )

        self.assertEqual(response.status_code, 302)
        prediction = Prediction.objects.get()
        self.assertTrue(prediction.overlay_image.name.endswith(".svg"))
        self.assertRedirects(response, reverse("prediction-result", kwargs={"pk": prediction.pk}))

    def test_api_returns_structured_prediction(self):
        response = self.client.post(
            reverse("predict-api"),
            {"image": build_test_upload(bright_box=True)},
        )

        self.assertEqual(response.status_code, 201)
        payload = response.json()
        self.assertIn("prediction_id", payload)
        self.assertIn("overlay_url", payload)
        self.assertIn("location_summary", payload)

    def test_invalid_file_type_is_rejected(self):
        bad_file = SimpleUploadedFile(
            "not-mri.txt",
            b"plain-text",
            content_type="text/plain",
        )
        response = self.client.post(reverse("predict-api"), {"image": bad_file})
        self.assertEqual(response.status_code, 400)
