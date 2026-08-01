# Corrected exposure-normalized activity profile

The first profile attempt loaded April catalogues only and therefore had zero exposure beyond solar longitude ~41°. Empty bins were incorrectly assigned a posterior rate. That result was rejected before it entered the manuscript.

The corrected analysis loaded March, April, and May catalogues for every year from 2022–2026. Bins with fewer than 40 simultaneous non-core antihelion meteors were treated as unavailable. Frozen stream-core counts were normalized by simultaneous non-core counts inside the same expanded antihelion source.

This is a relative source-normalized activity profile, not an absolute flux or ZHR estimate.

## Results

- Bin width: **0.50° solar longitude**
- Baseline rate: **1.604 stream-core meteors per 1000 antihelion-background meteors**
- Highest observed bin: **solar longitude 38.652°**
- Peak-bin counts: **15 stream / 1021 background**
- Peak relative rate: **15.17 per 1000 background**
- Peak-bin 95% interval: **8.56–23.72 per 1000 background**
- Statistically supported contiguous activity core: **solar longitude 35.902°–39.902°**
- Aggregate inside-versus-baseline odds ratio: **4.162**
- Aggregate p-value: **6.51×10⁻¹⁹**

The raw half-maximum width was only 0.5°, but it shifted between adjacent bins when individual years were omitted. It is therefore not interpreted as the physical stream width. The robust characterization is the contiguous four-degree interval whose posterior probability of exceeding the out-of-window baseline is at least 0.95.

## Year-level inside-versus-baseline tests

| Year | Stream inside | Background inside | Stream baseline | Background baseline | p |
|---:|---:|---:|---:|---:|---:|
| 2022 | 10 | 1086 | 6 | 2239 | 0.01395 |
| 2023 | 8 | 1525 | 3 | 4064 | 0.00224 |
| 2024 | 14 | 2181 | 15 | 10410 | 0.000126 |
| 2025 | 35 | 5277 | 15 | 9267 | 1.38×10⁻⁶ |
| 2026 | 29 | 4471 | 25 | 14366 | 2.07×10⁻⁶ |

The pooled profile remains highly significant when any one year is removed; leave-one-year-out aggregate p-values range from 2.17×10⁻¹³ to 2.30×10⁻¹⁷. The highest bin moves between solar-longitude offsets +0.25° and +1.75°, so the exact half-degree peak should not be treated as fixed annual timing.

## Interpretation boundary

The profile controls for changing catalogue exposure using the simultaneous expanded-antihelion population. It does not explicitly model weather, radiant elevation, limiting magnitude, station uptime, or effective collecting area. Therefore:

- the **four-degree relative activity core** is supported;
- an absolute flux, ZHR, or precisely measured physical FWHM is not yet supported.
