from __future__ import annotations
from AllMS2Data import *
from ChargeDataSet_in_AnotherFolder import *
from centroid_profile_ms2_spectrum_if_needed import *
from compute_relative_fragment_intensity_percent import *
from extract_fragment_peak_table import *
from remove_nonpositive_fragment_peaks import *
from sort_fragment_peak_table_by_intensity import *

# TODO: unresolved names: x

def ms2_spectrum(spectral_signals,
                 min_peaks = 1):
    if spectral_signals.getMSLevel() != 2:
        return []

    centroided_ms2_spectrum = centroid_profile_ms2_spectrum_if_needed(spectral_signals = spectral_signals)

    fragment_peak_table = extract_fragment_peak_table(spectral_signals = centroided_ms2_spectrum)

    fragment_peak_table = remove_nonpositive_fragment_peaks(fragment_peak_table = fragment_peak_table)

    if len(fragment_peak_table) < min_peaks:
        return []

    fragment_peak_table = sort_fragment_peak_table_by_intensity(fragment_peak_table = fragment_peak_table,
                                                                descending = True)

    relative_fragment_intensity_percent = compute_relative_fragment_intensity_percent(fragment_peak_table = fragment_peak_table)

    formatted_fragment_peak_table = np.hstack((fragment_peak_table,
                                               relative_fragment_intensity_percent))

    return formatted_fragment_peak_table
    
    
import numpy as np
import os
import pandas as pd
#from ms2_spectrum import *


def format_fragment_peak_table_as_legacy_ms2_spectrum(fragment_peak_table,
                                                      mz_std = 5e-4):
    if len(fragment_peak_table) == 0:
        return []

    if len(fragment_peak_table.shape) != 2:
        return []

    if fragment_peak_table.shape[1] == 10:
        return fragment_peak_table

    if fragment_peak_table.shape[1] == 2:
        relative_intensity_percent = (fragment_peak_table[:, 1] / np.max(fragment_peak_table[:, 1]) * 100).reshape(-1, 1)

        fragment_peak_table = np.hstack((fragment_peak_table,
                                         relative_intensity_percent))

    if fragment_peak_table.shape[1] != 3:
        return []

    number_of_peaks = len(fragment_peak_table[:, 0])

    fragment_mz_da = fragment_peak_table[:, 0].reshape(-1, 1)
    fragment_intensity = fragment_peak_table[:, 1].reshape(-1, 1)
    relative_intensity_percent = fragment_peak_table[:, 2].reshape(-1, 1)

    mz_std_da = np.ones((number_of_peaks, 1)) * mz_std
    gauss_r2 = np.zeros((number_of_peaks, 1))
    number_of_signals = np.ones((number_of_peaks, 1))
    confidence_interval_da = np.zeros((number_of_peaks, 1))
    confidence_interval_ppm = np.zeros((number_of_peaks, 1))
    mz_min_da = fragment_mz_da.copy()
    mz_max_da = fragment_mz_da.copy()

    legacy_ms2_spectrum = np.hstack((fragment_mz_da,
                                     mz_std_da,
                                     fragment_intensity,
                                     gauss_r2,
                                     number_of_signals,
                                     confidence_interval_da,
                                     confidence_interval_ppm,
                                     mz_min_da,
                                     mz_max_da,
                                     relative_intensity_percent))

    return legacy_ms2_spectrum


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

        Spectrum = format_fragment_peak_table_as_legacy_ms2_spectrum(
            fragment_peak_table = Spectrum
        )

        SpectraList.append(Spectrum)

        if save and len(Spectrum) > 0:
            SpectrumDF = pd.DataFrame(Spectrum,
                                      columns = Columns)

            FileName = SpectraFoler + '/' + str(spectrum_id) + '.csv'
            SpectrumDF.to_csv(FileName)

    return SpectraList
    
    
import os
import pandas as pd
from ChargeDataSet_in_AnotherFolder import *
from AllMS2Data import *



def BatchExtract_All_MS2_Spectra(DataFolder,
                                 saveFolder = 'ms2_spectra',
                                 min_RT = 0,
                                 max_RT = 1500,
                                 min_mz = 0,
                                 max_mz = 1200,
                                 minPeaks = 1,
                                 SFindicator = '-ms2Summary.csv'):
    if not os.path.exists(saveFolder):
        os.mkdir(saveFolder)

    dataset_list = [x for x in os.listdir(DataFolder) if not x.startswith('.')]

    Total = len(dataset_list)
    c = 0

    for datasetname in dataset_list:
        try:
            DataSet = ChargeDataSet_in_AnotherFolder(DataSetName = datasetname,
                                                     DataFolder = DataFolder)

            SummMS2 = AllMS2Data(DataSet = DataSet,
                                 min_RT = min_RT,
                                 max_RT = max_RT,
                                 min_mz = min_mz,
                                 max_mz = max_mz)

            if SummMS2 is None or len(SummMS2) == 0:
                print('No MS2:', datasetname)
                c += 1
                continue

            DataSetName = datasetname
            spectra_folder = saveFolder + '/' + DataSetName.replace('.', '')

            if not os.path.exists(spectra_folder):
                os.mkdir(spectra_folder)

            summ_ms2_df = pd.DataFrame(SummMS2,
                                       columns = ['mz(Da)',
                                                  'RT(s)',
                                                  'id',
                                                  'maxInt',
                                                  'maxInt_frac'])

            summ_file = saveFolder + '/' + DataSetName.replace('.', '') + SFindicator
            summ_ms2_df.to_csv(summ_file,
                               index = False)

            All_ms2_spectra(DataSet = DataSet,
                            SummMS2 = SummMS2,
                            DataSetName = datasetname,
                            minPeaks = minPeaks,
                            saveFolder = saveFolder,
                            save = True)

        except Exception as error:
            print('FAILED:', datasetname, error)

        print(c, int(c / max(Total, 1) * 100))
        c += 1