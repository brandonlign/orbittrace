import ast
from pathlib import Path
from reconnectid.features import INVARIANT_FEATURES


FORBIDDEN={"timestamp","sample_index","delta_t","event_id","spacecraft","reference_paper","target","soft_target","ambiguous"}


def test_model_features_contain_no_identity_time_or_target_leakage():
    assert not (FORBIDDEN & set(INVARIANT_FEATURES))


def test_preprocessing_fit_occurs_inside_outer_fold():
    source=(Path(__file__).parents[1]/"src/reconnectid/modeling.py").read_text()
    tree=ast.parse(source)
    function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="leave_one_event_out")
    text=ast.unparse(function)
    assert "samples.event_id != held" in text
    assert "model.fit(train.loc[train_use, features]" in text

