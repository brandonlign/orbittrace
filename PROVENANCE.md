# Computation provenance

The clean repository is a release archive, not a copy of the development workspace. The original analysis history included exploratory scripts, temporary runner wrappers, and earlier candidate names, so those files were kept out of this public-facing package. The final code, derived tables, and machine-readable results are preserved here.

The main GMN validation was independently rerun from the recovered immutable analysis snapshot at commit `39972b5fe0cf4d47092d3caa2b3ced12bedb065e`. That run reproduced the 101-event 2019–2026 selection and the 95-event 2022–2026 canonical sample timestamp for timestamp. It also reproduced the earlier-year activity and orbital-null tests, the 20,000-replicate bootstrap, the radiant-drift result, the 35.902°–39.902° activity interval, the 30/22/44 geographic split, and the 81/81 validation-sensitivity result.

For that primary reproduction:

- recovered source script SHA-256: `4a29b4c3bde528be2523b627f7e8a22d3c836f45981cc77aefd7d4c694c844ac`
- regenerated 101-event CSV SHA-256: `e0e1ec7dca981cc656ac458ce5fce8c825a7f8914460e023808b966e7ca51e6b`
- committed 95-event lookup SHA-256: `0f021d95df56901ba119114d9b7c3816abbb3c86354638f23a69eed71b1aa6d3`

The final external-catalogue replication was run separately with the unchanged GMN-derived template. CAMS returned 9 matches, SonotaCo 11, and EDMOND 4; SonotaCo was the only independent network to pass every fixed replication gate. The preserved execution record for that run is tied to commit `6c42782e052be1f7efd7ce41ebf602ee5c4275a6` and artifact digest `sha256:62ede845b5d4e9ef17a2806a0b0bf16f6770e26a9fc743cc80ced5f15827bbd2`.

The current release check in `reproduce.py` does not claim to recreate those third-party downloads. It tests the public code path, verifies the archived scientific invariants, and regenerates the paper figures from the versioned derived tables. Source acquisition and preparation are documented in `data/README.md`.
