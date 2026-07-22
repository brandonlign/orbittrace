#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from reconnectid.config import load_project_config,ensure_directories
from reconnectid.events import download_event_list,parse_event_list,select_events
cfg=load_project_config(ROOT); ensure_directories(ROOT)
path=download_event_list(cfg.zenodo_record,ROOT/"data/raw/EDR_list_MMS.txt")
catalog=parse_event_list(path); catalog.to_csv(ROOT/"data/event_metadata/all_events.csv",index=False)
selected=select_events(catalog,cfg.maximum_events,cfg.random_seed); selected.to_csv(ROOT/"data/event_metadata/selected_events.csv",index=False)
print(f"Parsed {len(catalog)} events; deterministically selected {len(selected)}; required events={int((selected.is_guide_field_study|selected.is_canonical).sum())}")
