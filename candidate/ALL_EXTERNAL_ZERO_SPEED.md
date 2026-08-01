# External-catalogue comparison

The year/night bootstrap did not resolve a geocentric-speed drift. To avoid carrying an unsupported slope into other catalogues, the external analyses were repeated with dVg/dλ⊙ set to zero. The radiant center, angular drift, dispersions, activity interval, and orbital rules were unchanged.

## CAMS and SonotaCo

The main external sample combines six CAMS meteors from 2011–2012 with four SonotaCo meteors from 2022, 2023, and 2025.

| Measure | Value |
|---|---:|
| Members | 10 |
| Years | 2011, 2012, 2022, 2023, 2025 |
| Activity p-value | 1.6218 × 10⁻⁴ |
| Shifted-window p-value | 0.02041 |
| Median orbital D | 0.04879 |
| 90th-percentile orbital D | 0.07708 |
| Orbit-null p-value | 5 × 10⁻⁵ |
| Medoid distance from the GMN orbit | 0.01723 |

CAMS and SonotaCo were examined separately first. CAMS narrowly missed the project’s activity cutoff, while SonotaCo had too few events to meet the minimum count. Their pooled result was calculated afterward, so it is supporting evidence rather than a planned independent discovery test.

## EDMOND extension

A shower-removed EDMOND subset adds six non-overlapping events in 2014, 2016, 2017, and 2022. With those included, the extended sample contains 16 events across eight years.

| Measure | Value |
|---|---:|
| Members | 16 |
| Activity p-value | 1.4639 × 10⁻⁶ |
| Shifted-window p-value | 0.02041 |
| Median orbital D | 0.04843 |
| 90th-percentile orbital D | 0.08701 |
| Orbit-null p-value | 5 × 10⁻⁵ |
| Exact UTC duplicate groups across sources | 0 |

EDMOND is a compilation of historical video-meteor data and may share upstream observations or reduction history with other catalogues. The absence of exact UTC duplicates prevents direct double-counting of the selected events, but the archive labels should not be treated as three completely independent instruments.

## Currently linked EDMOND files

The same zero-speed-drift definition was applied to every annual ZIP currently linked from the EDMOND page. Twenty-three files covering 2001–2023 passed ZIP, CRC, schema, and finite-field checks. The 2024 link returned 404.

The surviving links do not appear to be the complete advertised v6.01 release:

- linked rows for 2001–2023: 481,252;
- advertised rows for those years: 614,758;
- coverage: 78.283%;
- annual row-count matches: 0 of 23; and
- embedded versions: mainly 513 and 516 rather than 601.

The linked files selected exactly the same six EDMOND events and no additional ones. Their one-sided activity p-value was 3.379 × 10⁻⁴, the median D_SH was 0.03601, and the orbit-null p-value was 5.0 × 10⁻⁵. The shifted-window p-value was 0.06122, and the sample remained below the project’s minimum N = 8 rule.

The external evidence is therefore unchanged when the unsupported speed slope is removed. CAMS and SonotaCo provide the main cross-catalogue support; EDMOND adds useful but provenance-limited evidence.
