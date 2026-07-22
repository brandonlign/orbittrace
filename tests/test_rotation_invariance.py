import numpy as np
from reconnectid.features import INVARIANT_FEATURES
from reconnectid.robustness import test_rotation_invariance as rotation_check


def test_all_claimed_features_are_rotation_invariant():
    rng=np.random.default_rng(2026); n=64
    B=rng.normal(size=(n,3))*1e-8; E=rng.normal(size=(n,3))*1e-3
    ve=rng.normal(size=(n,3))*1e5; vi=rng.normal(size=(n,3))*1e5; ne=rng.uniform(1e6,2e7,n)
    A=rng.normal(size=(n,3,3)); Pe=np.einsum("...ij,...kj->...ik",A,A)*1e-10+np.eye(3)*1e-12
    result=rotation_check(B,E,ve,vi,ne,Pe,INVARIANT_FEATURES,25,2026)
    assert result.maximum_relative_discrepancy.max() < 1e-8

