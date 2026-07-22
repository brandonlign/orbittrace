#!/usr/bin/env python3
from pathlib import Path
import sys,pandas as pd,warnings
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from reconnectid.config import load_project_config
from reconnectid.modeling import leave_one_event_out
from reconnectid.evaluation import evaluate_predictions,event_center_permutation
cfg=load_project_config(ROOT); samples=pd.read_parquet(ROOT/"data/processed/samples.parquet")
warnings.filterwarnings("ignore",message="`sklearn.utils.parallel.delayed` should be used with")
result=leave_one_event_out(samples,seed=cfg.random_seed,include_baselines=False)
baseline=pd.read_parquet(ROOT/"results/tables/baseline_predictions.parquet"); predictions=pd.concat([baseline,result.predictions],ignore_index=True)
predictions.to_parquet(ROOT/"results/tables/predictions.parquet",index=False); result.coefficients.to_csv(ROOT/"results/tables/l1_coefficients.csv",index=False)
metrics=evaluate_predictions(predictions); metrics.to_csv(ROOT/"results/tables/event_metrics.csv",index=False)
event_center_permutation(predictions,cfg.permutation_iterations,cfg.random_seed,cfg.event_window_seconds).to_csv(ROOT/"results/tables/permutation_tests.csv",index=False)
print("Saved nested event-level sparse/nonlinear predictions, coefficients, metrics, and permutations")
