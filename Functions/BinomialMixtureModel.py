from __future__ import annotations

import numpy as np
from scipy.special import gammaln, logsumexp

class BinomialMixtureModel:
    """
    Binomial mixture model for clustering LC-HRMS features by replicate-aware
    presence/absence profiles.

    counts:
        n_features × n_blocks matrix.

    trials:
        number of trials per block.
        For reactor-level Bernoulli mode, this is all 1.
        For day-count mode, this can be 3 for reactor blocks.

    group_idx:
        maps each block to a sample type, e.g.
        Effluent | Histidine, Effluent | Aniline, etc.

    Each cluster k has one p[k, sample_type].
    """

    def __init__(self, n_clusters, max_iter=500, tol=1e-6,
                 random_state=None, eps=1e-6):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tol = tol
        self.random_state = random_state
        self.eps = eps

    def _log_binomial_likelihood(self, counts, trials, group_idx):
        n_features, n_blocks = counts.shape

        log_prob = np.zeros((n_features, self.n_clusters), dtype=float)

        for k in range(self.n_clusters):
            p_block = self.p_[k, group_idx]
            p_block = np.clip(p_block, self.eps, 1 - self.eps)

            log_coef = (
                gammaln(trials[None, :] + 1)
                - gammaln(counts + 1)
                - gammaln(trials[None, :] - counts + 1)
            )

            log_prob[:, k] = (
                log_coef
                + counts * np.log(p_block[None, :])
                + (trials[None, :] - counts) * np.log(1 - p_block[None, :])
            ).sum(axis=1)

        return log_prob

    def fit(self, counts, trials, group_idx):
        counts = np.asarray(counts, dtype=float)
        trials = np.asarray(trials, dtype=float)
        group_idx = np.asarray(group_idx, dtype=int)

        n_features, n_blocks = counts.shape
        n_groups = int(group_idx.max()) + 1

        rng = np.random.default_rng(self.random_state)

        responsibilities = rng.random((n_features, self.n_clusters))
        responsibilities = responsibilities / responsibilities.sum(axis=1, keepdims=True)

        prev_loglik = -np.inf

        for iteration in range(self.max_iter):
            Nk = responsibilities.sum(axis=0) + self.eps

            self.pi_ = Nk / n_features

            group_counts = np.zeros((n_features, n_groups), dtype=float)
            group_trials = np.zeros(n_groups, dtype=float)

            for g in range(n_groups):
                idx = group_idx == g
                group_counts[:, g] = counts[:, idx].sum(axis=1)
                group_trials[g] = trials[idx].sum()

            numerator = responsibilities.T @ group_counts
            denominator = Nk[:, None] * group_trials[None, :]

            self.p_ = numerator / denominator
            self.p_ = np.clip(self.p_, self.eps, 1 - self.eps)

            log_prob = self._log_binomial_likelihood(
                counts=counts,
                trials=trials,
                group_idx=group_idx
            )

            log_prob = log_prob + np.log(self.pi_)[None, :]

            log_norm = logsumexp(log_prob, axis=1, keepdims=True)
            responsibilities = np.exp(log_prob - log_norm)

            loglik = log_norm.sum()

            if abs(loglik - prev_loglik) < self.tol:
                break

            prev_loglik = loglik

        self.responsibilities_ = responsibilities
        self.labels_ = responsibilities.argmax(axis=1)
        self.assignment_probability_ = responsibilities.max(axis=1)
        self.loglik_ = loglik
        self.n_iter_ = iteration + 1

        n_parameters = (
            self.n_clusters * n_groups
            + (self.n_clusters - 1)
        )

        # Conservative BIC: count independent blocks, not raw samples.
        n_observations = n_features * n_blocks

        self.bic_ = (
            -2 * self.loglik_
            + n_parameters * np.log(n_observations)
        )

        self.aic_ = (
            -2 * self.loglik_
            + 2 * n_parameters
        )

        return self
