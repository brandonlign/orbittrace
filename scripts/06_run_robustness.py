#!/usr/bin/env python3
"""Run rotation, noise, timing, reference-group, and feature-ablation robustness."""
from pathlib import Path
import sys, warnings
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from reconnectid.config import load_project_config
from reconnectid.dataset import synchronize_event
from reconnectid.features import INVARIANT_FEATURES, BASELINE_SCORES, construct_features
from reconnectid.modeling import (_baseline_direction, _nonlinear_pipeline, _sparse_pipeline,
                                  fitting_rows, grouped_holdout_fixed)
from reconnectid.evaluation import evaluate_predictions
from reconnectid.robustness import test_rotation_invariance,add_relative_noise,FEATURE_ABLATIONS

warnings.filterwarnings("ignore",message="`sklearn.utils.parallel.delayed` should be used with")
cfg=load_project_config(ROOT)
events=pd.read_csv(ROOT/"data/event_metadata/selected_events.csv",parse_dates=["timestamp"])
samples=pd.read_parquet(ROOT/"data/processed/samples.parquet")
usable=set(samples.event_id.unique()); synchronized={}; rotation_rows=[]

# Each real usable event receives the configured 100 proper-rotation trials.
for _,event in events[events.event_id.isin(usable)].iterrows():
    _,x,valid,_=synchronize_event(event,cfg,ROOT); synchronized[event.event_id]=(x,valid)
    result=test_rotation_invariance(x["B"][valid],x["E"][valid],x["ve"][valid],x["vi"][valid],
                                    x["ne"][valid].squeeze(),x["Pe"][valid],INVARIANT_FEATURES,
                                    cfg.rotation_trials,cfg.random_seed)
    result.insert(0,"event_id",event.event_id); rotation_rows.append(result)
rotation=pd.concat(rotation_rows,ignore_index=True)
rotation.to_csv(ROOT/"results/tables/rotation_invariance.csv",index=False)
if rotation.maximum_relative_discrepancy.max()>=1e-8:
    raise RuntimeError("At least one claimed invariant feature exceeds rotation tolerance")
print(f"Rotation maximum discrepancy: {rotation.maximum_relative_discrepancy.max():.3e}",flush=True)

# Fit one clean training model per outer event. Sparse C is the clean nested-fold
# choice saved by stage 05; nonlinear l2=1 is fixed before any perturbation.
coef=pd.read_csv(ROOT/"results/tables/l1_coefficients.csv")
c_by_event=coef.groupby("held_out_event").C.first().to_dict()
outer_models={}
for held in samples.event_id.unique():
    train=samples[samples.event_id!=held]; use=fitting_rows(train); C=float(c_by_event.get(held,.3))
    sparse=_sparse_pipeline(C,cfg.random_seed); sparse.fit(train.loc[use,INVARIANT_FEATURES],train.loc[use,"target"],model__sample_weight=train.loc[use,"sample_weight"])
    nonlinear=_nonlinear_pipeline(cfg.random_seed,1.0); nonlinear.fit(train.loc[use,INVARIANT_FEATURES],train.loc[use,"target"],model__sample_weight=train.loc[use,"sample_weight"])
    directions={f:_baseline_direction(train,f) for f in BASELINE_SCORES}
    outer_models[held]=(sparse,nonlinear,directions)

# Frozen-clean-model input-noise evaluation is deliberately conservative: noise
# affects the held-out instrument quantities, never fitting or hyperparameter choice.
checkpoint=ROOT/"results/tables/noise_robustness_checkpoint.parquet"
noise_rows=pd.read_parquet(checkpoint).to_dict("records") if checkpoint.exists() else []
done={(r["noise_fraction"],int(r["trial"])) for r in noise_rows}
for level in (.005,.01,.02,.05):
  for trial in range(cfg.noise_trials):
    if (level,trial) in done: continue
    rng=np.random.default_rng(cfg.random_seed+int(level*1e6)+trial); predictions=[]
    for held,(x,_) in synchronized.items():
      B=add_relative_noise(x["B"],level,rng); E=add_relative_noise(x["E"],level,rng)
      ve=add_relative_noise(x["ve"],level,rng); vi=add_relative_noise(x["vi"],level,rng)
      ne=np.maximum(add_relative_noise(x["ne"],level,rng),np.finfo(float).tiny)
      Pe=add_relative_noise(x["Pe"],level,rng,True)
      feat=construct_features(B,E,ve,vi,ne.squeeze(),Pe,cfg.epsilon)
      test=samples[samples.event_id==held]; valid=test.valid.astype(bool).to_numpy()
      common=test.loc[valid,["event_id","delta_t","target","ambiguous","soft_target"]].reset_index(drop=True)
      sparse,nonlinear,directions=outer_models[held]
      for feature in BASELINE_SCORES:
        out=common.copy(); out["method"]=f"baseline:{feature}"; out["score"]=directions[feature]*feat.loc[valid,feature].to_numpy(); out["score_direction"]=directions[feature]; predictions.append(out)
      for method,model in (("sparse_invariant",sparse),("nonlinear_invariant",nonlinear)):
        out=common.copy(); out["method"]=method; out["score"]=model.predict_proba(feat.loc[valid,INVARIANT_FEATURES])[:,1]; out["score_direction"]=1; predictions.append(out)
    metrics=evaluate_predictions(pd.concat(predictions,ignore_index=True))
    means=metrics.groupby("method").auprc.mean(); best_baseline=means[[m.startswith("baseline:") for m in means.index]].max()
    survives=bool(means.get("sparse_invariant",-np.inf)>best_baseline and means.get("nonlinear_invariant",-np.inf)>best_baseline)
    noise_rows.extend({"noise_fraction":level,"trial":trial,"method":method,"auprc":value,"improvement_survives":survives} for method,value in means.items())
    pd.DataFrame(noise_rows).to_parquet(checkpoint,index=False)
noise=pd.DataFrame(noise_rows); noise.to_csv(ROOT/"results/tables/noise_robustness.csv",index=False)
print("Noise trials complete",flush=True)

# Timestamp uncertainty changes targets only; scores stay strictly out-of-event.
pred=pd.read_parquet(ROOT/"results/tables/predictions.parquet"); timing=[]
for shift in (-.12,-.06,-.03,.03,.06,.12):
  p=pred.copy(); d=p.delta_t-shift
  p["target"]=(d.abs()<=cfg.positive_half_width_seconds).astype(int)
  p["ambiguous"]=(d.abs()>cfg.positive_half_width_seconds)&(d.abs()<=cfg.ambiguous_half_width_seconds)
  m=evaluate_predictions(p); m["center_shift_seconds"]=shift; timing.append(m)
pd.concat(timing,ignore_index=True).to_csv(ROOT/"results/tables/timestamp_uncertainty.csv",index=False)

# Fixed-hyperparameter ablation avoids selecting an ablation after seeing its held-out event.
sets={**FEATURE_ABLATIONS,"all_invariant":INVARIANT_FEATURES,
      "all_except_Q":[x for x in INVARIANT_FEATURES if x!="Q"],
      "all_except_D_e":[x for x in INVARIANT_FEATURES if not x.startswith("D_e")]}
ablations=[]
for name,features in sets.items():
  p=grouped_holdout_fixed(samples,features=features,seed=cfg.random_seed,C=float(np.median(list(c_by_event.values()))))
  m=evaluate_predictions(p); m["ablation"]=name; ablations.append(m)
pd.concat(ablations,ignore_index=True).to_csv(ROOT/"results/tables/feature_ablations.csv",index=False)

# Leave all events from one reference source out together where n>=2.
meta=events[["event_id","reference_paper"]]; reference_samples=samples.merge(meta,on="event_id",how="left")
counts=meta.reference_paper.value_counts(); eligible=set(counts[counts>=2].index)
if len(eligible)>=1:
  p=grouped_holdout_fixed(reference_samples,group_column="reference_paper",holdout_groups=sorted(eligible),seed=cfg.random_seed,C=float(np.median(list(c_by_event.values()))))
  evaluate_predictions(p).to_csv(ROOT/"results/tables/leave_reference_group_out.csv",index=False)
else:
  pd.DataFrame(columns=["event_id","method","auprc"]).to_csv(ROOT/"results/tables/leave_reference_group_out.csv",index=False)
print("Robustness checks complete",flush=True)
