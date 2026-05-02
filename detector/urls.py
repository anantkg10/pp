from django.urls import path

from .views import PredictionResultView, home, predict_api


urlpatterns = [
    path("", home, name="detector-home"),
    path("predictions/<int:pk>/", PredictionResultView.as_view(), name="prediction-result"),
    path("api/predict/", predict_api, name="predict-api"),
]
