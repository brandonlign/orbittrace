#!/usr/bin/env python3
"""Fail-closed reproduction of the frozen GhostStream GMN confirmation."""
from __future__ import annotations

import argparse, csv, hashlib, io, json, math, statistics, time
import urllib.error, urllib.parse, urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

API = "https://explore.globalmeteornetwork.org/gmn_data_store/-/query.csv"
LOOKUP = Path("pilots/ghoststream/april_stream/mdc/GhostStream_April_95_GMN_lookup.csv")
OUT = Path("pilots/ghoststream/reconstruction/primary_gmn_reproduction")
EPOCH, LON0, LAT0, VG0 = 36.901963, 210.6236753, 7.3230377, 37.641692
DLON, DLAT, DVG = -0.1029483, -0.0230546, -0.0293492
SLON, SLAT, SVG, SCORE_MAX, HALF = 0.7369, 0.6250, 1.1596, 9.0, 4.0
REF = {"q": .079202, "e": .946296, "i": 24.709376, "peri": 333.493819, "node": 37.937477}
EXP_N = {2019:1, 2020:4, 2021:1, 2022:10, 2023:8, 2024:14, 2025:34, 2026:29}
EXP_P = {2019:.3532, 2020:.1319, 2021:.3436, 2022:.003970, 2023:.002168,
         2024:4.888e-5, 2025:9.42e-9, 2026:4.131e-6}
EXP_POOL, EXP_MED, EXP_Q90 = 1.857134041807409e-5, .0439834, .0923211
FIELDS = ["unique_trajectory_identifier","beginning_utc_time","year","shower_iau_no",
          "num_stat","participating_stations","medianfiterr_arcsec","sol_lon_deg",
          "delta_sol_deg","rageo_deg","decgeo_deg","lamgeo_deg","betgeo_deg",
          "sun_lon_deg","vgeo_km_s","score","a_au","e","i_deg","peri_deg",
          "node_deg","q_au","tisserandj","latbeg_n_deg","lonbeg_e_deg",
          "latend_n_deg","lonend_e_deg"]


def sha(data: bytes) -> str: return hashlib.sha256(data).hexdigest()
def f(row: dict[str,str], key: str) -> float: return float(row[key])
def i(row: dict[str,str], key: str) -> int: return int(float(row[key]))
def w180(x: float) -> float: return (x + 180.0) % 360.0 - 180.0
def ad(a: float, b: float) -> float: return abs(w180(a-b))


def fetch(sql: str, purpose: str) -> tuple[list[dict[str,str]], dict[str,Any]]:
    url = API + "?" + urllib.parse.urlencode({"sql": sql, "_size": "max"})
    req = urllib.request.Request(url, headers={"User-Agent":"GhostStream-reproduction/1.0",
                                               "Accept":"text/csv,*/*;q=0.1",
                                               "Accept-Encoding":"identity"})
    err: Exception | None = None
    for attempt in range(1, 6):
        try:
            with urllib.request.urlopen(req, timeout=240) as response:
                payload = response.read(); status = getattr(response, "status", 200)
            rows = list(csv.DictReader(io.StringIO(payload.decode("utf-8-sig"))))
            return rows, {"purpose":purpose,"accessed_at_utc":datetime.now(timezone.utc).isoformat(),
                          "url":url,"sql":sql,"http_status":status,"bytes":len(payload),
                          "sha256":sha(payload),"rows":len(rows),"attempt":attempt}
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            err = exc
            if attempt < 5: time.sleep(min(2**(attempt-1), 16))
    raise RuntimeError(f"GMN query failed ({purpose}): {err}")


def ctes() -> str:
    return f"""
WITH station_counts AS (
 SELECT meteor_unique_trajectory_identifier AS id, count(*) AS num_stat,
        group_concat(station_code) AS participating_stations
 FROM participating_station GROUP BY meteor_unique_trajectory_identifier
), base AS (
 SELECT m.unique_trajectory_identifier,m.beginning_utc_time,
        cast(substr(m.beginning_utc_time,1,4) AS integer) AS year,m.shower_iau_no,
        sc.num_stat,sc.participating_stations,m.medianfiterr_arcsec,m.sol_lon_deg,
        m.rageo_deg,m.decgeo_deg,m.lamgeo_deg,m.betgeo_deg,m.vgeo_km_s,m.a_au,m.e,
        m.i_deg,m.peri_deg,m.node_deg,m.q_au,m.tisserandj,m.latbeg_n_deg,m.lonbeg_e_deg,
        m.latend_n_deg,m.lonend_e_deg
 FROM meteor m JOIN station_counts sc ON sc.id=m.unique_trajectory_identifier
 WHERE cast(substr(m.beginning_utc_time,1,4) AS integer) BETWEEN 2019 AND 2026
   AND m.shower_iau_no=-1 AND sc.num_stat>=2
   AND m.medianfiterr_arcsec IS NOT NULL AND m.sol_lon_deg IS NOT NULL
   AND m.rageo_deg IS NOT NULL AND m.decgeo_deg IS NOT NULL
   AND m.lamgeo_deg IS NOT NULL AND m.betgeo_deg IS NOT NULL
   AND m.vgeo_km_s IS NOT NULL AND m.a_au IS NOT NULL AND m.e IS NOT NULL
   AND m.i_deg IS NOT NULL AND m.peri_deg IS NOT NULL AND m.node_deg IS NOT NULL
   AND m.q_au IS NOT NULL AND m.vgeo_km_s BETWEEN 5.0 AND 75.0
), ranked AS (
 SELECT base.*,row_number() OVER (
   PARTITION BY substr(beginning_utc_time,1,19)
   ORDER BY medianfiterr_arcsec ASC,num_stat DESC,unique_trajectory_identifier ASC
 ) AS rn FROM base
), central AS (
 SELECT * FROM ranked WHERE rn=1 AND medianfiterr_arcsec<=180.0
), geometry AS (
 SELECT central.*,
  CASE WHEN sol_lon_deg-{EPOCH}>180 THEN sol_lon_deg-{EPOCH}-360
       WHEN sol_lon_deg-{EPOCH}<-180 THEN sol_lon_deg-{EPOCH}+360
       ELSE sol_lon_deg-{EPOCH} END AS delta_sol_deg,
  CASE WHEN lamgeo_deg-sol_lon_deg<0 THEN lamgeo_deg-sol_lon_deg+360
       WHEN lamgeo_deg-sol_lon_deg>=360 THEN lamgeo_deg-sol_lon_deg-360
       ELSE lamgeo_deg-sol_lon_deg END AS sun_lon_deg
 FROM central
), expected AS (
 SELECT geometry.*,{LON0}+({DLON})*delta_sol_deg AS ex_lon,
        {LAT0}+({DLAT})*delta_sol_deg AS ex_lat,{VG0}+({DVG})*delta_sol_deg AS ex_vg
 FROM geometry
), residuals AS (
 SELECT expected.*,
  CASE WHEN sun_lon_deg-ex_lon>180 THEN sun_lon_deg-ex_lon-360
       WHEN sun_lon_deg-ex_lon<-180 THEN sun_lon_deg-ex_lon+360
       ELSE sun_lon_deg-ex_lon END AS rlon,
  betgeo_deg-ex_lat AS rlat,vgeo_km_s-ex_vg AS rvg
 FROM expected
), scored AS (
 SELECT residuals.*,(rlon/{SLON})*(rlon/{SLON})+(rlat/{SLAT})*(rlat/{SLAT})
        +(rvg/{SVG})*(rvg/{SVG}) AS score
 FROM residuals
)
""".strip()


def membership_sql() -> str:
    return ctes()+"\nSELECT "+",".join(FIELDS)+f" FROM scored WHERE abs(delta_sol_deg)<={HALF} AND score<={SCORE_MAX} ORDER BY beginning_utc_time"


def activity_sql() -> str:
    return ctes()+f"""
SELECT year,
 sum(CASE WHEN abs(delta_sol_deg)<={HALF} AND score<={SCORE_MAX} THEN 1 ELSE 0 END) AS a,
 sum(CASE WHEN abs(delta_sol_deg)<={HALF} AND score>{SCORE_MAX} THEN 1 ELSE 0 END) AS b,
 sum(CASE WHEN abs(delta_sol_deg)>{HALF} AND score<={SCORE_MAX} THEN 1 ELSE 0 END) AS c,
 sum(CASE WHEN abs(delta_sol_deg)>{HALF} AND score>{SCORE_MAX} THEN 1 ELSE 0 END) AS d,
 count(*) AS broad_total
FROM scored WHERE sun_lon_deg BETWEEN 120 AND 240 AND abs(betgeo_deg)<=35
 AND vgeo_km_s BETWEEN 15 AND 50 GROUP BY year ORDER BY year
"""


def logc(n:int,k:int)->float:
    if k<0 or k>n:return -math.inf
    return math.lgamma(n+1)-math.lgamma(k+1)-math.lgamma(n-k+1)


def fisher(a:int,b:int,c:int,d:int)->float:
    ni,n,tc=a+b,a+b+c+d,a+c; hi=min(ni,tc)
    logs=[logc(tc,x)+logc(n-tc,ni-x)-logc(n,ni) for x in range(a,hi+1)]
    if not logs:return 1.0
    m=max(logs); return min(1.0,math.exp(m)*sum(math.exp(x-m) for x in logs))


def pct(vals:list[float],p:float)->float:
    v=sorted(vals)
    if len(v)==1:return v[0]
    x=(len(v)-1)*p; lo,hi=math.floor(x),math.ceil(x)
    return v[lo] if lo==hi else v[lo]*(hi-x)+v[hi]*(x-lo)


def norm_orbit(row:dict[str,str])->dict[str,float]:
    node,peri=f(row,"node_deg")%360,f(row,"peri_deg")%360; sol=f(row,"sol_lon_deg")
    if ad((node+180)%360,sol)<ad(node,sol):node,peri=(node+180)%360,(peri+180)%360
    return {"q":f(row,"q_au"),"e":f(row,"e"),"i":f(row,"i_deg"),"peri":peri,"node":node}


def dsh(x:dict[str,float],y:dict[str,float])->float:
    i1,w1,o1,i2,w2,o2=map(math.radians,[x["i"],x["peri"],x["node"],y["i"],y["peri"],y["node"]])
    ci=math.cos(i1)*math.cos(i2)+math.sin(i1)*math.sin(i2)*math.cos(o1-o2)
    I=math.acos(max(-1,min(1,ci))); den=max(1e-15,math.cos(I/2))
    z=math.cos((i1+i2)/2)*math.sin((o1-o2)/2)/den; z=max(-1,min(1,z))
    P=(w1-w2)+2*math.asin(z)
    return math.sqrt((x["e"]-y["e"])**2+(x["q"]-y["q"])**2+
                     (2*math.sin(I/2))**2+((x["e"]+y["e"])*math.sin(P/2))**2)


def write_csv(path:Path, rows:list[dict[str,Any]], fields:list[str])->None:
    with path.open("w",newline="",encoding="utf-8") as h:
        w=csv.DictWriter(h,fieldnames=fields,extrasaction="ignore");w.writeheader();w.writerows(rows)


def lookup_time(s:str)->str:return s[:10]+" "+s[11:]


def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument("--lookup",type=Path,default=LOOKUP)
    ap.add_argument("--output-dir",type=Path,default=OUT);args=ap.parse_args();args.output_dir.mkdir(parents=True,exist_ok=True)
    raw=args.lookup.read_bytes(); lookup=list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
    if len(lookup)!=95:raise RuntimeError(f"Expected 95 lookup rows, got {len(lookup)}")
    exp_times={lookup_time(r["Tobs"]) for r in lookup}
    members,ev1=fetch(membership_sql(),"frozen_template_membership")
    tables,ev2=fetch(activity_sql(),"expanded_antihelion_activity_tables")
    write_csv(args.output_dir/"reproduced_members_2019_2026.csv",members,FIELDS)
    write_csv(args.output_dir/"reproduced_activity_tables.csv",tables,["year","a","b","c","d","broad_total"])

    counts=Counter(i(r,"year") for r in members)
    cmp={str(y):{"expected":n,"actual":counts.get(y,0),"delta":counts.get(y,0)-n} for y,n in EXP_N.items()}
    selected=[r for r in members if i(r,"year")>=2022]; got_times={r["beginning_utc_time"][:19] for r in selected}
    missing,extra=sorted(exp_times-got_times),sorted(got_times-exp_times)
    lookup_exact=len(selected)==95 and not missing and not extra

    annual={}
    for r in tables:
        y=i(r,"year"); tab=[i(r,k) for k in ("a","b","c","d")]; p=fisher(*tab)
        annual[y]={"table":tab,"p":p,"expected_p":EXP_P.get(y),
                   "relative_error":None if y not in EXP_P else abs(p-EXP_P[y])/max(abs(EXP_P[y]),1e-300),
                   "passes_p_0_01":p<=.01}
    pool=[sum(annual[y]["table"][j] for y in (2022,2023)) for j in range(4)]
    pool_p=fisher(*pool); untouched=pool_p<=.05/12

    distances=[dsh(norm_orbit(r),REF) for r in selected]
    med=statistics.median(distances) if distances else math.nan; q90=pct(distances,.9) if distances else math.nan
    orbit_pass=bool(distances) and med<=.10 and q90<=.15
    count_exact=len(members)==101 and all(v["delta"]==0 for v in cmp.values())
    p_exact=abs(pool_p-EXP_POOL)/EXP_POOL<=1e-8
    if count_exact and lookup_exact and p_exact and orbit_pass: verdict="EXACT_REPRODUCTION"
    elif lookup_exact and untouched and orbit_pass: verdict="SCIENTIFIC_REPRODUCTION_WITH_SOURCE_DRIFT"
    elif members and untouched and orbit_pass: verdict="PARTIAL_REPRODUCTION"
    else: verdict="FAILED_REPRODUCTION"

    now=datetime.now(timezone.utc).isoformat()
    result={"generated_at_utc":now,"verdict":verdict,
      "scope":"Frozen-template membership, expanded-antihelion activity, and post-selection orbit only.",
      "protocol":"pilots/ghoststream/reconstruction/RECONSTRUCTION_PROTOCOL.md",
      "source":{"api":API,"queries":[ev1,ev2]},
      "lookup":{"path":str(args.lookup),"rows":95,"sha256":sha(raw)},
      "membership":{"expected_total":101,"actual_total":len(members),"annual":cmp,
        "annual_counts_exact":count_exact,"lookup_95_exact":lookup_exact,
        "actual_2022_2026":len(selected),"missing_timestamps":missing,"additional_timestamps":extra},
      "activity":{"annual":{str(k):v for k,v in annual.items()},"pooled_2022_2023":{"table":pool,
        "p":pool_p,"expected_p":EXP_POOL,"relative_error":abs(pool_p-EXP_POOL)/EXP_POOL,
        "passes_familywise_0_05_over_12":untouched}},
      "orbit":{"n":len(distances),"median_d_sh":med,"expected_median":EXP_MED,
        "q90_d_sh":q90,"expected_q90":EXP_Q90,"max_d_sh":max(distances) if distances else None,
        "passes_frozen_compactness_screen":orbit_pass},
      "gates":{"count_exact":count_exact,"lookup_exact":lookup_exact,"pooled_p_exact":p_exact,
        "untouched_activity":untouched,"orbit":orbit_pass}}
    (args.output_dir/"primary_gmn_reproduction.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")

    md=["# GhostStream primary GMN reproduction","",f"Generated: `{now}`","",f"## Verdict: `{verdict}`","",
        "This is the frozen-template confirmation stage, not yet the reconstructed blind discovery pipeline.","",
        "## Membership","",f"- Expected total: **101**",f"- Reproduced total: **{len(members)}**",
        f"- Annual counts exact: **{count_exact}**",f"- Preserved 95 timestamps exact: **{lookup_exact}**",
        f"- Missing preserved timestamps: **{len(missing)}**",f"- Additional live timestamps: **{len(extra)}**","",
        "|Year|Expected|Actual|Delta|Activity p|Preserved p|","|---:|---:|---:|---:|---:|---:|"]
    for y in range(2019,2027):
        x=cmp[str(y)]; a=annual.get(y,{"p":math.nan});md.append(f"|{y}|{x['expected']}|{x['actual']}|{x['delta']}|{a['p']:.12g}|{EXP_P[y]:.12g}|")
    md += ["","## Untouched 2022-2023",f"- Table `[a,b,c,d]`: `{pool}`",f"- Reproduced p: **{pool_p:.16g}**",
           f"- Preserved p: **{EXP_POOL:.16g}**",f"- Familywise gate passed: **{untouched}**","",
           "## Post-selection orbit",f"- Reproduced median D_SH: **{med:.9g}**",f"- Preserved median D_SH: **{EXP_MED:.9g}**",
           f"- Reproduced q90 D_SH: **{q90:.9g}**",f"- Preserved q90 D_SH: **{EXP_Q90:.9g}**","",
           "## Interpretation","",{
             "EXACT_REPRODUCTION":"The central frozen result regenerated within the declared exact tolerance.",
             "SCIENTIFIC_REPRODUCTION_WITH_SOURCE_DRIFT":"The preserved 95-event sample and decisive gates regenerated, but some live-source numerical comparison changed and must be audited.",
             "PARTIAL_REPRODUCTION":"The candidate remained significant and compact, but exact preserved membership did not regenerate; row discrepancies must be audited without retuning.",
             "FAILED_REPRODUCTION":"The decisive frozen gates did not regenerate. Thresholds must not be tuned; source and implementation discrepancies must be inspected."
           }[verdict],"","## Files","","- `primary_gmn_reproduction.json`","- `reproduced_members_2019_2026.csv`","- `reproduced_activity_tables.csv`",""]
    (args.output_dir/"PRIMARY_GMN_REPRODUCTION.md").write_text("\n".join(md))
    print(json.dumps({"verdict":verdict,"members":len(members),"lookup_exact":lookup_exact,"pooled_p":pool_p},indent=2))
    return 0 if verdict in {"EXACT_REPRODUCTION","SCIENTIFIC_REPRODUCTION_WITH_SOURCE_DRIFT"} else 3

if __name__=="__main__":raise SystemExit(main())
