"""R13-C1: protect canonical claim-registry identity from public replacement."""
from pathlib import Path as _Path
from types import MappingProxyType

_prior_path = _Path.cwd() / "src" / "claim_lifecycle_v0_1_4_18_R12B3.py"
_prior_source = _prior_path.read_text(encoding="utf-8").split("\nresults=[]", 1)[0]
exec(compile(_prior_source, str(_prior_path), "exec"), globals())
_R12B3ClaimStore = ClaimStore


class ClaimStore(_R12B3ClaimStore):
    def __init__(self):
        self._claims = {}
        self.source_seen = set()
        self.evidence_ids = set()
        self.source_to_claims = {}
        self.active_source_to_claims = {}
        self.contradictions = set()
        self._now = datetime.now(timezone.utc)

    @property
    def claims(self):
        """Normal lookup view; lifecycle registry writes remain store-owned."""
        return MappingProxyType(self._claims)

    def add_claim(self, claim):
        if getattr(claim, "_mutation_locked", False):
            return False, "claim_already_managed"
        if claim.status != Status.UNVERIFIED:
            return False, "dirty_initial_status"
        if claim._evidence:
            return False, "preloaded_evidence"
        if claim._parents or claim._dependents:
            return False, "preloaded_graph"
        if claim.revision_of is not None or claim.revised_by is not None or claim.revised_at is not None:
            return False, "preloaded_revision_provenance"
        if claim.history:
            return False, "preloaded_history"
        if claim.repetition_count != 0:
            return False, "dirty_repetition_count"
        if claim.premise_reuse_count != 0:
            return False, "dirty_premise_reuse_count"
        if claim.audit_triggered:
            return False, "dirty_audit_state"
        if claim.active is not True:
            return False, "dirty_active_state"
        if claim.user_endorsement != "ACTIVE":
            return False, "dirty_user_endorsement"
        if not isinstance(claim.claim_id, str) or not claim.claim_id.strip():
            return False, "invalid_claim_id"
        if not isinstance(claim.text, str) or not claim.text.strip():
            return False, "invalid_claim_text"
        if claim.claim_id in self._claims:
            return False, "duplicate_claim_id"
        self._claims[claim.claim_id] = claim
        claim._lock_mutation()
        return True, "accepted"

    def _restore_state(self, snapshot):
        for cid in list(self._claims):
            if cid not in snapshot["claim_ids"]:
                del self._claims[cid]
        for cid, st in snapshot["claim_states"].items():
            c = self._claims[cid]
            c._status = st["_status"]
            c.repetition_count = st["repetition_count"]
            c.premise_reuse_count = st["premise_reuse_count"]
            c.user_endorsement = st["user_endorsement"]
            c.audit_triggered = st["audit_triggered"]
            c._revision_of = st["_revision_of"]
            c._revised_by = st["_revised_by"]
            c._revised_at = st["_revised_at"]
            c.active = st["active"]
            c._text = st["_text"]
            c._claim_type = st["_claim_type"]
            c._scope = st["_scope"]
            c._evidence[:] = copy.deepcopy(st["_evidence"])
            c._parents[:] = st["_parents"]
            c._dependents[:] = st["_dependents"]
            c.history[:] = st["history"]
        self.source_seen = snapshot["source_seen"]
        self.evidence_ids = snapshot["evidence_ids"]
        self.source_to_claims = snapshot["source_to_claims"]
        self.active_source_to_claims = snapshot["active_source_to_claims"]
        self.contradictions = snapshot["contradictions"]
        self._now = snapshot["now"]


results=[]
