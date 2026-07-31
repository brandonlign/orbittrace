# Official IAU MDC consistency-checker report

Run date: 2026-07-31

## Software

The package was tested with the current consistency-checker archive linked by the IAU Meteor Data Center downloads page. The archive contains the Fortran programs `elements.f` and `radiants.f`, described by the MDC as checks of the internal consistency between a shower's mean geocentric quantities and mean orbital elements.

The programs were compiled with GNU Fortran using legacy fixed-form compatibility. The unmodified MDC tolerance files were used:

- q: 0.05 AU
- e: 0.05
- argument of perihelion: 5°
- node: 5°
- inclination: 2.5°
- solar longitude: 5°
- right ascension: 5°
- declination: 2.5°
- geocentric speed: 1.5 km/s

## Tested mean record

```text
IAU=0 AdNo=0 LS=37.149522 RA=247.169746 Dec=-14.342743 Vg=37.617513 q=0.080114 e=0.943593 peri=333.636907 node=37.157736 i=24.369371 N=95
```

The zero IAU and solution numbers are deliberate placeholders because the MDC has not assigned the provisional identifiers.

## Radiant-to-orbit reconstruction

Observed mean orbit:

```text
q=0.08011  e=0.94359  peri=333.637°  node=37.158°  i=24.369°
```

Orbit reconstructed by the official `elements.f` program from the mean solar longitude, radiant, and speed:

```text
q=0.09250  e=0.94100  peri=330.838°  node=38.881°  i=22.578°
```

The official error file was empty: **no orbital parameter exceeded the MDC tolerance**.

## Orbit-to-radiant reconstruction

Observed mean geocentric quantities:

```text
LS=37.158°  RA=247.170°  Dec=-14.343°  Vg=37.618 km/s
```

Geocentric quantities reconstructed by the official `radiants.f` program from the mean orbit:

```text
LS=38.881°  RA=247.905°  Dec=-14.285°  Vg=36.810 km/s
```

The checker selected its Q-adjustment solution. The official error file was empty: **no geocentric parameter exceeded the MDC tolerance**.

## Verdict

**PASS — zero consistency errors were reported by either official MDC program.**

This validates internal compatibility of the submitted mean radiant, speed, solar longitude, and orbital elements. It does not validate shower novelty, membership selection, statistical significance, or official recognition.
