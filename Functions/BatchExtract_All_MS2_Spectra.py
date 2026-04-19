from __future__ import annotations
from AllMS2Data import *
from ms2_spectrum import *
from ChargeDataSet_in_AnotherFolder import *
import os
import pandas as pd
from All_ms2_spectra import *

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
