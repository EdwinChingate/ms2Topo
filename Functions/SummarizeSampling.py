from __future__ import annotations
from AlignFragmentsEngine import *
from CosineOverlappingClustering import *
from FeaturesTableSamples2Check import *
from FormattingSummary import *
from ReOrganizeSamplingResults import *
from Retrieve_and_Join_ms2_for_feature import *
from SamplingSamplesSpectra import *
from ShowDF import *
from UpdateIntramoduleSimilarityAfterClustering import *
from UpdateUniqueModulesAfterClustering import *

def SummarizeSampling(feature_clusterList,
                      All_FeaturesTable,
                      SamplesNames,
                      min_spectra = 3,
                      Intensity_to_explain = 0.9,
                      cos_tol = 0.9,
                      percentile = 10,
                      slice_id = 0,
                      sample_id_col = 16,
                      ms2_spec_id_col = 15,
                      percentile_mz = 5,
                      percentile_Int = 10,
                      ms2Folder = 'ms2_spectra',
                      ToAdd = 'mzML',
                      Norm2One = False):

    All_consensus_ms2, ModulesList, IntramoduleSimilarityList, BigFeature_Module = ReOrganizeSamplingResults(feature_clusterList = feature_clusterList,
                                                                                                             min_spectra = min_spectra,
                                                                                                             percentile_mz = percentile_mz,
                                                                                                             percentile_Int = percentile_Int)
    print(len(feature_clusterList))
    feature_cluster_data = CosineOverlappingClustering(All_ms2 = np.array(All_consensus_ms2),
                                                       SamplesNames = SamplesNames,
                                                       All_FeaturesTable = All_FeaturesTable,
                                                       Feature_module = np.arange(len(ModulesList)),
                                                       Spectra_idVec = np.arange(len(ModulesList)),
                                                       Intensity_to_explain = 1,
                                                       min_spectra = min_spectra,
                                                       cos_tol = cos_tol,
                                                       percentile = percentile,
                                                       slice_id = slice_id)   
    Modules, Feature_Module, IntramoduleSimilarity, This_Module_FeaturesTable, AlignedFragmentsMat, AlignedFragments_mz_Mat = feature_cluster_data
    IntramoduleSimilarityModulesMat = UpdateIntramoduleSimilarityAfterClustering(Modules = Modules,
                                                                                 IntramoduleSimilarityList = IntramoduleSimilarityList)
    Modules = UpdateUniqueModulesAfterClustering(New_Modules = Modules,
                                                 Modules = ModulesList)
    All_ms2, Spectra_idVec = Retrieve_and_Join_ms2_for_feature(All_FeaturesTable = All_FeaturesTable,
                                                               Feature_module = BigFeature_Module,
                                                               SamplesNames = SamplesNames,
                                                               sample_id_col = sample_id_col,
                                                               ms2_spec_id_col = ms2_spec_id_col,
                                                               ms2Folder = ms2Folder,
                                                               ToAdd = ToAdd,
                                                               Norm2One = Norm2One)
    print('ha', len(Spectra_idVec), len(Feature_Module), len(set(BigFeature_Module)))
    #Feature_Module = np.arange(Feature_Module)[Spectra_idVec].tolist() #Comeback here

    AlignedFragmentsMat, AlignedFragments_mz_Mat, Explained_fractionInt, N_features = AlignFragmentsEngine(All_ms2 = All_ms2,
                                                                                                           Feature_module = BigFeature_Module,
                                                                                                           Intensity_to_explain = Intensity_to_explain,
                                                                                                           min_spectra = min_spectra)
    
    feature_cluster_data = FormattingSummary(All_FeaturesTable = All_FeaturesTable,
                                             Modules = Modules,
                                             IntramoduleSimilarityModulesMat = IntramoduleSimilarityModulesMat,
                                             Feature_Module = BigFeature_Module,
                                             Explained_fractionInt = Explained_fractionInt,
                                             slice_id = slice_id,
                                             AlignedFragmentsMat = AlignedFragmentsMat,
                                             AlignedFragments_mz_Mat = AlignedFragments_mz_Mat)
    
    
    
    Samples_FeaturesIdsList, Samples_ids2Check = FeaturesTableSamples2Check(Feature_Module = BigFeature_Module,
                                                                            All_FeaturesTable = All_FeaturesTable)
    print(Samples_ids2Check)
    if len(Samples_ids2Check) > 0:
        SamplesSamplesList = SamplingSamplesSpectra(Samples_FeaturesIdsList = Samples_FeaturesIdsList,
                                                    Samples_ids2Check = Samples_ids2Check,
                                                    Nspectra_sampling = 3)
        print(SamplesSamplesList)
        All_ms2, Spectra_idVec = Retrieve_and_Join_ms2_for_feature(All_FeaturesTable = All_FeaturesTable,
                                                               Feature_module = SamplesSamplesList,
                                                               SamplesNames = SamplesNames,
                                                               sample_id_col = sample_id_col,
                                                               ms2_spec_id_col = ms2_spec_id_col,
                                                               ms2Folder = ms2Folder,
                                                               ToAdd = ToAdd,
                                                               Norm2One = Norm2One)
        SamplesSamplesList = np.array(SamplesSamplesList)[Spectra_idVec].tolist()
        ShowDF(All_FeaturesTable[SamplesSamplesList,:])
        AlignedFragmentsMats, AlignedFragments_mz_Mats, Explained_fractionInts, N_featuress = AlignFragmentsEngine(All_ms2 = All_ms2,
                                                                                                               Feature_module = SamplesSamplesList,
                                                                                                               Intensity_to_explain = Intensity_to_explain,
                                                                                                               min_spectra = min_spectra)

        ShowDF(AlignedFragmentsMats)
        std_distance = 3
        ppm_tol = 20
        mz_FragmentsVec = AlignedFragmentsMat[:, 0]
        N_Fragments = len(mz_FragmentsVec)
        AlignedFragmentsSamplesSpectraMat = np.zeros((N_Fragments,
                                                      len(Spectra_idVec) + 1))
        AlignedFragmentsSamplesSpectraMat[:, 0] = AlignedFragmentsMat[:, 0]
        #Frag_Modules = [[]] * N_Fragments
        #SamplesSamplesList = SamplesSamplesList[Spectra_idVec]
        
        mzVec = All_ms2[:, 0]
        mz_stdVec = All_ms2[:, 1]
        mz_std_edgeVec = np.minimum(mz_stdVec * std_distance,
                                    ppm_tol / 1e6 * mzVec)  
        mzMaxVec = mzVec + mz_std_edgeVec
        mzMinVec = mzVec - mz_std_edgeVec
        for fragment_id in np.arange(N_Fragments):
            mz = mz_FragmentsVec[fragment_id]
            mzLoc = np.where((mzMinVec < mz) & (mzMaxVec > mz))[0]
            Fragments_in_line = np.array(All_ms2[mzLoc, 10],
                                         dtype = 'int')
            AlignedFragmentsSamplesSpectraMat[fragment_id, Fragments_in_line + 1] = All_ms2[mzLoc, 9]


        Modules, Feature_Module, IntramoduleSimilarity, This_Module_FeaturesTable, AlignedFragmentsMat, AlignedFragments_mz_Mat = feature_cluster_data

        CentroidsAlignedFragmentsMat = np.zeros((N_Fragments,
                                                 len(Modules) + 1))
        for module_id in np.arange(len(Modules)):       
            module = Modules[module_id]
            MeanVec = np.mean(AlignedFragmentsMat[:, 1:][:, module],
                              axis = 1)
            CentroidsAlignedFragmentsMat[:, module_id + 1] = MeanVec

        ShowDF(CentroidsAlignedFragmentsMat)
        ShowDF(AlignedFragmentsSamplesSpectraMat)
    return feature_cluster_data