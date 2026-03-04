"""
ClipFusion — Temporal Obfuscation
Speed variation ±0.5% e frame jitter via FFmpeg.
Limiar humano: ~3%. Muda fingerprint temporal completo.
"""
import random


class TemporalObfuscation:

    def __init__(self, seed: int):
        self.rng = random.Random(seed)

    def ffmpeg_filters(self) -> list:
        """setpts com fator de speed imperceptível."""
        speed = self.rng.uniform(0.995, 1.005)
        pts   = 1.0 / speed
        return [f"setpts={pts:.5f}*PTS"]

    def audio_tempo_filter(self) -> str:
        """atempo correspondente para manter sync A/V."""
        speed = self.rng.uniform(0.995, 1.005)
        return f"atempo={speed:.5f}"
