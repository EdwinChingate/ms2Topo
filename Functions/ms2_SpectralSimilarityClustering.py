import pandas as pd
import numpy as np
from AdjacencyListFeatures import *
from ms2_feat_modules import *
from ms2_FeaturesDifferences import *
def ms2_SpectralSimilarityClustering(SummMS2_raw,
                                     SampleName='',
                                     SamplesNames=[],
                                     mz_col=1,
                                     RT_col=2,
                                     RT_tol=20,
                                     mz_Tol=1e-2,
                                     sample_id_col=-1,
                                     ms2_spec_id_col=0,
                                     ms2Folder='ms2_spectra',
                                     ToAdd='mzML',
                                     min_Int_Frac=2,
                                     cos_tol=0.9):
    if len(SamplesNames)==0:
        SamplesNames=[SampleName]
    AdjacencyList,feat_ids=AdjacencyListFeatures(MS2_features=SummMS2_raw,
                                                 mz_col=mz_col,
                                                 RT_col=RT_col,
                                                 RT_tol=RT_tol,
                                                 mz_Tol=mz_Tol)
    RawModules=ms2_feat_modules(AdjacencyList=AdjacencyList,
                                ms2_ids=feat_ids)
    Modules=[]
    for Feature_module in RawModules:
        Feature_Modules=ms2_FeaturesDifferences(All_FeaturesTable=SummMS2_raw,
                                                Feature_module=Feature_module,
                                                SamplesNames=SamplesNames,
                                                sample_id_col=sample_id_col,
                                                ms2_spec_id_col=ms2_spec_id_col,
                                                ms2Folder=ms2Folder,
                                                ToAdd=ToAdd,
                                                min_Int_Frac=min_Int_Frac,
                                                cos_tol=cos_tol)
        Modules+=Feature_Modules
    return Modules
