from __future__ import annotations

import numpy as np
import pandas as pd
from extract_mz_vec_by_neutral_loss_object import *
from search_neutral_loss_gmm_components import *

def search_gmm_by_neutral_loss_objects(mz_vec,
                                       NeutralLossObjectsDF,
                                       min_col="min_mz_(Da)",
                                       max_col="max_mz_(Da)",
                                       min_points=5,
                                       min_components=1,
                                       max_components=10,
                                       covariance_type="full",
                                       reg_covar=1e-12,
                                       max_iter=1000,
                                       random_state=7):

    rows = []
    ModelsDict = {}

    for _, NeutralLossObject in NeutralLossObjectsDF.iterrows():

        neutral_loss_id = NeutralLossObject["neutral_loss_id"]

        ObjectMzVec = extract_mz_vec_by_neutral_loss_object(
            mz_vec=mz_vec,
            NeutralLossObject=NeutralLossObject,
            min_col=min_col,
            max_col=max_col
        )

        if len(ObjectMzVec) < min_points:
            continue

        local_max_components = min(
            max_components,
            len(ObjectMzVec) - 1,
            len(np.unique(ObjectMzVec))
        )

        if local_max_components < min_components:
            continue

        BestGMM, GMMSearchDF, LocalModelsDict = search_neutral_loss_gmm_components(
            mz_vec=ObjectMzVec,
            min_components=min_components,
            max_components=local_max_components,
            covariance_type=covariance_type,
            reg_covar=reg_covar,
            max_iter=max_iter,
            random_state=random_state
        )

        for component_id in range(BestGMM.n_components):

            mz_mean = BestGMM.means_.reshape(-1)[component_id]

            if BestGMM.covariance_type == "full":
                mz_var = BestGMM.covariances_.reshape(-1)[component_id]
            elif BestGMM.covariance_type == "diag":
                mz_var = BestGMM.covariances_.reshape(-1)[component_id]
            elif BestGMM.covariance_type == "spherical":
                mz_var = BestGMM.covariances_.reshape(-1)[component_id]
            elif BestGMM.covariance_type == "tied":
                mz_var = BestGMM.covariances_.reshape(-1)[0]

            mz_std = np.sqrt(mz_var)

            rows.append({
                "parent_neutral_loss_id": neutral_loss_id,
                "local_component_id": component_id,
                "neutral_loss_mz_(Da)": mz_mean,
                "neutral_loss_mz_std_(Da)": mz_std,
                "neutral_loss_mz_std_(ppm)": mz_std / mz_mean * 1e6,
                "local_n_components": BestGMM.n_components,
                "raw_support_count": len(ObjectMzVec)
            })

        ModelsDict[neutral_loss_id] = {
            "BestGMM": BestGMM,
            "GMMSearchDF": GMMSearchDF,
            "ModelsDict": LocalModelsDict,
            "ObjectMzVec": ObjectMzVec
        }

    NeutralLossGMMObjectsDF = pd.DataFrame(rows)

    if len(NeutralLossGMMObjectsDF) > 0:
        NeutralLossGMMObjectsDF = NeutralLossGMMObjectsDF.sort_values(
            "neutral_loss_mz_(Da)"
        ).reset_index(drop=True)

    return NeutralLossGMMObjectsDF, ModelsDict
