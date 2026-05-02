from pathlib import Path


def build_overlay_svg(*, width: int, height: int, contour: list, bbox: dict, output_path: Path) -> Path:
    polygon_points = " ".join(f"{point['x']},{point['y']}" for point in contour)
    rect = ""
    if bbox:
        rect = (
            f"<rect x='{bbox['x']}' y='{bbox['y']}' width='{bbox['width']}' height='{bbox['height']}' "
            "fill='#ff3b30' fill-opacity='0.15' stroke='#ff3b30' stroke-width='4' rx='8' />"
        )

    polygon = ""
    if polygon_points:
        polygon = (
            f"<polygon points='{polygon_points}' fill='#ff9500' fill-opacity='0.25' "
            "stroke='#ff9500' stroke-width='3' />"
        )

    content = (
        f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {width} {height}' "
        f"width='{width}' height='{height}'>"
        "<defs><filter id='glow'><feGaussianBlur stdDeviation='3.5' result='blur' />"
        "<feMerge><feMergeNode in='blur' /><feMergeNode in='SourceGraphic' /></feMerge></filter></defs>"
        f"<g filter='url(#glow)'>{rect}{polygon}</g></svg>"
    )
    output_path.write_text(content, encoding="utf-8")
    return output_path
