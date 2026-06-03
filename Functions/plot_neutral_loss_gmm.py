from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

def plot_neutral_loss_gmm(mz_vec,
                          GMM,
                          bins=5000,
                          plot_components=True):
    """
    Plot empirical neutral-loss density and fitted GMM density.
    """

    mz_vec = np.asarray(mz_vec, dtype=float)
    mz_vec = mz_vec[np.isfinite(mz_vec)]

    x_axis = np.linspace(
        np.min(mz_vec),
        np.max(mz_vec),
        5000
    ).reshape(-1, 1)

    log_density = GMM.score_samples(x_axis)
    mixture_density = np.exp(log_density)

    plt.hist(
        mz_vec,
        bins=bins,
        density=True,
        alpha=0.35
    )

    plt.plot(
        x_axis[:, 0],
        mixture_density,
        linewidth=2
    )

    if plot_components:

        means = GMM.means_.reshape(-1)

        if GMM.covariance_type == "full":
            variances = GMM.covariances_.reshape(-1)
        elif GMM.covariance_type == "diag":
            variances = GMM.covariances_.reshape(-1)
        elif GMM.covariance_type == "spherical":
            variances = GMM.covariances_.reshape(-1)
        elif GMM.covariance_type == "tied":
            variances = np.repeat(GMM.covariances_.reshape(-1)[0],
                                  GMM.n_components)

        stds = np.sqrt(variances)

        for weight, mz_mean, mz_std in zip(GMM.weights_, means, stds):

            component_density = (
                weight
                * (1 / (mz_std * np.sqrt(2 * np.pi)))
                * np.exp(-0.5 * ((x_axis[:, 0] - mz_mean) / mz_std) ** 2)
            )

            plt.plot(
                x_axis[:, 0],
                component_density,
                linewidth=0.8
            )

    plt.xlabel("neutral loss m/z")
    plt.ylabel("density")
    plt.show()
