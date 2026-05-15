from __future__ import annotations

# TODO: unresolved names: deepcopy

def deep_update(base, updates=None):
    """
    Recursively update a nested dictionary.

    This keeps configuration changes local: override only the values you want,
    while preserving the rest of the defaults.
    """
    if updates is None:
        return base

    for key, value in updates.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            deep_update(base[key], value)
        else:
            base[key] = value

    return base


def make_ms2topo_params(overrides=None):
    """
    Central parameter dictionary for the MS2 spectral-clustering workflow.

    The keys intentionally preserve your existing parameter names where possible,
    so the refactor changes plumbing/readability rather than algorithmic meaning.
    """
    params = {
        "io": {
            "ms2Folder": "ms2_spectra",
            "ToAdd": "mzML",
            "Norm2One": True,
        },
        "columns": {
            "mz_col": 1,
            "RT_col": 2,
            "sample_id_col": 6,
            "ms2_spec_id_col": 0,
        },
        "feature_grouping": {
            "RT_tol": 30,
            "mz_Tol": 2e-3,
        },
        "alignment": {
            "Intensity_to_explain": 0.9,
            "min_spectra_fraction": 0.3,
        },
        "clustering": {
            "max_Nspectra_cluster": 8,
            "Nspectra_sampling": 50,
            "SamplingTimes": 20,
            "std_times": 1,
            "min_nodes": 1,
            "assign_labels": "discretize",
            "random_state": 0,
        },
        "summary": {
            "percentile": 10,
            "percentile_mz": 5,
            "percentile_Int": 10,
            "percentile_RT": 5,
        },
        "closing": {
            "min_spectra": 3,
            "minSpectra": 3,
            "alpha": 0.01,
        },
    }

    return deep_update(params, deepcopy(overrides))


def make_ms2topo_context(**kwargs):
    """
    Small convenience helper for creating runtime dictionaries.
    """
    return dict(kwargs)