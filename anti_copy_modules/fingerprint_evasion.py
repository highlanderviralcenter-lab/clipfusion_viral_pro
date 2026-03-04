"""
ClipFusion — Fingerprint Evasion
Cor, noise, chroma, frequency, metadados — via filtros FFmpeg.
Todas imperceptíveis ao olho humano.
"""
import random, hashlib
from datetime import datetime, timedelta


class FingerprintEvasion:

    def __init__(self, seed: int):
        self.rng = random.Random(seed)

    def color_filters(self) -> list:
        """Shift RGB ±2/255. Imperceptível (limiar humano ±5/255). Muda checksum frame a frame."""
        b = self.rng.uniform(-0.006, 0.006)
        c = self.rng.uniform(0.995, 1.005)
        s = self.rng.uniform(0.996, 1.004)
        g = self.rng.uniform(0.996, 1.004)
        return [f"eq=brightness={b:.4f}:contrast={c:.4f}:saturation={s:.4f}:gamma={g:.4f}"]

    def noise_filters(self) -> list:
        """Ruído gaussiano sigma≈0.5. Altera cada pixel ±1 máx. Invalida hash frame a frame."""
        strength = self.rng.uniform(0.3, 0.6)
        return [f"noise=alls={strength:.2f}:allf=t+u"]

    def chroma_filters(self) -> list:
        """Micro-shift de hue <0.5°. Altera fingerprint de cor sem mudar luminância."""
        h = self.rng.uniform(-0.4, 0.4)
        s = self.rng.uniform(0.997, 1.003)
        return [f"hue=h={h:.3f}:s={s:.4f}"]

    def frequency_filters(self) -> list:
        """Unsharp mask imperceptível. Altera componentes de alta frequência (DCT)."""
        lx = self.rng.randint(3, 5)
        la = self.rng.uniform(-0.05, 0.05)
        cx = self.rng.randint(3, 5)
        ca = self.rng.uniform(-0.03, 0.03)
        return [f"unsharp=luma_msize_x={lx}:luma_msize_y={lx}:luma_amount={la:.3f}"
                f":chroma_msize_x={cx}:chroma_msize_y={cx}:chroma_amount={ca:.3f}"]

    def metadata_inject_args(self, project_id: str) -> list:
        """Metadados randomizados plausíveis. Determinístico por project_id."""
        rng = random.Random(int(hashlib.md5(project_id.encode()).hexdigest()[:8], 16))
        fake_date = datetime.now() - timedelta(
            days=rng.randint(0, 730), hours=rng.randint(0, 23), minutes=rng.randint(0, 59))
        encoders = ["libx264 (High@L4.1)", "H.264/AVC Codec",
                    "libx265 (Main@L4.0)", "H.264 Video"]
        comments = [f"Edit v{rng.randint(1,5)}.{rng.randint(0,9)}",
                    f"Exported at {rng.randint(1,4)}K",
                    "Processed with color grade", ""]
        return [
            "-metadata", f"creation_time={fake_date.isoformat()}",
            "-metadata", f"encoder={rng.choice(encoders)}",
            "-metadata", f"comment={rng.choice(comments)}",
            "-metadata", "copyright=", "-metadata", "description=",
            "-metadata", "title=",     "-metadata", "artist=",
            "-metadata", "album=",
        ]
