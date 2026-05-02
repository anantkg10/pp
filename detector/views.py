from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import DetailView

from .forms import PredictionUploadForm
from .models import Prediction
from .services.inference import BrainMRIPredictor, persist_prediction_result, result_to_payload


def home(request):
    form = PredictionUploadForm(request.POST or None, request.FILES or None)
    recent_predictions = Prediction.objects.all()[:5]

    if request.method == "POST" and form.is_valid():
        prediction = Prediction.objects.create(upload_image=form.cleaned_data["image"])
        predictor = BrainMRIPredictor()
        result = predictor.run(prediction)
        persist_prediction_result(prediction, result)
        return redirect("prediction-result", pk=prediction.pk)

    return render(
        request,
        "detector/home.html",
        {"form": form, "recent_predictions": recent_predictions},
    )


class PredictionResultView(DetailView):
    model = Prediction
    template_name = "detector/result.html"
    context_object_name = "prediction"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prediction = context["prediction"]
        context["low_confidence"] = prediction.confidence < 0.65
        return context


@require_POST
def predict_api(request):
    form = PredictionUploadForm(request.POST, request.FILES)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

    prediction = Prediction.objects.create(upload_image=form.cleaned_data["image"])
    predictor = BrainMRIPredictor()
    result = predictor.run(prediction)
    persist_prediction_result(prediction, result)
    return JsonResponse(result_to_payload(prediction, result), status=201)
