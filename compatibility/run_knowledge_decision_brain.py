from decision_brain import assess
from compatibility.knowledge_decision_handoff import build_handoff


def run(market_row, alignment_output, similarity=None):
    handoff = build_handoff(market_row, alignment_output, similarity)
    if handoff["routing"] != "ASSESS":
        return {
            "status": handoff["routing"],
            "assessment": None,
            "knowledge_evidence": handoff["knowledge_evidence"],
            "gates": handoff["gates"],
        }

    # Similarity is retained by the handoff as historical evidence/metadata,
    # but must never enter the directional assessment function.
    assessment = assess(handoff["decision_brain_row"], similarity=None)
    return {
        "status": "ASSESSED",
        "assessment": assessment,
        "knowledge_evidence": handoff["knowledge_evidence"],
        "gates": handoff["gates"],
    }
