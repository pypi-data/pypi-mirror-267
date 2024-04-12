from unittest import TestCase

from numpy import linalg, random, zeros_like
from numpy.testing import assert_array_almost_equal
from pandas import DataFrame, read_csv

from bearclaw.feature_extraction import (
    _COSMIC_MUTATIONAL_SIGNATURES,
    CosmicNMF,
)


class TestIdentityTransform(TestCase):
    """Verify that the transformation is invertible.

    Given W, the identity W = (W H) H^{-1} should hold.
    """

    def setUp(self):
        # Fix seed for reproducibility.
        random.seed(1234)

    def test_single_base_substitution(self):
        """Test identity transformation for single base substitutions."""
        signature_file = _COSMIC_MUTATIONAL_SIGNATURES["3.4"][
            "single_base_substitutions"
        ]
        weights = read_csv(signature_file, sep="\t", index_col=0).T

        # Test very specific activation functions.
        H_true = DataFrame(0, index=range(2), columns=weights.index)
        H_true.loc[0, "SBS3"] = 2600
        H_true.loc[1, "SBS3"] = 3757
        H_true.loc[0, "SBS5"] = 1240
        H_true.loc[1, "SBS5"] = 277
        H_true.loc[0, "SBS40a"] = 2952
        H_true.loc[1, "SBS40a"] = 1245

        # Construct mutational spectrum from random W.
        X = H_true @ weights

        decomposer = CosmicNMF(cosmic_signature="single_base_substitutions")
        H_reconstr = decomposer.transform(X)

        # They should be (nearly) identical.
        error = abs(H_reconstr - H_true)
        relative_error = linalg.norm(error) / linalg.norm(H_true)
        assert_array_almost_equal(relative_error, zeros_like(relative_error), decimal=2)

    def test_random_single_base_substitution(self):
        """Test identity transformation for single base substitutions."""
        signature_file = _COSMIC_MUTATIONAL_SIGNATURES["3.4"][
            "single_base_substitutions"
        ]
        H = read_csv(signature_file, sep="\t", index_col=0).T

        m_samples = 3
        n_components = H.shape[0]
        # We require >50 observations per sample.
        activations = random.randint(0, 2, size=(m_samples, n_components)) * 5
        W_true = DataFrame(activations, columns=H.index)

        # Construct mutational spectrum from random W.
        X = W_true @ H

        decomposer = CosmicNMF(cosmic_signature="single_base_substitutions")
        W_reconstr = decomposer.transform(X)

        # They should be (nearly) identical.
        error = abs(W_reconstr - W_true)
        relative_error = linalg.norm(error) / linalg.norm(W_true)
        assert_array_almost_equal(relative_error, zeros_like(relative_error), decimal=1)

    def test_doublet_base_substitution(self):
        """Test identity transformation for doublet base substitutions."""
        signature_file = _COSMIC_MUTATIONAL_SIGNATURES["3.4"][
            "doublet_base_substitutions"
        ]
        H = read_csv(signature_file, sep="\t", index_col=0).T

        m_samples = 3
        n_components = H.shape[0]
        # We require >50 observations per sample.
        activations = random.randint(0, 2, size=(m_samples, n_components)) * 5
        W_true = DataFrame(activations, columns=H.index)

        # Construct mutational spectrum from random W.
        X = W_true @ H

        decomposer = CosmicNMF(cosmic_signature="doublet_base_substitutions")
        W_reconstr = decomposer.transform(X)

        # They should be (nearly) identical.
        error = abs(W_reconstr - W_true)
        relative_error = linalg.norm(error) / linalg.norm(W_true)
        assert_array_almost_equal(relative_error, zeros_like(relative_error), decimal=3)

    def test_indel(self):
        """Test identity transformation for indels."""
        signature_file = _COSMIC_MUTATIONAL_SIGNATURES["3.4"]["indel"]
        H = read_csv(signature_file, sep="\t", index_col=0).T

        m_samples = 3
        n_components = H.shape[0]
        # We require >50 observations per sample.
        activations = random.randint(0, 2, size=(m_samples, n_components)) * 5
        W_true = DataFrame(activations, columns=H.index)

        # Construct mutational spectrum from random W.
        X = W_true @ H

        decomposer = CosmicNMF(cosmic_signature="indel")
        W_reconstr = decomposer.transform(X)

        # They should be (nearly) identical.
        error = abs(W_reconstr - W_true)
        relative_error = linalg.norm(error) / linalg.norm(W_true)
        assert_array_almost_equal(relative_error, zeros_like(relative_error), decimal=3)
