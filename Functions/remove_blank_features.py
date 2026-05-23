from __future__ import annotations

from get_feature_metadata_columns import *
from samples_n_features_filter import *

# TODO: unresolved names: column

def remove_blank_features(AlignedSamplesDF,
                          SamplesInfDF,
                          AlignedSamples_RT_DF = None,
                          FeaturesBlankAppear = 2,
                          FeaturesEffluentAppear = 2,
                          CarbonSource = None,
                          BlankSource = None,
                          AllBlanksAllSamples = True,
                          FeatureIDCol = "feat_id",
                          SourceCol = "Source",
                          CarbonSourceCol = "Primary carbon source",
                          TreatmentSource = "Effluent"):
    """
    Keep treatment-associated features while removing blank/control-associated ones.

    For each carbon source, a feature is kept when it appears in enough treatment
    samples and appears in fewer than FeaturesBlankAppear samples for each
    blank/control source. If AllBlanksAllSamples is True, the feature must also
    remain blank-clean across all carbon-source blank groups.

    The output feature table preserves all non-sample feature descriptors from
    the original table. The function also returns a dictionary containing the
    feature IDs retained for each treatment group.
    """

    if CarbonSource is None:
        CarbonSource = ["Aniline",
                        "Histidine",
                        "Succinate"]

    if BlankSource is None:
        BlankSource = ["EffluentClean",
                       "Influent",
                       "InfluentClean"]

    if FeatureIDCol not in AlignedSamplesDF.columns:
        raise ValueError(f"FeatureIDCol was not found in AlignedSamplesDF: {FeatureIDCol}")

    FeatureMetadataColumns = get_feature_metadata_columns(AlignedSamplesDF = AlignedSamplesDF,
                                                          SamplesInfDF = SamplesInfDF)

    FirstCS = True

    SelectedTreatmentColumns = []
    GroupFilters = {}

    for carbon_source in CarbonSource:
        EffluentFilter, EffluentSamples_index = samples_n_features_filter(AlignedSamplesDF = AlignedSamplesDF,
                                                                         SamplesInfDF = SamplesInfDF,
                                                                         AttributeList = [SourceCol,
                                                                                          CarbonSourceCol],
                                                                         attributeList = [TreatmentSource,
                                                                                          carbon_source],
                                                                         Min_Feat = FeaturesEffluentAppear)

        SelectedTreatmentColumns = SelectedTreatmentColumns + list(EffluentSamples_index)

        FirstBlank = True

        for blank_source in BlankSource:
            BlankSamplesLoc = samples_n_features_filter(AlignedSamplesDF = AlignedSamplesDF,
                                                        SamplesInfDF = SamplesInfDF,
                                                        AttributeList = [SourceCol,
                                                                         CarbonSourceCol],
                                                        attributeList = [blank_source,
                                                                         carbon_source],
                                                        Min_Feat = FeaturesBlankAppear,
                                                        MoreThan = False)[0]

            if FirstBlank:
                BlankFilter = BlankSamplesLoc
                FirstBlank = False
            else:
                BlankFilter = BlankFilter & BlankSamplesLoc

        CS_Filter = BlankFilter & EffluentFilter
        GroupFilters[carbon_source] = CS_Filter

        if FirstCS:
            Features_to_keep = CS_Filter.copy()
            Features_to_keepBlanks = BlankFilter.copy()
            FirstCS = False
        else:
            Features_to_keep = Features_to_keep | CS_Filter
            Features_to_keepBlanks = Features_to_keepBlanks & BlankFilter

    if AllBlanksAllSamples:
        Features_to_keep = Features_to_keep & Features_to_keepBlanks

    SelectedTreatmentColumns = list(dict.fromkeys(SelectedTreatmentColumns))

    OutputColumns = FeatureMetadataColumns + SelectedTreatmentColumns

    CarbonSourceFeatures = AlignedSamplesDF.loc[Features_to_keep,
                                                OutputColumns].copy()
    CarbonSourceFeatures = CarbonSourceFeatures.sort_values(by = 'median_mz(Da)',
                                                            ascending = True)

    FeatureIDSet_by_Group = {}

    for carbon_source in CarbonSource:
        GroupFinalFilter = GroupFilters[carbon_source] & Features_to_keep

        FeatureIDSet_by_Group[carbon_source] = set(AlignedSamplesDF.loc[GroupFinalFilter,
                                                                        FeatureIDCol].astype(str))

    if AlignedSamples_RT_DF is not None:
        RTFeatureMetadataColumns = [column for column in FeatureMetadataColumns
                                    if column in AlignedSamples_RT_DF.columns]

        RTSelectedTreatmentColumns = [column for column in SelectedTreatmentColumns
                                      if column in AlignedSamples_RT_DF.columns]

        RTOutputColumns = RTFeatureMetadataColumns + RTSelectedTreatmentColumns

        CarbonSourceFeatures_RT = AlignedSamples_RT_DF.loc[Features_to_keep,
                                                           RTOutputColumns].copy()

    else:
        CarbonSourceFeatures_RT = None

    return [CarbonSourceFeatures,
            CarbonSourceFeatures_RT,
            FeatureIDSet_by_Group]
