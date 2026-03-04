"""
ClipFusion — Geometric Transforms
Zoom, rotação, perspectiva via filtros FFmpeg.
"""
import random


class GeometricTransforms:

    def __init__(self, seed: int):
        self.rng = random.Random(seed)

    def ffmpeg_filters(self, rotation: bool = False, perspective: bool = False) -> list:
        filters = []

        # Zoom 1–3% — muda fingerprint de todos os frames
        zoom = self.rng.uniform(1.010, 1.030)
        filters.append(
            f"scale=iw*{zoom:.4f}:ih*{zoom:.4f},"
            f"crop=iw/{zoom:.4f}:ih/{zoom:.4f}")

        # Micro-rotação ±0.3° — imperceptível (limiar humano ~1°)
        if rotation:
            rad = self.rng.uniform(-0.3, 0.3) * 3.14159 / 180
            filters.append(f"rotate={rad:.5f}:fillcolor=black:expand=0")

        # Perspectiva micro-warp — só MAXIMUM
        if perspective:
            ox = self.rng.uniform(0.001, 0.003)
            oy = self.rng.uniform(0.001, 0.003)
            filters.append(
                f"perspective="
                f"x0=iw*{ox:.4f}:y0=ih*{oy:.4f}:"
                f"x1=iw*(1-{ox:.4f}):y1=ih*{oy:.4f}:"
                f"x2=iw*{ox:.4f}:y2=ih*(1-{oy:.4f}):"
                f"x3=iw*(1-{ox:.4f}):y3=ih*(1-{oy:.4f}):"
                f"interpolation=linear")

        return filters
