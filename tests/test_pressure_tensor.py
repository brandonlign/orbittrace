import numpy as np
from reconnectid.diagnostics import pressure_diagnostics
from reconnectid.robustness import random_rotation,rotate_vectors,rotate_tensors


def test_swisdak_q_gyrotropic_zero_and_agyrotropic_positive():
    B=np.array([[0.,0.,1.]])
    gyro=np.diag([2.,2.,4.])[None]
    agyro=np.array([[[3.,1.,0.],[1.,1.,0.],[0.,0.,4.]]])
    assert abs(pressure_diagnostics(gyro,B).values["Q"][0]) < 1e-12
    assert pressure_diagnostics(agyro,B).values["Q"][0] > 0


def test_q_rotation_invariant_for_gyro_and_agyro():
    rng=np.random.default_rng(3); B=np.array([[.2,-.4,1.]])
    for P in (np.diag([2.,2.,4.])[None],np.array([[[3.,1.,0.],[1.,1.,0.],[0.,0.,4.]]])):
        q=pressure_diagnostics(P,B).values["Q"]
        for _ in range(20):
            R=random_rotation(rng); qr=pressure_diagnostics(rotate_tensors(P,R),rotate_vectors(B,R)).values["Q"]
            np.testing.assert_allclose(q,qr,rtol=1e-12,atol=1e-12)


def test_nearly_singular_is_finite_and_nonphysical_is_flagged():
    B=np.array([[0.,0.,1.]])
    near=pressure_diagnostics(np.diag([1e-15,1.,1.])[None],B)
    assert near.positive_semidefinite[0] and np.isfinite(near.values["Q"][0])
    bad=pressure_diagnostics(np.diag([-1.,2.,3.])[None],B)
    assert not bad.positive_semidefinite[0]
    assert np.isnan(bad.values["Q"][0])

