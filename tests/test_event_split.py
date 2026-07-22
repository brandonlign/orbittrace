import numpy as np
import pandas as pd
import pytest
from reconnectid.modeling import assert_event_disjoint


def test_event_groups_never_overlap():
    frame=pd.DataFrame({"event_id":np.repeat(["A","B","C"],5)})
    for held in frame.event_id.unique():
        train=frame[frame.event_id!=held]; test=frame[frame.event_id==held]
        assert_event_disjoint(train,test)


def test_overlap_is_detected():
    with pytest.raises(AssertionError,match="Event leakage"):
        assert_event_disjoint(pd.DataFrame({"event_id":["A"]}),pd.DataFrame({"event_id":["A"]}))

