from django.db import models


class Prediction(models.Model):
    upload_image = models.ImageField(upload_to="uploads/")
    processed_image = models.ImageField(upload_to="processed/", blank=True)
    overlay_image = models.ImageField(upload_to="overlays/", blank=True)
    tumor_detected = models.BooleanField(default=False)
    predicted_type = models.CharField(max_length=64, blank=True)
    confidence = models.FloatField(default=0.0)
    backend = models.CharField(max_length=32, default="demo_heuristic")
    bbox = models.JSONField(default=dict, blank=True)
    contour = models.JSONField(default=list, blank=True)
    area_percent = models.FloatField(default=0.0)
    location_summary = models.CharField(max_length=255, blank=True)
    size_summary = models.CharField(max_length=255, blank=True)
    disclaimer = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Prediction #{self.pk}"
