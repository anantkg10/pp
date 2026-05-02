from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Prediction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("upload_image", models.ImageField(upload_to="uploads/")),
                ("processed_image", models.ImageField(blank=True, upload_to="processed/")),
                ("overlay_image", models.ImageField(blank=True, upload_to="overlays/")),
                ("tumor_detected", models.BooleanField(default=False)),
                ("predicted_type", models.CharField(blank=True, max_length=64)),
                ("confidence", models.FloatField(default=0.0)),
                ("backend", models.CharField(default="demo_heuristic", max_length=32)),
                ("bbox", models.JSONField(blank=True, default=dict)),
                ("contour", models.JSONField(blank=True, default=list)),
                ("area_percent", models.FloatField(default=0.0)),
                ("location_summary", models.CharField(blank=True, max_length=255)),
                ("size_summary", models.CharField(blank=True, max_length=255)),
                ("disclaimer", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        )
    ]
