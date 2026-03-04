"""
ClipFusion — AI Evasion
Proteção contra detecção por IA das plataformas.

IAs de detecção usam:
  - Perceptual hashing (pHash, dHash)
  - Embeddings visuais (CNN features)
  - Temporal fingerprinting (motion vectors)
  - Audio fingerprinting (spectral correlation)
"""
import random


class AIEvasion:

    def __init__(self, seed: int):
        self.rng = random.Random(seed)

    def ffmpeg_filters(self) -> list:
        """
        Filtros que perturbam sistemas de detecção por IA.
        Imperceptíveis ao humano.
        """
        filters = []

        # Vignette invertido leve — perturba embeddings CNN nas bordas
        filters.append("vignette=angle=PI/5:mode=backward")

        # Temporal jitter imperceptível — perturba motion vectors
        jitter = self.rng.uniform(0.0001, 0.0003)
        filters.append(f"setpts=PTS+{jitter:.5f}*random(0)")

        # Micro-blur — sigma 0.2–0.4px, abaixo do limiar visual
        sigma = self.rng.uniform(0.2, 0.4)
        filters.append(f"gblur=sigma={sigma:.2f}")

        return filters

    def network_config(self, platform: str = "tiktok") -> dict:
        """Config de sessão para simular comportamento humano no upload."""
        agents = {
            "tiktok": [
                "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
            ],
            "instagram": [
                "Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15",
                "Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36",
            ],
            "youtube": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15",
            ],
        }
        return {
            "user_agent":    self.rng.choice(agents.get(platform, agents["tiktok"])),
            "upload_delay_s": self.rng.uniform(2.0, 8.0),
            "chunk_size_kb":  self.rng.choice([256, 512, 1024]),
        }
