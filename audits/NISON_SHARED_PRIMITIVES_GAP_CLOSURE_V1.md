# Nison Shared Primitive Gap Closure V1

Status: CONTRACT DESIGN ONLY — NOT FROZEN

## Objective
Close the shared compatibility gaps for Nison 0039–0044 without creating duplicate engines, inventing thresholds, or allowing Nison to generate direction.

## Primitive A — Zone / Level Identity
Required contract:
- represent support/resistance as a zone, not an exact price;
- preserve source evidence for why the zone exists;
- expose tests/retests/rejections as evidence events;
- no implicit price-width tolerance unless already canonical elsewhere;
- no lookahead: a zone/event may only use information available at its evaluation timestamp.
Consumers: 0040, 0042, 0044 and part of 0043.

## Primitive B — Trendline Geometry
Required contract:
- source-defined swing points are the inputs;
- line identity, touches, and break events are explicit evidence;
- break is a warning/evidence event, not an automatic direction signal;
- confirmation remains a separate Nison evidence step;
- no invented swing lookback/tolerance.
Consumers: 0041.

## Primitive C — Breakout / Return / Retest Chain
Required contract:
- prior level identity;
- breakout event;
- return/re-entry event where source requires it;
- retest/confirmation event;
- all events timestamped and causally ordered;
- no invented penetration or 'quickly' threshold.
Consumers: 0043 and 0044.

## Primitive D — Confluence / Cluster Evidence
Required contract:
- collect independently supported evidence items in the same price/context area;
- preserve provenance and timestamps for every evidence item;
- do not convert count into a score automatically;
- do not invent a minimum evidence count;
- Nison output remains confirmation/evidence only.
Consumers: 0039 and 0040.

## Closure rule
A primitive is CLOSED only when an existing canonical implementation or source-locked operator contract is found and verified by deterministic tests. This document itself does not close any primitive.

## 2025 governance
2025 is OOS and must not be used for operator selection, tuning, calibration, optimization, or threshold creation.

## Current verdict
The four gaps are now expressed as shared contracts rather than six separate rule-specific implementations. No production evaluator or PASS status is granted by this document.
