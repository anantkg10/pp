from django import forms


class PredictionUploadForm(forms.Form):
    image = forms.ImageField(
        help_text="Upload a brain MRI slice as PNG, JPG, or JPEG."
    )

    def clean_image(self):
        image = self.cleaned_data["image"]
        valid_types = {"image/png", "image/jpeg"}
        if image.content_type not in valid_types:
            raise forms.ValidationError("Please upload a PNG or JPEG MRI image.")
        max_size = 8 * 1024 * 1024
        if image.size > max_size:
            raise forms.ValidationError("Please keep uploads below 8 MB.")
        return image
