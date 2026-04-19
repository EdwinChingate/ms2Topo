from __future__ import annotations
from ms2_spectrum import *
from format_fragment_peak_table_as_legacy_ms2_spectrum import *
import numpy as np
import os
import pandas as pd

def All_ms2_spectra(DataSet,
                    SummMS2,
                    DataSetName,
                    minInt = 1e3,
                    LogFileName = 'LogFile_ms2.csv',
                    minPeaks = 1,
                    saveFolder = 'ms2_spectra',
                    save = True):
    SpectraFoler = saveFolder + '/' + DataSetName.replace('.', '')

    Columns = ['mz(Da)',
               'mz_std(Da)',
               'Int',
               'Gauss_r2',
               'N_signals',
               'Confidence_interval(Da)',
               'Confidence_interval(ppm)',
               'mz_min(Da)',
               'mz_max(Da)',
               'RelativeIntensity(%)']

    NotExistSave = not os.path.exists(saveFolder)
    if NotExistSave and save:
        os.mkdir(saveFolder)

    NotExistSpecFol = not os.path.exists(SpectraFoler)
    if NotExistSpecFol and save:
        os.mkdir(SpectraFoler)

    if save:
        SummMS2DF = pd.DataFrame(SummMS2,
                                 columns = ['mz(Da)',
                                            'RT(s)',
                                            'id',
                                            'maxInt',
                                            'maxInt_frac'])

        SummMS2DF.to_excel(SpectraFoler + '-ms2Summary.xlsx')

    SpectraList = []
    N_spec = len(SummMS2[:, 2])

    for spectrum_id in np.arange(N_spec,
                                 dtype = 'int'):
        ms_id = int(SummMS2[spectrum_id, 2])

        SpectralSignals = DataSet[int(ms_id)]

        try:
            Spectrum = ms2_spectrum(spectral_signals = SpectralSignals,
                                    min_peaks = minPeaks)
        except TypeError:
            RawSpectrum = np.array(SpectralSignals.get_peaks()).T

            Spectrum = ms2_spectrum(RawSpectrum = RawSpectrum,
                                    DataSetName = DataSetName,
                                    ms_id = ms_id,
                                    minInt = minInt,
                                    LogFileName = LogFileName,
                                    minPeaks = minPeaks)

        Spectrum = format_fragment_peak_table_as_legacy_ms2_spectrum(fragment_peak_table = Spectrum)

        SpectraList.append(Spectrum)

        if save and len(Spectrum) > 0:
            SpectrumDF = pd.DataFrame(Spectrum,
                                      columns = Columns)

            FileName = SpectraFoler + '/' + str(spectrum_id) + '.csv'
            SpectrumDF.to_csv(FileName)

    return SpectraList
