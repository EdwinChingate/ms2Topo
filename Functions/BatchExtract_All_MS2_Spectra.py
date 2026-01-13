from ChargeDataSet_in_AnotherFolder import *
from AllMS2Data import *
from All_ms2_spectra import *
def BatchExtract_All_MS2_Spectra(DataFolder,
                                 saveFolder='ms2_spectra',
                                 min_RT=0,
                                 max_RT=1500,
                                 min_mz=0,
                                 max_mz=1200,
                                 minInt=1e4,
                                 minPeaks=1,
                                 LogFileName='LogFile_ms2.csv',
                                 SFindicator='-ms2Summary.csv'):
    """
    Batch extract MS2 summary + per-spectrum MS2 tables for all datasets in DataFolder.

    Outputs:
    - <saveFolder>/<datasetname_no_dots>-ms2Summary.csv
    - <saveFolder>/<datasetname_no_dots>/<spectrum_index>.csv   (table for each spectrum)
    """



    if not os.path.exists(saveFolder):
        os.mkdir(saveFolder)

    dataset_list = [x for x in os.listdir(DataFolder) if not x.startswith('.')]
    Total = len(dataset_list)
    c = 0

    for datasetname in dataset_list:
        try:
            DataSet = ChargeDataSet_in_AnotherFolder(datasetname, DataFolder)

            SummMS2 = AllMS2Data(
                DataSet=DataSet,
                min_RT=min_RT, max_RT=max_RT,
                min_mz=min_mz, max_mz=max_mz
            )

            if SummMS2 is None or len(SummMS2) == 0:
                print('No MS2:', datasetname)
                c += 1
                continue

            SummMS2 = np.array(SummMS2)

            DataSetName = datasetname
            SpectraFolder = saveFolder + '/' + DataSetName.replace('.', '')

            if not os.path.exists(SpectraFolder):
                os.mkdir(SpectraFolder)

            # Save summary
            SummMS2DF = pd.DataFrame(
                SummMS2,
                columns=['mz(Da)', 'RT(s)', 'id', 'maxInt', 'maxInt_frac']
            )
            SummFile = saveFolder + '/' + DataSetName.replace('.', '') + SFindicator
            SummMS2DF.to_csv(SummFile, index=False)

            # Extract spectra tables
            SpectraList = All_ms2_spectra(
                DataSet=DataSet,
                SummMS2=SummMS2,
                DataSetName=datasetname,
                minInt=minInt,
                LogFileName=LogFileName,
                minPeaks=minPeaks,
                saveFolder=saveFolder,
                save=True
            )

        except:
            print('FAILED:', datasetname)

        print(c, int(c / max(Total, 1) * 100))
        c += 1

