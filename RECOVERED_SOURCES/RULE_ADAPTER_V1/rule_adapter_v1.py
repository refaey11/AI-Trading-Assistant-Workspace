"""Compatibility adapter: normalizes existing subsystem outputs into one evidence bundle.
Does not create direction; Murphy is authoritative for direction."""
from typing import Any, Dict
DIRECTIONS = {"BULLISH", "BEARISH", "NONE", "NEUTRAL", None}
def _direction(v):
    if v is None: return None
    s = str(v).upper()
    return {"BUY":"BULLISH", "BUY_CANDIDATE":"BULLISH", "SELL":"BEARISH", "SELL_CANDIDATE":"BEARISH", "NO_TRADE":"NONE"}.get(s, s if s in DIRECTIONS else None)
def build_bundle(event: Dict[str, Any]) -> Dict[str, Any]:
    murphy=event.get("murphy") or {}; nison=event.get("nison") or {}; mtf=event.get("mtf") or {}; memories=event.get("historical_evidence") or {}
    direction=_direction(murphy.get("direction")); nison_dir=_direction(nison.get("direction") or nison.get("signal"))
    decision_hint="no_trade" if direction is None or (nison_dir and nison_dir != direction) else direction.lower()
    return {"schema_version":"canonical_evidence_bundle_v1","event_id":event.get("event_id"),"as_of":event.get("as_of"),"market":event.get("market"),"direction":direction or "NONE","evidence":[{"module":"murphy","statement":murphy.get("statement"),"direction":direction,"strength":murphy.get("strength"),"available":bool(murphy),"source_rule_id":murphy.get("rule_id")},{"module":"nison","statement":nison.get("statement"),"direction":nison_dir,"strength":nison.get("strength"),"available":bool(nison),"source_rule_id":nison.get("rule_id")},{"module":"mtf","statement":mtf.get("statement"),"direction":_direction(mtf.get("direction")),"strength":mtf.get("strength"),"available":bool(mtf),"source_rule_id":None}],"historical_evidence":memories,"gates":{"process":"pass","risk":"pending","murphy":"pass" if direction else "needs_review"},"conflict":"contradicts" if nison_dir and direction and nison_dir != direction else "supports" if direction else "insufficient","decision_hint":decision_hint,"fail_closed":direction is None or (nison_dir and nison_dir != direction)}
