from django.contrib import admin

from .models import Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created_at",
        "tumor_detected",
        "predicted_type",
        "confidence",
        "backend",
    )
    list_filter = ("tumor_detected", "predicted_type", "backend")
    search_fields = ("location_summary", "size_summary")
