import numpy as np
from reconnectid.diagnostics import current_density, vector_diagnostics, ELEMENTARY_CHARGE
from reconnectid.synchronization import to_si, gap_aware_interpolate
from reconnectid.events import parse_event_list, select_events
from reconnectid.variable_resolver import PRODUCT_REQUESTS, resolve_variable


def test_si_conversions():
    np.testing.assert_allclose(to_si(np.array([1.0]), "B"), 1e-9)
    np.testing.assert_allclose(to_si(np.array([1.0]), "E"), 1e-3)
    np.testing.assert_allclose(to_si(np.array([1.0]), "velocity"), 1e3)
    np.testing.assert_allclose(to_si(np.array([1.0]), "density"), 1e6)
    np.testing.assert_allclose(to_si(np.array([1.0]), "pressure"), 1e-9)


def test_current_and_electron_frame_field_units():
    ne=np.array([1e6]); vi=np.array([[1e3,0,0]]); ve=np.zeros((1,3))
    J=current_density(ne,vi,ve)
    np.testing.assert_allclose(J[0,0],ELEMENTARY_CHARGE*1e9)
    out=vector_diagnostics(np.array([[0,0,1e-9]]),np.zeros((1,3)),ve,J)
    np.testing.assert_allclose(out["E_prime"],0)


def test_interpolation_does_not_cross_long_gap():
    t=np.array([0,.03,.30,.33]); y=np.column_stack((t,t))
    out=gap_aware_interpolate(t,y,np.array([.015,.15,.315]),max_gap=.15)
    assert out.valid.tolist()==[True,False,True]


def test_event_parser_annotations_and_deterministic_selection(tmp_path):
    catalog=tmp_path/"EDR_list_MMS.txt"
    catalog.write_text("""Date Time Spacecraft Reference paper
2015-09-08 11:01:20.370 MMS3 Eriksson_et_al._[2016]
2015-10-16 13:07:02.200 MMS2 Burch_et_al._[2016]
2015-12-14 01:17:39.650 MMS1 Chen_et_al._[2017]
2016-01-01 00:00:00.000 MMS4 Example_[2016]
""")
    events=parse_event_list(catalog)
    assert events.is_guide_field_study.sum()==2 and events.is_canonical.sum()==1
    a=select_events(events,3,2026); b=select_events(events,3,2026)
    assert a.event_id.tolist()==b.event_id.tolist()
    assert set(a.event_id)==set(events.loc[events.is_guide_field_study|events.is_canonical,"event_id"])


def test_variable_resolver_prefers_physical_vector_over_support_products():
    names=["mms3_fgm_b_gse_brst_l2","mms3_fgm_b_gse_brst_l2_btot","mms3_fgm_b_gse_brst_l2_bvec"]
    assert resolve_variable(names,PRODUCT_REQUESTS["B"]("mms3"))=="mms3_fgm_b_gse_brst_l2_bvec"
    density=["mms3_des_numberdensity_err_brst","mms3_des_numberdensity_brst"]
    assert resolve_variable(density,PRODUCT_REQUESTS["ne"]("mms3"))=="mms3_des_numberdensity_brst"
