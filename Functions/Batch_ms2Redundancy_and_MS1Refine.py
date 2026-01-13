import os
import pandas as pd
from ChargeDataSet_in_AnotherFolder import *
from ms2_SpectralRedundancy import *
from feat_ms2_Gauss import *
from MS_L_IDs import *

def Batch_ms2Redundancy_and_MS1Refine(DataFolder,
                                      ResultsFolder,
                                      ms2FolderName='ms2_spectra',
                                      SFindicator='-ms2Summary.xlsx',
                                      ToReplace='mzML-ms2Summary.xlsx',
                              
                                      # SummMS2 filters (coarse)
                                      min_RT=0,
                                      max_RT=1500,
                                      min_mz=0,
                                      max_mz=1200,
                              
                                      # Redundancy clustering params
                                      mz_col=1,
                                      RT_col=2,
                                      RT_tol=20,
                                      mz_Tol=1e-2,
                                      sample_id_col=-1,
                                      ms2_spec_id_col=0,
                                      ToAdd='mzML',
                                      min_Int_Frac=2,
                                      cos_tol=0.9,
                              
                                      # MS1 refinement params (feat_ms2_Gauss)
                                      mz_std=2e-3,
                                      MS2_to_MS1_ratio=10,
                                      stdDistance=3,
                                      MaxCount=3,
                                      Points_for_regression=5,
                                      minSignals=7,
                              
                                      # Behavior
                                      overwrite=False,
                                      LogFileName='LogFile_ms2Refine.csv'):
    """
    Batch pipeline:
    - For each dataset in DataFolder:
        - Load DataSet
        - Read ms2 summary (from ms2FolderName)
        - Remove redundant MS2 spectra (cosine clustering)
        - Refine features with MS1 (feat_ms2_Gauss)
        - Save Excel to ResultsFolder

    Assumptions:
    - You already created ms2 summaries & ms2_spectra tables under ms2FolderName.
    """

    home = os.getcwd()
    ms2Folder = home + '/' + ms2FolderName

    # Folders
    if not os.path.exists(ResultsFolder):
        os.mkdir(ResultsFolder)

    # Log file
    if LogFileName is not None:
        if not os.path.exists(LogFileName):
            pd.DataFrame([], columns=[
                'dataset', 'status', 'n_raw_ms2', 'n_nr_ms2', 'outfile', 'error'
            ]).to_csv(LogFileName, index=False)

    dataset_list = [x for x in os.listdir(DataFolder) if not x.startswith('.')]
    Total = len(dataset_list)
    c = 0

    for datasetname in dataset_list:
        while True:
            try:
                print('---')
                print(datasetname)

                OutFile = ResultsFolder + '/' + datasetname + '.xlsx'
                if (not overwrite) and os.path.exists(OutFile):
                    print('SKIP (exists):', OutFile)
                    if LogFileName is not None:
                        try:
                            df = pd.read_csv(LogFileName)
                            df = pd.concat([df, pd.DataFrame([{
                                'dataset': datasetname,
                                'status': 'skipped_exists',
                                'n_raw_ms2': None,
                                'n_nr_ms2': None,
                                'outfile': OutFile,
                                'error': ''
                            }])], ignore_index=True)
                            df.to_csv(LogFileName, index=False)
                        except:
                            pass
                    break

                # Build summary filename (your convention)
                SummaryFile = datasetname.replace('.', '') + SFindicator

                # Load dataset
                DataSet = ChargeDataSet_in_AnotherFolder(
                    DataSetName=datasetname,
                    DataFolder=DataFolder
                )

                # MS1 ids
                MS1IDVec = MS_L_IDs(DataSet=DataSet, Level=1)

                # Optional: count raw MS2 in summary (if file exists)
                n_raw_ms2 = None
                try:
                    SummPath = ms2Folder + '/' + SummaryFile
                    if os.path.exists(SummPath):
                        n_raw_ms2 = len(pd.read_excel(SummPath))
                except:
                    pass

                # Remove redundancy (returns reduced SummMS2)
                SummMS2 = ms2_SpectralRedundancy(
                    SummaryFile=SummaryFile,
                    min_RT=min_RT, max_RT=max_RT,
                    min_mz=min_mz, max_mz=max_mz,
                    ms2FolderName=ms2FolderName,
                    ToReplace=ToReplace,
                    mz_col=mz_col,
                    RT_col=RT_col,
                    RT_tol=RT_tol,
                    mz_Tol=mz_Tol,
                    sample_id_col=sample_id_col,
                    ms2_spec_id_col=ms2_spec_id_col,
                    ToAdd=ToAdd,
                    min_Int_Frac=min_Int_Frac,
                    cos_tol=cos_tol
                )

                if SummMS2 is None or len(SummMS2) == 0:
                    print('No nonredundant MS2 produced:', datasetname)
                    if LogFileName is not None:
                        try:
                            df = pd.read_csv(LogFileName)
                            df = pd.concat([df, pd.DataFrame([{
                                'dataset': datasetname,
                                'status': 'no_ms2',
                                'n_raw_ms2': n_raw_ms2,
                                'n_nr_ms2': 0,
                                'outfile': OutFile,
                                'error': ''
                            }])], ignore_index=True)
                            df.to_csv(LogFileName, index=False)
                        except:
                            pass
                    break

                n_nr_ms2 = len(SummMS2)

                # MS1 refinement
                ms2_featuresDF = feat_ms2_Gauss(
                    DataSet=DataSet,
                    SummMS2=SummMS2,
                    MS1IDVec=MS1IDVec,
                    mz_std=mz_std,
                    MS2_to_MS1_ratio=MS2_to_MS1_ratio,
                    stdDistance=stdDistance,
                    MaxCount=MaxCount,
                    Points_for_regression=Points_for_regression,
                    minSignals=minSignals
                )
                # Save
                
                ms2_featuresDF.to_excel(OutFile)
                print('Saved:', OutFile)

                # Log
                if LogFileName is not None:
                    try:
                        df = pd.read_csv(LogFileName)
                        df = pd.concat([df, pd.DataFrame([{
                            'dataset': datasetname,
                            'status': 'ok',
                            'n_raw_ms2': n_raw_ms2,
                            'n_nr_ms2': n_nr_ms2,
                            'outfile': OutFile,
                            'error': ''
                        }])], ignore_index=True)
                        df.to_csv(LogFileName, index=False)
                    except:
                        pass

                break

            except Exception as error:
                print("An exception occurred:", error)
                print('error', datasetname)

                # Log error and move on
                if LogFileName is not None:
                    try:
                        df = pd.read_csv(LogFileName)
                        df = pd.concat([df, pd.DataFrame([{
                            'dataset': datasetname,
                            'status': 'failed',
                            'n_raw_ms2': None,
                            'n_nr_ms2': None,
                            'outfile': '',
                            'error': str(error)
                        }])], ignore_index=True)
                        df.to_csv(LogFileName, index=False)
                    except:
                        pass

                break

        print(c, int(c / max(Total, 1) * 100))
        c += 1

