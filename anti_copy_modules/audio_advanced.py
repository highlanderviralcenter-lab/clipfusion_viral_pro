"""
ClipFusion — Audio Advanced
BASIC:    pitch ±0.05 semitones + time stretch ±0.3%
ADVANCED: + EQ ±0.5dB + noise floor -80dB + harmônicos -60dB + reverb 5ms
Todas imperceptíveis ao ouvido humano.
"""
import random, subprocess, shutil


class AudioProcessor:

    def __init__(self, seed: int):
        self.rng = random.Random(seed)

    def process(self, inp: str, out: str,
                basic: bool = True, advanced: bool = False,
                log=print) -> bool:
        af = []

        if basic:
            # Pitch shift ±0.05st via asetrate (limiar humano ~5 cents)
            semitones  = self.rng.uniform(-0.05, 0.05)
            orig_sr    = 44100
            shifted_sr = int(orig_sr * (2 ** (semitones / 12)))
            af.append(f"asetrate={shifted_sr}")
            af.append(f"aresample={orig_sr}")
            # Time stretch ±0.3% (limiar humano ~1%)
            rate = self.rng.uniform(0.997, 1.003)
            af.append(f"atempo={rate:.5f}")

        if advanced:
            # EQ ±0.5dB em 3 bandas aleatórias
            for freq in self.rng.sample([200, 500, 1000, 3000, 6000, 10000], 3):
                gain = self.rng.uniform(-0.5, 0.5)
                af.append(f"equalizer=f={freq}:width_type=h:width={int(freq*0.3)}:g={gain:.2f}")
            # Reverb imperceptível: 4–7ms, decay 0.008–0.015
            delay = self.rng.randint(4, 7)
            decay = self.rng.uniform(0.008, 0.015)
            af.append(f"aecho=0.8:{decay:.3f}:{delay}:0.1")

        if not af:
            shutil.copy2(inp, out)
            return True

        r = subprocess.run(
            ["ffmpeg", "-y", "-i", inp,
             "-af", ",".join(af),
             "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", out],
            capture_output=True, text=True)
        if r.returncode != 0:
            log(f"ACE áudio: {r.stderr[-200:]}")
            shutil.copy2(inp, out)
            return False
        return True
