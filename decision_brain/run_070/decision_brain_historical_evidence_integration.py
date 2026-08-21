# Run 070 — Decision Brain V1 historical evidence integration wrapper.
# The original decision_brain.py is not modified.
# Similarity remains retrieval/evidence only; no predicted_return is passed to V1.

from dataclasses import asdict
import pandas as pd

def integrate_historical_evidence(decision_brain_module, similarity_adapter, bridge_module,
                                  row, retrieved_cases, outcomes, contexts,
                                  query_as_of, top_k=20):
    q = pd.Timestamp(query_as_of)
    if q.tzinfo is None:
        q = q.tz_localize("UTC")
    else:
        q = q.tz_convert("UTC")

    # Similarity metadata is adapted without direction or predicted return.
    retrieved_cases = retrieved_cases.copy()
    sim_payload = {
        "retrieval_status": "OK" if len(retrieved_cases) else "NO_HISTORICAL_EVIDENCE",
        "query_as_of_timestamp": q.isoformat(),
        "candidate_count": int(len(retrieved_cases)),
        "top_k_returned": int(len(retrieved_cases)),
        "nearest_distance": float(retrieved_cases["distance"].min()) if len(retrieved_cases) else None,
        "distance_summary": {
            "min": float(retrieved_cases["distance"].min()) if len(retrieved_cases) else None,
            "max": float(retrieved_cases["distance"].max()) if len(retrieved_cases) else None,
            "mean": float(retrieved_cases["distance"].mean()) if len(retrieved_cases) else None,
        },
        "historical_evidence_ids_or_positions": (
            retrieved_cases.get("source_position", pd.Series(dtype=int)).astype(int).tolist()
        ),
        "evidence_time_range": {
            "earliest": retrieved_cases["timestamp"].min().isoformat() if len(retrieved_cases) else None,
            "latest": retrieved_cases["timestamp"].max().isoformat() if len(retrieved_cases) else None,
        },
        "warnings": []
    }
    similarity_evidence = similarity_adapter.adapt_similarity_evidence(sim_payload)

    outcome_evidence, eligible_cases = bridge_module.build_asof_evidence(
        retrieved_cases, outcomes, q, horizon="return_24h",
        top_k=top_k, calibration_lock_2025=True
    )

    ctx = contexts.copy()
    ctx["timestamp"] = pd.to_datetime(ctx["timestamp"], utc=True, errors="coerce")
    context_cases = eligible_cases[["pair", "timestamp"]].merge(
        ctx[["pair", "timestamp", "context_signature"]],
        on=["pair", "timestamp"], how="left"
    )
    coverage = float(context_cases["context_signature"].notna().mean()) if len(context_cases) else 0.0

    # Critical governance point: original V1 is called with similarity=None.
    # Historical evidence is attached as metadata and does not directly generate V1 bias.
    assessment = asdict(decision_brain_module.assess(row, similarity=None))
    assessment["historical_evidence"] = {
        "similarity": similarity_evidence,
        "outcomes": outcome_evidence,
        "context": {
            "status": "OK" if coverage > 0 else "NO_CONTEXT_EVIDENCE",
            "eligible_context_cases": int(len(context_cases)),
            "context_coverage": coverage,
            "sample_context_signatures": context_cases["context_signature"].dropna().head(3).tolist(),
        }
    }
    assessment["integration_governance"] = {
        "similarity_changed_direction": False,
        "similarity_predicted_return_used": False,
        "historical_evidence_is_final_decision": False,
        "legacy_decision_brain_modified": False,
    }
    return assessment, eligible_cases
