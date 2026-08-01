# Recovered GhostStream source pipeline

This directory preserves exact snapshots of the executable GhostStream source trees from `remotion-worker` PR #56 and PR #57 at immutable commit SHAs. See `SOURCE_MANIFEST.json` for file-level SHA-256 provenance.

The snapshots intentionally retain their original filenames, including version suffixes and small `_fixed.py` execution wrappers. Those wrappers document the exact deterministic, compatibility, and validation fixes used during the recovered runs; they are provenance evidence, not temporary files.

Generated logs, downloaded archives, caches, build products, and exploratory files created outside these immutable source trees are not stored in the final repository. Reproduction repairs or future code changes must be made outside this snapshot rather than silently rewriting it.
