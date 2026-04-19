from __future__ import annotations
# TODO: unresolved names: oms

def detect_spectral_signal_mode(spectral_signals):
    try:
        spectral_signal_mode = spectral_signals.getType()
    except Exception:
        spectral_signal_mode = oms.SpectrumSettings.SpectrumType.UNKNOWN
    return spectral_signal_mode