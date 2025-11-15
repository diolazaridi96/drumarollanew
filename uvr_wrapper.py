# ---- uvr_wrapper.py ----
# Lazy-loading wrapper for MDX-B (drum model)
import os
import soundfile as sf


# try/except import because package name may vary slightly between versions
try:
from uvr5.mdx import MDXNet
except Exception:
MDXNet = None


_model = None


def _ensure_model():
global _model
if _model is None:
if MDXNet is None:
raise RuntimeError("uvr5 or its MDX bindings are not available. Check requirements installed.")
# 'mdx-b-drum' or similar name. This tries the common identifier.
_model = MDXNet("mdx-b-drum")
return _model




def extract_drums(input_path, output_path):
"""Extract drum stem from input audio and write WAV to output_path.
Returns output_path.
"""
model = _ensure_model()
# read input with soundfile to preserve sampling rate
audio, sr = sf.read(input_path)
# model.extract expects numpy array and sr, returns stem audio (mono or stereo)
drums = model.extract(audio, sr)
# Ensure output directory exists
os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
sf.write(output_path, drums, sr)
return output_path
