# Lightweight wrapper around Wav2Vec2 base for 768-D embeddings.

from pathlib import Path
import torch, torchaudio

class EmbeddingExtractor:
    def __init__(self, device: str | None = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        bundle = torchaudio.pipelines.WAV2VEC2_BASE
        self.model = bundle.get_model().to(self.device).eval()
        self.sample_rate = bundle.sample_rate
        self._resample = torchaudio.transforms.Resample(
            orig_freq=48_000, new_freq=self.sample_rate
        )

    @torch.inference_mode()
    def __call__(self, wav_path: Path) -> torch.Tensor:
        wav, sr = torchaudio.load(wav_path)
        if sr != self.sample_rate:
            wav = self._resample(wav)

        wav = wav.to(self.device)
        reps, _ = self.model.extract_features(wav)  # list of layers
        vec = reps[-1].mean(dim=-1).squeeze(0)      # (768, _)
        return vec.cpu()
