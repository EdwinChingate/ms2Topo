from __future__ import annotations
from detect_spectral_signal_mode import *

# TODO: unresolved names: oms

def centroid_profile_ms2_spectrum_if_needed(spectral_signals):
    spectral_signal_mode = detect_spectral_signal_mode(spectral_signals = spectral_signals)

    if spectral_signal_mode != oms.SpectrumSettings.SpectrumType.PROFILE:
        return spectral_signals

    input_experiment = oms.MSExperiment()
    output_experiment = oms.MSExperiment()

    input_experiment.addSpectrum(spectral_signals)

    oms.PeakPickerHiRes().pickExperiment(input_experiment,
                                         output_experiment,
                                         True)

    if len(output_experiment) == 0:
        return spectral_signals

    centroided_ms2_spectrum = output_experiment[0]
    return centroided_ms2_spectrum