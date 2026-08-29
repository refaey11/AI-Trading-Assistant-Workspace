# Murphy Source Audit — 2026-08-29

## Source
User-uploaded archive: `قواعد مورفي  2(6).zip`

## Local inspection
The archive was unpacked recursively, including nested Murphy backup/freeze ZIPs.
Top-level extraction contained 53 non-metadata files; 17 nested ZIP archives were recursively opened, yielding 77 non-metadata files across the full inspection tree.

## Confirmed Murphy material
The archive contains source/evidence/freeze material covering at least these explicit rule IDs:
- 0003, 0004
- 0006, 0007, 0008
- 0021, 0022, 0023
- 0028, 0029
- 0030, 0031, 0032, 0033
- 0034, 0035, 0036, 0037, 0038, 0039, 0040, 0041, 0042, 0043, 0044, 0045
- 0047, 0048, 0049
- 0050, 0051

The strongest batch freeze record inspected states `MURPHY_0034_0045` is locally production-frozen as a rule-contract/evidence freeze, with explicit statuses for 0034–0045 and governance that future changes require a new version. It also records 0037/0038 as historical evidence/context, 0039 as governance/process gate, and 0040/0041 as source-backed dynamic replay.

## Integration decision
Do not rebuild Murphy. Treat this archive as source evidence. The integration task is to preserve each existing rule's semantics, normalize its evidence to the existing governed consumer contract, retain provenance/as-of, and aggregate the rule outputs at the Decision Boundary.

## Important status note
This archive contains substantially more than a simple 34-rule summary. The project must not infer completeness from file-name counts alone. The official governed runtime boundary remains the authoritative consumer contract; any rule is only consumed when its existing evidence/producer is valid and provenance-compatible.

## Next execution step
Use this source archive to build the canonical Murphy evidence envelope for the selected pre-2025 Gate 3C event, without inventing thresholds or changing rule semantics. Then join the canonical Murphy envelope with the existing Nison, PIT Memory, TIZ, Decision Brain, Risk, and Trade Plan path.

## No-change constraints
- No Murphy rule semantics changed.
- No 2025 tuning.
- No synthetic Murphy signals.
- Memory remains evidence-only.
- Nison remains confirmation/contradiction only.
- TIZ remains process-only.
- Risk remains the hard execution gate.
