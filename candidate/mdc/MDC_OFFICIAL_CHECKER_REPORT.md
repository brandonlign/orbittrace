# Official IAU MDC consistency-checker report

Run date: 2026-08-01

## Verdict

**PASS — zero consistency errors on the exact committed mean record.**

The current official IAU Meteor Data Center checker archive was downloaded, ZIP/CRC-validated, and run in two independent executable forms:

1. the distributed static Linux binaries; and
2. fresh binaries compiled from the distributed `elements.f` and `radiants.f` source with GNU Fortran.

Both forms produced byte-identical scientific comparison files and empty orbital and geocentric error files.

## Official software provenance

- Official archive: `checking_program.zip`
- Archive size: **1,797,920 bytes**
- Archive SHA-256: `dbc5c87c405ced956721814980588c0af59306d3e5196403b9d78e21e7d108a2`
- ZIP CRC validation: **passed**
- Distributed programs: `elements.exes`, `radiants.exes`
- Distributed source: `elements.f`, `radiants.f`
- Fresh compiler: GNU Fortran 13.2
- Fresh-build flags: `-std=legacy -ffixed-line-length-none -fallow-argument-mismatch -O2`

## Exact tested record

The checker input was generated directly from the committed `GhostStream_April_mean_submission.json` without changing or independently retyping any scientific value:

```text
IAU=0 AdNo=0 LS=37.149520 RA=247.169746 Dec=-14.342743 Vg=37.617513 q=0.080114 e=0.943593 peri=333.636995 node=37.157321 i=24.370030 N=95
```

The zero IAU and solution numbers are deliberate placeholders because the MDC has not assigned identifiers.

This exact rerun supersedes the earlier report whose displayed orbit used slightly different last-decimal values (`peri=333.636907`, `node=37.157736`, `i=24.369371`). Those differences were an audit-trail inconsistency, not a failed checker result.

## Unmodified official tolerances

- q: **0.05 AU**
- e: **0.05**
- argument of perihelion: **5°**
- node: **5°**
- inclination: **2.5°**
- solar longitude: **5°**
- right ascension: **5°**
- declination: **2.5°**
- geocentric speed: **1.5 km/s**

## Radiant-to-orbit reconstruction

Observed committed mean orbit:

```text
q=0.08011  e=0.94359  peri=333.637°  node=37.157°  i=24.370°
```

Orbit reconstructed by the official `elements` program:

```text
q=0.09250  e=0.94100  peri=330.838°  node=38.881°  i=22.578°
```

The official orbital error file was empty in both the distributed-binary and fresh-source-build runs.

## Orbit-to-radiant reconstruction

Observed committed mean geocentric quantities:

```text
LS=37.157°  RA=247.170°  Dec=-14.343°  Vg=37.618 km/s
```

Geocentric quantities reconstructed by the official `radiants` program:

```text
LS=38.881°  RA=247.905°  Dec=-14.285°  Vg=36.810 km/s
```

The checker selected its Q-adjustment solution. The official geocentric error file was empty in both executable forms.

## Reproducibility result

- Distributed static binaries: **zero orbital errors, zero geocentric errors**
- Freshly compiled official source: **zero orbital errors, zero geocentric errors**
- Static/fresh orbital comparison output: **byte-identical**
- Static/fresh geocentric comparison output: **byte-identical**

## Preserved CI evidence

- Workflow run: `30678890262`
- Artifact: `8811492090`
- Artifact SHA-256: `e81ad1756b63fd47b39783c693bdba16e028c71af37fc6ba2c1a90e563b4fb89`

## Claim boundary

This validates internal compatibility of the committed arithmetic-mean radiant, speed, solar longitude, and orbital elements under the official MDC tolerances. It does **not** validate shower novelty, membership selection, statistical significance, external replication, publication, or official IAU recognition.
