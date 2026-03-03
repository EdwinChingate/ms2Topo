from __future__ import annotations
from ConsensusSpectra import *
import pandas as pd

def ReOrganizeSamplingResults(feature_clusterList,
                              min_spectra = 3,
                              percentile_mz = 5,
                              percentile_Int = 10):
    ModulesList = []
    FirstSpectra = True
    IntramoduleSimilarityList = []
    feature_id = 0
    BigFeature_Module = []
    for feature_cluster_data in feature_clusterList:
        Modules, Feature_Module, IntramoduleSimilarity, This_Module_FeaturesTable, AlignedFragmentsMat, AlignedFragments_mz_Mat = feature_cluster_data        
        for module_id in np.arange(len(Modules)):   
            module = Modules[module_id]            
            consensus_spectraDF = ConsensusSpectra(module = module,
                                                   min_spectra = min_spectra,
                                                   AlignedFragmentsMat = AlignedFragmentsMat,
                                                   AlignedFragments_mz_Mat = AlignedFragments_mz_Mat,
                                                   percentile_mz = percentile_mz,
                                                   percentile_Int = percentile_Int,
                                                   reduceIQR_factor = 6,
                                                   Columns_to_return = np.array([ 0, 2, 3, 9, 10, 11, 17, 18, 19, 20]))             
            if len(consensus_spectraDF) > 0:
                consensus_spectraDF['feature_id'] = feature_id
                if FirstSpectra:
                    All_consensus_ms2 = consensus_spectraDF
                    FirstSpectra = False
                else:
                    All_consensus_ms2 = pd.concat([All_consensus_ms2, consensus_spectraDF],
                                                  ignore_index = True)            
                ModulesList.append(np.array(Feature_Module)[module].tolist()) 
                IntramoduleSimilarityList.append(IntramoduleSimilarity[module_id, :])
                BigFeature_Module += np.array(Feature_Module)[module].tolist()
                feature_id += 1  
    BigFeature_Module = list(set(BigFeature_Module))
    return [All_consensus_ms2, ModulesList, IntramoduleSimilarityList, BigFeature_Module]