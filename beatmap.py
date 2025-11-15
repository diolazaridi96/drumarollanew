# ---- beatmap.py ----
# Onset detection and basic post-processing
import librosa
import numpy as np




def get_onsets_seconds(wav_path, sr=None, backtrack=False, pre_max=0.03, post_max=0.00):
"""Return list of onset times in seconds for given wav file.
Uses librosa.onset.onset_detect with tuned parameters for drum transients.
"""
y, fs = librosa.load(wav_path, sr=sr, mono=True)


# use a higher hop length for speed if file is long
hop_length = 512


# onset detection
onsets = librosa.onset.onset_detect(y=y, sr=fs, hop_length=hop_length, units='time', backtrack=backtrack)


# Optional: filter extremely close onsets (within 40ms) to reduce double triggers
if len(onsets) > 1:
diffs = np.diff(onsets)
mask = np.concatenate(([True], diffs > 0.04)) # keep onset if >40ms from previous
onsets = list(np.array(onsets)[mask])
else:
onsets = list(onsets)


# round to 3 decimals to keep JSON small
onsets = [float(round(float(t), 3)) for t in onsets]
return onsets
