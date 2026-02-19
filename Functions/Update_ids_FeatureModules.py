import numpy as np
#from ClosingModule import *
def Update_ids_FeatureModules(Feature_module,
                              Feature_Modules,
                              AlignedFragmentsMat,
                              All_FeaturesTable,
                              AlignedSamplesList,
                              AlignedFragments_mz_Mat,
                              SamplesNames,
                              sample_id_col = 6,
                              ms2_spec_id_col = 0,
                              percentile_mz = 5,
                              percentile_Int = 10,
                              feature_id = 0,
                              min_spectra = 3):    
    Modules=[]
    for module in Feature_Modules:        
        Modules, feature_id, AlignedSamplesList = ClosingModule(module = module,
                                            Modules = Modules,
                                            min_spectra = min_spectra,
                                            All_FeaturesTable = All_FeaturesTable,
                                            sample_id_col = sample_id_col,
                                            ms2_spec_id_col = ms2_spec_id_col,
                                            Feature_module = Feature_module,
                                            AlignedSamplesList = AlignedSamplesList,
                                            AlignedFragmentsMat = AlignedFragmentsMat,
                                            AlignedFragments_mz_Mat = AlignedFragments_mz_Mat,
                                            percentile_mz = percentile_mz,
                                            percentile_Int = percentile_Int,
                                            feature_id = feature_id,
                                            SamplesNames = SamplesNames)            
    return [Modules, feature_id, AlignedSamplesList]
