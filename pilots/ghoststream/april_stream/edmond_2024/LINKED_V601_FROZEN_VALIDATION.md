# Linked EDMOND frozen evaluation — integrity correction

**Status:** `SUPERSEDED_BY_EDMOND_CURRENT_RELEASE_AUDIT`

The frozen statistical evaluation in this file's original version was numerically valid for the files that were downloaded, but its description of those files as the complete usable EDMOND v6.01 series was too strong.

The authoritative interpretation is now in `EDMOND_CURRENT_RELEASE_AUDIT.md`:

- 23 currently linked annual ZIPs for 2001–2023 are readable and pass ZIP/CRC/schema checks;
- the 2024 link returns HTTP 404;
- linked rows for 2001–2023 total 481,252 versus 614,758 advertised (78.283%);
- 0 of 23 annual row counts matches the page table;
- embedded `_Version` values are predominantly 513 and 516, not 601;
- the frozen selector recovers exactly the prior six Shober-EDMOND events and no additional events;
- activity p = 3.3785×10⁻⁴, shifted-window p = 0.06122, and orbit-null p = 4.99975×10⁻⁵; and
- the result remains supporting evidence, not a new independent sample, a standalone pass, or a complete v6.01 replication.

The original CI evidence remains preserved in workflow run `30677912275` and artifact `8811142249`; its statistics apply only to the currently linked files.
