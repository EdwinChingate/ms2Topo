from Retrieve_and_Join_ms2_for_feature import *
from AdjacencyList_ms2Fragments import *
from ms2_feat_modules import *
from AligniningFragments_in_Feature import *
#from minimalAlignedFragmentsMat import *
from CosineMatrix import *
from AdjacencyList_from_matrix import *
from CommunityBlocks import *
from OverlappingClustering import *
#from Update_ids_FeatureModules import *
def ms2_FeaturesDifferences(All_FeaturesTable,
                            Feature_module,
                            SamplesNames,
                            AlignedSamplesList,
                            sample_id_col = 16,
                            ms2_spec_id_col = 15,
                            ms2Folder = 'ms2_spectra',
                            ToAdd = 'mzML',
                            cos_tol = 0.9,
                            Intensity_to_explain = 0.9,
                            min_spectra = 3,
                            Norm2One = False,
                            percentile = 10,
                            percentile_mz = 5,
                            percentile_Int = 10,
                            feature_id = 0):
    All_ms2, Spectra_idVec = Retrieve_and_Join_ms2_for_feature(All_FeaturesTable = All_FeaturesTable,
                                                               Feature_module = Feature_module,
                                                               SamplesNames = SamplesNames,
                                                               sample_id_col = sample_id_col,
                                                               ms2_spec_id_col = ms2_spec_id_col,
                                                               ms2Folder = ms2Folder,
                                                               ToAdd = ToAdd,
                                                               Norm2One = Norm2One)
    if len(All_ms2) == 0:
        return []
    Feature_module = np.array(Feature_module)[Spectra_idVec].tolist()
    AdjacencyListFragments, feat_ids = AdjacencyList_ms2Fragments(All_ms2 = All_ms2)
    N_features = len(Feature_module)
    Frag_Modules = ms2_feat_modules(AdjacencyList = AdjacencyListFragments,
                                    ms2_ids = feat_ids)
    AlignedFragmentsMat, AlignedFragments_mz_Mat = AligniningFragments_in_Feature(Frag_Modules = Frag_Modules,
                                                                                  All_ms2 = All_ms2,
                                                                                  N_features = N_features)   
    AlignedFragmentsMat, AlignedFragments_mz_Mat, Explained_fractionInt = minimalAlignedFragmentsMat(AlignedFragmentsMat = AlignedFragmentsMat,
                                                                                                     AlignedFragments_mz_Mat = AlignedFragments_mz_Mat,
                                                                                                     Intensity_to_explain = Intensity_to_explain,
                                                                                                     min_spectra = min_spectra)
    CosineMat = CosineMatrix(AlignedFragmentsMat = AlignedFragmentsMat,
                             N_features = N_features)
    AdjacencyList_Features, features_ids = AdjacencyList_from_matrix(CosineMat = CosineMat,
                                                                     N_ms2_spectra = N_features,
                                                                     cos_tol = cos_tol)
    Feature_Modules = CommunityBlocks(AdjacencyList_Features = AdjacencyList_Features)
    Modules = OverlappingClustering(Feature_Modules = Feature_Modules,
                                    CosineMat = CosineMat.copy(),
                                    percentile = percentile)    
    This_Module_FeaturesTable = All_FeaturesTable[Feature_module, :].copy()
    This_Module_FeaturesTable = np.hstack((This_Module_FeaturesTable, Explained_fractionInt))
    Modules, feature_id, AlignedSamplesList = Update_ids_FeatureModules(Feature_module = Feature_module,
                                                    Feature_Modules = Modules,
                                                                        AlignedSamplesList = AlignedSamplesList,
                                                    All_FeaturesTable = This_Module_FeaturesTable,
                                                    sample_id_col = sample_id_col,
                                                    ms2_spec_id_col = ms2_spec_id_col,
                                                    AlignedFragmentsMat = AlignedFragmentsMat,
                                                    AlignedFragments_mz_Mat = AlignedFragments_mz_Mat,
                                                    percentile_mz = percentile_mz,
                                                    percentile_Int = percentile_Int,
                                                    feature_id = feature_id,
                                                    min_spectra = min_spectra,
                                                    SamplesNames = SamplesNames)
    return [Modules, feature_id, AlignedSamplesList]
