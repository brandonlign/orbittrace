#!/usr/bin/env python3
from pathlib import Path
import sys,pandas as pd
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from reconnectid.config import load_project_config
from reconnectid.evaluation import assign_guide_groups,event_bootstrap_difference
from reconnectid.plotting import generate_figures
from reconnectid.report import generate_report
cfg=load_project_config(ROOT); events=pd.read_parquet(ROOT/"data/processed/events.parquet"); events=assign_guide_groups(events,cfg.low_guide_quantile,cfg.high_guide_quantile); events.to_parquet(ROOT/"data/processed/events.parquet",index=False)
def csv(name):
 p=ROOT/"results/tables"/name; return pd.read_csv(p) if p.exists() else pd.DataFrame()
metrics=csv("event_metrics.csv"); noise=csv("noise_robustness.csv"); rotation=csv("rotation_invariance.csv"); coeff=csv("l1_coefficients.csv")
merged=metrics.merge(events[["event_id","guide_group"]],on="event_id",how="left") if not metrics.empty else metrics
comparisons=[]
high=merged[merged.guide_group=="higher"] if not merged.empty else merged
for model in ("sparse_invariant","nonlinear_invariant"):
 for baseline in [m for m in high.method.unique() if str(m).startswith("baseline:")]:
  for metric,higher in (("auprc",True),("localization_error_seconds",False),("within_0p30",True)):
   result=event_bootstrap_difference(high,model,baseline,metric,cfg.bootstrap_iterations,cfg.random_seed,higher)
   comparisons.append({"model":model,"baseline":baseline,"metric":metric,**result})
pd.DataFrame(comparisons).to_csv(ROOT/"results/tables/higher_guide_bootstrap_comparisons.csv",index=False)
pp=ROOT/"results/tables/predictions.parquet"; predictions=pd.read_parquet(pp) if pp.exists() else pd.DataFrame()
generate_figures(ROOT,events,metrics,predictions,coeff,rotation,noise); decision=generate_report(ROOT,cfg,events,metrics,noise,rotation); print(decision)
