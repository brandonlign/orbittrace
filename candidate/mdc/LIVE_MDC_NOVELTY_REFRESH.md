# Live IAU Meteor Data Center novelty refresh

**Verdict:** `NO_CURRENT_IAU_MDC_HARD_DUPLICATE`

## Scope

The frozen GhostStream April candidate was compared against the current official IAU Meteor Data Center full shower-data JSON without changing the candidate, its drifts, or the duplicate-screen thresholds.

The refresh was run on **2026-08-01 UTC** against catalogue version **2026-06-25**.

## Catalogue provenance

- Official shower records declared and parsed: **1,072**
- Submitted shower solutions parsed: **2,174**
- Download size: **3,308,032 bytes**
- Download SHA-256: `821fa09734314e2796388c4f2fc94bb770998f2f2b08d6a84135660849aef899`
- Source/count/schema checks: **passed**

## Frozen duplicate screen

A hard duplicate required all of the following:

1. the published activity interval to overlap the candidate's frozen solar-longitude interval of **32.901963°–40.901963°**, or the mean epoch to lie within ±8° when bounds were absent;
2. drifted radiant separation no greater than **5°**;
3. drifted geocentric-speed difference no greater than **5 km s⁻¹**; and
4. a complete orbit with Southworth–Hawkins distance `D_SH ≤ 0.15`.

Orbit-incomplete radiant–speed–activity near matches were also reported separately rather than being silently treated as novel.

## Result

- Hard duplicate matches: **0**
- Activity-compatible radiant–speed near matches: **0**
- Orbit-incomplete near matches: **0**

The nearest complete orbit remains:

- IAU number/code: **149 NOP**
- Name: **Northern May Ophiuchids**
- Solution: **004**
- `D_SH`: **0.2344515**
- Published activity interval: **45°–75°** solar longitude
- Mean epoch: **58.6°**, or **21.698°** after the candidate epoch
- Drifted radiant separation: **9.5879°**
- Drifted speed difference: **1.0049 km s⁻¹**
- Activity-compatible with GhostStream: **no**

NOP therefore fails the activity, radiant, and orbital duplicate rules despite its relatively similar speed.

## Interpretation

The current official catalogue contains no shower solution that satisfies the frozen GhostStream duplicate criteria. The result preserves the existing claim boundary: GhostStream remains an **uncatalogued candidate**, not an official IAU discovery or established shower.

This refresh tests catalogue duplication only. It does not replace expert review of coordinate conventions, minor-shower literature, or the submitted 95-event membership table.

## Reproduce

```bash
python pilots/ghoststream/april_stream/mdc/refresh_live_mdc_novelty.py \
  --output-dir live_mdc_refresh
```

## Preserved CI evidence

- Workflow run: `30678572191`
- Artifact: `8811375826`
- Artifact SHA-256: `d7a88515dcc97762812dd4df6b431a2c65805928969ad114b3636809254ae393`
