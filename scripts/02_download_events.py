#!/usr/bin/env python3
from pathlib import Path
import argparse,logging,sys
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from reconnectid.config import load_project_config,ensure_directories
from reconnectid.mms_download import download_events
parser=argparse.ArgumentParser(); parser.add_argument("--smoke",action="store_true",help="Only the two anchors and canonical event"); parser.add_argument("--force",action="store_true"); args=parser.parse_args()
ensure_directories(ROOT); logging.basicConfig(filename=ROOT/"results/logs/download.log",level=logging.INFO,format="%(asctime)s %(levelname)s %(name)s %(message)s")
cfg=load_project_config(ROOT); events=pd.read_csv(ROOT/"data/event_metadata/selected_events.csv",parse_dates=["timestamp"])
if args.smoke: events=events[events.is_guide_field_study.astype(bool)|events.is_canonical.astype(bool)]
manifest=download_events(events,cfg,ROOT,args.force); print(manifest[["event_id","spacecraft","success","failure_reason"]].to_string(index=False));
if args.smoke and not manifest.success.all(): raise SystemExit("Smoke test failed; see explicit manifest and results/logs/download.log")
