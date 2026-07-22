#!/usr/bin/env python3
from pathlib import Path
import sys,pandas as pd
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from reconnectid.config import load_project_config
from reconnectid.modeling import leave_one_event_out
from reconnectid.evaluation import evaluate_predictions
cfg=load_project_config(ROOT); samples=pd.read_parquet(ROOT/"data/processed/samples.parquet")
result=leave_one_event_out(samples,seed=cfg.random_seed,include_sparse=False,include_nonlinear=False)
result.predictions.to_parquet(ROOT/"results/tables/baseline_predictions.parquet",index=False); evaluate_predictions(result.predictions).to_csv(ROOT/"results/tables/baseline_metrics.csv",index=False)
print("Saved strict leave-one-event-out individual baseline results")
