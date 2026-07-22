"""Sequential, checkpoint-aware full workflow entry point."""
from __future__ import annotations
import argparse, subprocess, sys, os
from pathlib import Path

def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument("--config",default="configs/pilot.yaml"); args=parser.parse_args()
    root=Path(__file__).resolve().parents[2]
    config=Path(args.config); config=config if config.is_absolute() else root/config
    if not config.exists(): raise SystemExit(f"Configuration does not exist: {config}")
    env=os.environ.copy(); env["RECONNECTID_CONFIG"]=str(config)
    for script in sorted((root/"scripts").glob("[0-9][0-9]_*.py")):
        print(f"\n=== {script.name} ===",flush=True)
        subprocess.run([sys.executable,str(script)],cwd=root,check=True,env=env)

if __name__=="__main__": main()
