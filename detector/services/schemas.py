from dataclasses import dataclass, field


@dataclass
class InferenceResult:
    tumor_detected: bool
    predicted_type: str
    confidence: float
    backend: str
    bbox: dict
    contour: list
    area_percent: float
    location_summary: str
    size_summary: str
    disclaimer: str
    low_confidence: bool = False
    notes: list[str] = field(default_factory=list)
