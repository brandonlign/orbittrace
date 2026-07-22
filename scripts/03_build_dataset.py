#!/usr/bin/env python3
from pathlib import Path
import logging,sys,pandas as pd
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from reconnectid.config import load_project_config,ensure_directories
from reconnectid.dataset import build_dataset
cfg=load_project_config(ROOT); ensure_directories(ROOT); logging.basicConfig(filename=ROOT/"results/logs/dataset.log",level=logging.INFO)
events=pd.read_csv(ROOT/"data/event_metadata/selected_events.csv",parse_dates=["timestamp"]); data,meta=build_dataset(events,cfg,ROOT)
print(f"Built {len(data)} synchronized rows from {int(meta.success.fillna(False).sum())}/{len(meta)} events")
