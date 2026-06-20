from __future__ import annotations

def compress_experiments_dist(bool_experiment_features_vec):
    return "".join(bool_experiment_features_vec.astype(str).tolist())
