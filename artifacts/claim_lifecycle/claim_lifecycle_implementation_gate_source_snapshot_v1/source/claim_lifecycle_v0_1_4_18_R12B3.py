from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Set, Tuple
import copy
import math
from urllib.parse import urlsplit, urlunsplit
from datetime import datetime, timezone, timedelta

class Status(str, Enum):
    UNVERIFIED = "UNVERIFIED"
    TENTATIVE = "TENTATIVELY_SUPPORTED"
    SUPPORTED = "SUPPORTED"
    STRONG = "STRONGLY_SUPPORTED"
    NEEDS_REAUDIT = "NEEDS_REAUDIT"
    CONTRADICTED = "CONTRADICTED"
    REVISED = "REVISED"

class ClaimType(str, Enum):
    FACT = "FACT"
    FORECAST = "FORECAST"
    OPINION = "OPINION"
    USER_BELIEF = "USER_BELIEF"
    HYPOTHESIS = "HYPOTHESIS"

@dataclass
class Evidence:
    evidence_id: str
    _direction: str
    _quality: int
    _source_id: str
    independent: bool = True
    derived_from_claim: Optional[str] = None
    age_days: int = 0
    _scope: Optional[str] = None
    evidence_type: ClaimType = ClaimType.FACT
    entails_claim: bool = True
    verified_source: bool = True
    _active: bool = True
    invalidation_reason: Optional[str] = None
    invalidated_at: Optional[str] = None
    admitted_at: Optional[str] = None

    @property
    def direction(self): return self._direction
    @direction.setter
    def direction(self, value):
        if getattr(self, "_mutation_locked", False):
            raise AttributeError("direction is managed by ClaimStore")
        self._direction = value

    @property
    def quality(self): return self._quality
    @quality.setter
    def quality(self, value):
        if getattr(self, "_mutation_locked", False):
            raise AttributeError("quality is managed by ClaimStore")
        self._quality = value

    def __setattr__(self, name, value):
        if name == "evidence_id" and getattr(self, "_mutation_locked", False):
            raise AttributeError("evidence_id is managed by ClaimStore")
        managed = {
            "independent", "derived_from_claim", "age_days",
            "evidence_type", "entails_claim", "verified_source",
            "admitted_at"
        }
        if name in managed and getattr(self, "_mutation_locked", False):
            raise AttributeError(f"{name} is managed by ClaimStore")
        object.__setattr__(self, name, value)

    @property
    def active(self): return self._active
    @active.setter
    def active(self, value):
        if getattr(self, "_mutation_locked", False):
            raise AttributeError("active is managed by ClaimStore")
        self._active = value

    @property
    def source_id(self): return self._source_id
    @source_id.setter
    def source_id(self, value):
        if getattr(self, "_mutation_locked", False):
            raise AttributeError("source_id is managed by ClaimStore")
        self._source_id = value

    @property
    def scope(self): return self._scope
    @scope.setter
    def scope(self, value):
        if getattr(self, "_mutation_locked", False):
            raise AttributeError("scope is managed by ClaimStore")
        self._scope = value

    def _lock_mutation(self):
        self._mutation_locked = True

@dataclass
class Claim:
    claim_id: str
    _text: str
    _claim_type: ClaimType = ClaimType.FACT
    _scope: Optional[str] = None
    _status: Status = field(default=Status.UNVERIFIED, repr=False)
    repetition_count: int = 0
    premise_reuse_count: int = 0
    user_endorsement: str = "ACTIVE"
    audit_triggered: bool = False
    _revision_of: Optional[str] = None
    _revised_by: Optional[str] = None
    _revised_at: Optional[str] = None
    active: bool = True
    _evidence: List[Evidence] = field(default_factory=list, repr=False)
    _parents: List[str] = field(default_factory=list, repr=False)
    _dependents: List[str] = field(default_factory=list, repr=False)
    history: List[str] = field(default_factory=list)

    def __setattr__(self, name, value):
        if name == "claim_id" and getattr(self, "_mutation_locked", False):
            raise AttributeError("claim_id is managed by ClaimStore")
        object.__setattr__(self, name, value)

    @property
    def text(self): return self._text
    @text.setter
    def text(self, value):
        if getattr(self, "_mutation_locked", False):
            raise AttributeError("text is managed by ClaimStore")
        self._text = value

    @property
    def claim_type(self): return self._claim_type
    @claim_type.setter
    def claim_type(self, value):
        if getattr(self, "_mutation_locked", False):
            raise AttributeError("claim_type is managed by ClaimStore")
        self._claim_type = value

    @property
    def scope(self): return self._scope
    @scope.setter
    def scope(self, value):
        if getattr(self, "_mutation_locked", False):
            raise AttributeError("scope is managed by ClaimStore")
        self._scope = value

    @property
    def status(self): return self._status
    @status.setter
    def status(self, value):
        if getattr(self, "_mutation_locked", False):
            raise AttributeError("status is managed by ClaimStore")
        self._status = value

    @property
    def revision_of(self): return self._revision_of
    @revision_of.setter
    def revision_of(self, value):
        if getattr(self, "_mutation_locked", False):
            raise AttributeError("revision_of is managed by ClaimStore")
        self._revision_of = value

    @property
    def revised_by(self): return self._revised_by
    @revised_by.setter
    def revised_by(self, value):
        if getattr(self, "_mutation_locked", False):
            raise AttributeError("revised_by is managed by ClaimStore")
        self._revised_by = value

    @property
    def revised_at(self): return self._revised_at
    @revised_at.setter
    def revised_at(self, value):
        if getattr(self, "_mutation_locked", False):
            raise AttributeError("revised_at is managed by ClaimStore")
        self._revised_at = value

    @property
    def evidence(self): return tuple(self._evidence)

    @property
    def parents(self): return tuple(self._parents)

    @property
    def dependents(self): return tuple(self._dependents)

    def _lock_mutation(self):
        self._mutation_locked = True

class ClaimStore:
    def __init__(self):
        self.claims: Dict[str, Claim] = {}
        self.source_seen: Set[Tuple[str, str]] = set()
        self.evidence_ids: Set[Tuple[str, str]] = set()
        self.source_to_claims: Dict[str, Set[str]] = {}          # historical provenance
        self.active_source_to_claims: Dict[str, Set[str]] = {}   # active evidence only
        self.contradictions: Set[Tuple[str, str]] = set()
        self._now = datetime.now(timezone.utc)

    TERMINAL_STATES = {Status.CONTRADICTED, Status.REVISED}

    @property
    def now(self):
        """Read-only view of the authoritative lifecycle clock."""
        return self._now

    def _is_terminal(self, c):
        return (not c.active) or c.status in self.TERMINAL_STATES

    def _canonical_source_id(self, source_id):
        raw = source_id.strip()
        try:
            parts = urlsplit(raw)
            if parts.scheme and parts.netloc:
                scheme = parts.scheme.lower()
                netloc = parts.netloc.lower()
                # Fragments are not treated as distinct source identity.
                return urlunsplit((scheme, netloc, parts.path, parts.query, ""))
        except Exception:
            pass
        # Minimal fragment-family normalization for file/report-style identifiers.
        return raw.split("#", 1)[0]

    def _register_evidence_identity(self, claim_id, e):
        canon = self._canonical_source_id(e.source_id)
        self.source_seen.add((claim_id, canon))
        self.evidence_ids.add((claim_id, e.evidence_id))
        self.source_to_claims.setdefault(canon, set()).add(claim_id)
        self.active_source_to_claims.setdefault(canon, set()).add(claim_id)
        return canon

    def _refresh_active_source_membership(self, claim_id, canon):
        c = self.claims[claim_id]
        still_active = any(
            getattr(e, "active", True) and self._canonical_source_id(e.source_id) == canon
            for e in c._evidence
        )
        if still_active:
            self.active_source_to_claims.setdefault(canon, set()).add(claim_id)
        else:
            members = self.active_source_to_claims.get(canon)
            if members is not None:
                members.discard(claim_id)
                if not members:
                    self.active_source_to_claims.pop(canon, None)

    def _validate_evidence(self, e):
        # A3: inactive evidence is invalid at the admission boundary.
        # Invalidation is a post-admission lifecycle transition; callers may not
        # submit an already-inactive object and still receive evidence weight.
        if not getattr(e, "active", True):
            return False, "inactive_evidence"
        if e.direction not in {"support", "conflict"}:
            return False, "invalid_evidence_direction"
        if (not isinstance(e.quality, (int, float)) or not math.isfinite(e.quality)
                or e.quality < 0 or e.quality > 4):
            return False, "invalid_evidence_quality"
        if not isinstance(e.source_id, str) or not e.source_id.strip():
            return False, "invalid_source_id"
        if (not isinstance(e.age_days, (int, float)) or not math.isfinite(e.age_days)
                or e.age_days < 0):
            return False, "invalid_age_days"
        return True, "ok"

    def _snapshot_state(self):
        # Snapshot values, but preserve original object identities for rollback.
        claim_states = {}
        for cid, c in self.claims.items():
            claim_states[cid] = {
                "_status": c._status,
                "repetition_count": c.repetition_count,
                "premise_reuse_count": c.premise_reuse_count,
                "user_endorsement": c.user_endorsement,
                "audit_triggered": c.audit_triggered,
                "_revision_of": c._revision_of,
                "_revised_by": c._revised_by,
                "_revised_at": c._revised_at,
                "active": c.active,
                "_text": c._text,
                "_claim_type": c._claim_type,
                "_scope": c._scope,
                "_evidence": copy.deepcopy(c._evidence),
                "_parents": list(c._parents),
                "_dependents": list(c._dependents),
                "history": list(c.history),
            }
        return {
            "claim_ids": set(self.claims.keys()),
            "claim_states": claim_states,
            "source_seen": copy.deepcopy(self.source_seen),
            "evidence_ids": copy.deepcopy(self.evidence_ids),
            "source_to_claims": copy.deepcopy(self.source_to_claims),
            "active_source_to_claims": copy.deepcopy(self.active_source_to_claims),
            "contradictions": copy.deepcopy(self.contradictions),
            "now": self.now,
        }

    def _restore_state(self, snapshot):
        # Remove claims created during the failed transaction.
        for cid in list(self.claims):
            if cid not in snapshot["claim_ids"]:
                del self.claims[cid]

        # Restore fields in-place so existing external object references remain valid.
        for cid, st in snapshot["claim_states"].items():
            c = self.claims[cid]
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

    def _transaction(self, fn):
        snap = self._snapshot_state()
        try:
            return fn()
        except Exception:
            self._restore_state(snap)
            raise

    def _set_status(self, cid, new_status, reason="transition"):
        c = self.claims[cid]
        old_status = c.status
        if old_status == new_status:
            return False
        c.history.append(f"{reason}:{old_status.value}->{new_status.value}")
        c._status = new_status

        # Iterative descendant enforcement avoids recursion depth failure.
        queue = list(c.dependents)
        seen = set()
        while queue:
            child_id = queue.pop(0)
            if child_id in seen:
                continue
            seen.add(child_id)
            self._enforce_derived_ceiling_local(child_id)
            queue.extend(self.claims[child_id].dependents)
        return True

    def _reject_terminal_mutation(self, c, op):
        if self._is_terminal(c):
            c.history.append(f"rejected_{op}:terminal_or_inactive")
            return False, "terminal_or_inactive"
        return True, "ok"

    def _would_create_cycle(self, parent_id, child_id):
        if parent_id == child_id:
            return True
        # Adding parent -> child is illegal if child can already reach parent.
        stack = [child_id]
        seen = set()
        while stack:
            cur = stack.pop()
            if cur == parent_id:
                return True
            if cur in seen:
                continue
            seen.add(cur)
            stack.extend(self.claims[cur].dependents)
        return False

    def add_claim(self, claim):
        # Ownership isolation: a Claim that has already crossed any ClaimStore
        # admission boundary is mutation-locked and must not be shared as the
        # same managed object across stores.
        if getattr(claim, "_mutation_locked", False):
            return False, "claim_already_managed"

        # Clean-admission invariant: externally supplied claims enter pristine.
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
        if claim.claim_id in self.claims:
            return False, "duplicate_claim_id"
        self.claims[claim.claim_id] = claim
        claim._lock_mutation()
        return True, "accepted"

    def _dynamic_age_days(self, e):
        if not getattr(e, "admitted_at", None):
            return e.age_days
        admitted = datetime.fromisoformat(e.admitted_at)
        return e.age_days + max(0, (self.now - admitted).days)

    def _freshness_factor(self, age_days):
        if age_days <= 730: return 1.0
        if age_days <= 1825: return 0.5
        return 0.0

    def _compatible(self, c, e):
        if not e.verified_source: return False, "unverified_source"
        canon = self._canonical_source_id(e.source_id)
        if ((c.claim_id, e.evidence_id) in self.evidence_ids or
                any(stored.evidence_id == e.evidence_id for stored in c._evidence)):
            return False, "duplicate_evidence_id"
        if ((c.claim_id, canon) in self.source_seen or
                any(self._canonical_source_id(stored.source_id) == canon for stored in c._evidence)):
            return False, "duplicate_source"
        if e.derived_from_claim == c.claim_id: return False, "circular_lineage"
        if not e.entails_claim: return False, "non_entailing"
        if c.scope and e.scope and c.scope != e.scope: return False, "scope_mismatch"
        if c.claim_type == ClaimType.FACT and e.evidence_type == ClaimType.FORECAST:
            return False, "forecast_cannot_prove_fact"
        if self._freshness_factor(self._dynamic_age_days(e)) == 0.0: return False, "stale_evidence"
        return True, "ok"

    def _compatible_for_reaudit(self, c, e):
        if not getattr(e, "active", True):
            return False, "invalidated_evidence"
        if not e.verified_source: return False, "unverified_source"
        if e.derived_from_claim == c.claim_id: return False, "circular_lineage"
        if not e.entails_claim: return False, "non_entailing"
        if c.scope and e.scope and c.scope != e.scope: return False, "scope_mismatch"
        if c.claim_type == ClaimType.FACT and e.evidence_type == ClaimType.FORECAST:
            return False, "forecast_cannot_prove_fact"
        if self._freshness_factor(self._dynamic_age_days(e)) == 0.0: return False, "stale_evidence"
        return True, "ok"

    def add_support(self, claim_id, e):
        if claim_id not in self.claims:
            raise KeyError(claim_id)
        valid, reason = self._validate_evidence(e)
        if not valid:
            return False, reason

        def op():
            c = self.claims[claim_id]
            mutable, reason2 = self._reject_terminal_mutation(c, "add_support")
            if not mutable:
                return False, reason2

            ok, reason2 = self._compatible(c, e)
            if not ok:
                if reason2 == "stale_evidence" and c.status in {Status.TENTATIVE, Status.SUPPORTED, Status.STRONG}:
                    self._set_status(claim_id, Status.NEEDS_REAUDIT, "stale_evidence")
                    c.audit_triggered = True
                return False, reason2

            stored = copy.deepcopy(e)
            stored._source_id = self._canonical_source_id(stored.source_id)
            stored.admitted_at = self.now.isoformat()
            stored._lock_mutation()
            self._register_evidence_identity(c.claim_id, stored)
            c._evidence.append(stored)
            weight = stored.quality * self._freshness_factor(stored.age_days)
            if c.status != Status.NEEDS_REAUDIT:
                if weight >= 3:
                    self._set_status(claim_id, Status.SUPPORTED, "support")
                elif weight >= 2 and c.status == Status.UNVERIFIED:
                    self._set_status(claim_id, Status.TENTATIVE, "support")

            self._enforce_derived_ceiling(claim_id)
            return True, "accepted"
        return self._transaction(op)

    def add_conflict(self, claim_id, e):
        if claim_id not in self.claims:
            raise KeyError(claim_id)
        valid, reason = self._validate_evidence(e)
        if not valid:
            return False, reason

        def op():
            c = self.claims[claim_id]
            mutable, reason2 = self._reject_terminal_mutation(c, "add_conflict")
            if not mutable:
                return False, reason2
            ok, reason2 = self._compatible(c, e)
            if not ok:
                return False, reason2
            stored = copy.deepcopy(e)
            stored._source_id = self._canonical_source_id(stored.source_id)
            stored.admitted_at = self.now.isoformat()
            stored._lock_mutation()
            self._register_evidence_identity(c.claim_id, stored)
            c._evidence.append(stored)
            self._set_status(claim_id, Status.NEEDS_REAUDIT, "conflict")
            c.audit_triggered = True
            return True, "accepted"
        return self._transaction(op)

    def invalidate_evidence(self, claim_id, evidence_id, reason="invalidated"):
        if claim_id not in self.claims:
            raise KeyError(claim_id)

        def op():
            c = self.claims[claim_id]
            changed_sources = set()
            found = False
            for e in c._evidence:
                if e.evidence_id == evidence_id and getattr(e, "active", True):
                    e._active = False
                    e.invalidation_reason = reason
                    e.invalidated_at = self.now.isoformat()
                    changed_sources.add(self._canonical_source_id(e.source_id))
                    found = True

            if not found:
                return False, "evidence_not_found"

            for canon in changed_sources:
                self._refresh_active_source_membership(claim_id, canon)

            # Terminal-state precedence: provenance changes, terminal claim state does not.
            if c.status not in {Status.REVISED, Status.CONTRADICTED}:
                self._set_status(claim_id, Status.NEEDS_REAUDIT, "evidence_invalidated")
                c.audit_triggered = True
            else:
                c.history.append(f"evidence_invalidated_terminal:{reason}")

            return True, "accepted"

        return self._transaction(op)

    def revoke_source(self, source_id, reason="source_revoked"):
        canon = self._canonical_source_id(source_id)
        affected = sorted(
            set(self.active_source_to_claims.get(canon, set()))
            | {
                cid for cid, c in self.claims.items()
                if any(
                    getattr(e, "active", True)
                    and self._canonical_source_id(e.source_id) == canon
                    for e in c._evidence
                )
            }
        )
        if not affected:
            return False, "source_not_found"

        def op():
            effective = []
            for cid in affected:
                c = self.claims[cid]
                changed = False
                for e in c._evidence:
                    if self._canonical_source_id(e.source_id) == canon and getattr(e, "active", True):
                        e._active = False
                        e.invalidation_reason = reason
                        e.invalidated_at = self.now.isoformat()
                        changed = True

                if not changed:
                    continue

                effective.append(cid)
                self._refresh_active_source_membership(cid, canon)

                # Terminal state wins over invalidation-induced quarantine.
                if c.status not in {Status.REVISED, Status.CONTRADICTED}:
                    self._set_status(cid, Status.NEEDS_REAUDIT, "source_revoked")
                    c.audit_triggered = True
                else:
                    c.history.append(f"source_revoked_terminal:{reason}")

            if not effective:
                return False, "source_not_found"
            return True, effective

        return self._transaction(op)

    def advance_time(self, days=0):
        if not isinstance(days, (int, float)) or days < 0:
            return False, "invalid_time_delta"
        self._now = self._now + timedelta(days=days)
        return self.refresh_freshness()

    def refresh_freshness(self):
        affected = []
        for cid, c in self.claims.items():
            if c.status in {Status.REVISED, Status.CONTRADICTED}:
                continue
            stale_support = False
            for e in c._evidence:
                if not getattr(e, "active", True):
                    continue
                if not e.admitted_at:
                    continue
                admitted = datetime.fromisoformat(e.admitted_at)
                dynamic_age = self._dynamic_age_days(e)
                if self._freshness_factor(dynamic_age) == 0.0 and e.direction == "support":
                    stale_support = True
                    break
            if stale_support and c.status in {Status.TENTATIVE, Status.SUPPORTED, Status.STRONG}:
                self._set_status(cid, Status.NEEDS_REAUDIT, "freshness_expired")
                c.audit_triggered = True
                affected.append(cid)
        return True, affected

    def repeat_claim(self, cid): self.claims[cid].repetition_count += 1
    def ai_repeats_or_derives(self, cid): pass
    def user_cites_ai_agreement(self, cid): pass
    def user_reports_third_party(self, cid): pass

    def reuse_as_premise(self, cid):
        c = self.claims[cid]
        c.premise_reuse_count += 1
        if c.premise_reuse_count >= 2 and c.status == Status.UNVERIFIED:
            c.audit_triggered = True

    def retract(self, cid):
        self.claims[cid].user_endorsement = "WITHDRAWN"

    def revise(self, old_id, new_claim):
        if old_id not in self.claims:
            raise KeyError(old_id)
        def op():
            old = self.claims[old_id]
            # R5A1: terminal precedence also applies at the revision boundary.
            if self._is_terminal(old):
                old.history.append("rejected_revise:already_revised_or_inactive")
                return False, "already_revised_or_inactive"
            if new_claim.claim_id in self.claims:
                old.history.append("rejected_revise:duplicate_claim_id")
                return False, "duplicate_claim_id"

            self._set_status(old_id, Status.REVISED, "revise")
            old.active = False
            ok, reason = self.add_claim(new_claim)
            if ok:
                new_claim._revision_of = old_id
                old._revised_by = new_claim.claim_id
                old._revised_at = self.now.isoformat()
            if not ok:
                raise RuntimeError(reason)
            return True, "accepted"
        return self._transaction(op)

    def link_dependency(self, parent_id, child_id):
        if parent_id not in self.claims:
            raise KeyError(parent_id)
        if child_id not in self.claims:
            raise KeyError(child_id)

        def op():
            p, ch = self.claims[parent_id], self.claims[child_id]
            if self._is_terminal(p) or self._is_terminal(ch):
                return False, "terminal_or_inactive_dependency"
            if self._would_create_cycle(parent_id, child_id):
                return False, "dependency_cycle"
            if child_id not in p._dependents:
                p._dependents.append(child_id)
            if parent_id not in ch._parents:
                ch._parents.append(parent_id)
            self._enforce_derived_ceiling(child_id)
            return True, "accepted"
        return self._transaction(op)

    def can_use_as_active_premise(self, cid):
        self._enforce_derived_ceiling(cid)
        c = self.claims[cid]
        return c.active and c.status not in {Status.REVISED, Status.CONTRADICTED, Status.NEEDS_REAUDIT}

    def check_cross_claim_contradiction(self, a_id, b_id, contradict):
        if not contradict:
            return False, "no_relation"
        a, b = self.claims[a_id], self.claims[b_id]
        key = tuple(sorted((a_id, b_id)))
        self.contradictions.add(key)
        if a.status in {Status.SUPPORTED, Status.STRONG} and b.status in {Status.SUPPORTED, Status.STRONG}:
            self._set_status(a_id, Status.NEEDS_REAUDIT, "cross_claim_contradiction")
            self._set_status(b_id, Status.NEEDS_REAUDIT, "cross_claim_contradiction")
            a.audit_triggered = b.audit_triggered = True
        return True, "accepted"

    def resolve_contradiction(self, a_id, b_id):
        key = tuple(sorted((a_id, b_id)))
        if key not in self.contradictions:
            return False, "contradiction_not_found"
        self.contradictions.remove(key)
        return True, "accepted"

    def reaudit(self, cid):
        if cid not in self.claims:
            raise KeyError(cid)
        def op():
            c = self.claims[cid]
            # R4A1: terminal precedence applies at the reaudit boundary too.
            if self._is_terminal(c):
                c.history.append("rejected_reaudit:terminal_or_inactive")
                return False, "terminal_or_inactive"

            def w(e, direction):
                ok, _ = self._compatible_for_reaudit(c, e)
                return e.quality * self._freshness_factor(self._dynamic_age_days(e)) if ok and e.direction == direction else 0

            s = sum(w(e, "support") for e in c._evidence)
            x = sum(w(e, "conflict") for e in c._evidence)

            if x >= s + 2:
                new_status = Status.CONTRADICTED
            elif s >= x + 2:
                maxs = max([w(e, "support") for e in c._evidence], default=0)
                new_status = Status.SUPPORTED if maxs >= 3 else Status.TENTATIVE
            else:
                new_status = Status.UNVERIFIED

            self._set_status(cid, new_status, "reaudit")
            self._enforce_derived_ceiling(cid)
            if new_status in {Status.CONTRADICTED, Status.UNVERIFIED, Status.REVISED}:
                self._cascade_reaudit(cid)
            return True, "accepted"
        return self._transaction(op)

    def _cascade_reaudit(self, cid):
        queue = list(self.claims[cid].dependents)
        seen = set()
        while queue:
            x = queue.pop(0)
            if x in seen:
                continue
            seen.add(x)
            child = self.claims[x]
            if child.status not in {Status.REVISED, Status.CONTRADICTED}:
                child._status = Status.NEEDS_REAUDIT
                child.audit_triggered = True
            queue.extend(child.dependents)

    def _enforce_derived_ceiling_local(self, child_id):
        child = self.claims[child_id]
        if not child.parents:
            return False

        parents = [self.claims[p] for p in child.parents]

        quarantine = {Status.NEEDS_REAUDIT, Status.CONTRADICTED, Status.REVISED}
        if any(p.status in quarantine or not p.active for p in parents):
            if child.status not in {Status.REVISED, Status.CONTRADICTED, Status.NEEDS_REAUDIT}:
                child.history.append(f"derived_ceiling:{child.status.value}->NEEDS_REAUDIT")
                child._status = Status.NEEDS_REAUDIT
                child.audit_triggered = True
                return True
            return False

        rank = {
            Status.UNVERIFIED: 1,
            Status.TENTATIVE: 2,
            Status.SUPPORTED: 3,
            Status.STRONG: 4,
            Status.NEEDS_REAUDIT: 1,
            Status.CONTRADICTED: 0,
            Status.REVISED: 0,
        }
        reverse = {
            1: Status.UNVERIFIED,
            2: Status.TENTATIVE,
            3: Status.SUPPORTED,
            4: Status.STRONG,
        }
        ceiling_rank = min(rank[p.status] for p in parents)
        if rank[child.status] > ceiling_rank:
            new_status = reverse[ceiling_rank]
            child.history.append(f"derived_ceiling:{child.status.value}->{new_status.value}")
            child._status = new_status
            child.audit_triggered = True
            return True
        return False

    def _enforce_derived_ceiling(self, child_id):
        changed = self._enforce_derived_ceiling_local(child_id)
        if changed:
            queue = list(self.claims[child_id].dependents)
            seen = set()
            while queue:
                cid = queue.pop(0)
                if cid in seen:
                    continue
                seen.add(cid)
                self._enforce_derived_ceiling_local(cid)
                queue.extend(self.claims[cid].dependents)
        return changed

    def derived_claim_ceiling_ok(self, child_id):
        child = self.claims[child_id]
        if not child.parents: return True
        if child.status == Status.NEEDS_REAUDIT:
            return True
        if any(self.claims[p].status in {Status.NEEDS_REAUDIT, Status.CONTRADICTED, Status.REVISED}
               for p in child.parents):
            return False
        rank = {Status.UNVERIFIED:1, Status.TENTATIVE:2, Status.SUPPORTED:3, Status.STRONG:4}
        if child.status not in rank:
            return child.status in {Status.CONTRADICTED, Status.REVISED}
        ceiling = min(rank[self.claims[p].status] for p in child.parents)
        return rank[child.status] <= ceiling

results=[]
def rec(name, cond): results.append((name, bool(cond)))

s=ClaimStore(); c=Claim("C1","A company will fail next year"); s.add_claim(c)
s.repeat_claim("C1"); rec("T01 repeat does not upgrade", c.status==Status.UNVERIFIED)
s.ai_repeats_or_derives("C1"); rec("T02 AI repetition does not upgrade", c.status==Status.UNVERIFIED)
s.user_cites_ai_agreement("C1"); rec("T03 agreement does not upgrade", c.status==Status.UNVERIFIED)
s.user_reports_third_party("C1"); rec("T04 third-party report not evidence", c.status==Status.UNVERIFIED)
s.reuse_as_premise("C1"); rec("T05 first reuse no status change", c.status==Status.UNVERIFIED)
s.reuse_as_premise("C1"); rec("T06 repeated reuse triggers audit", c.audit_triggered and c.status==Status.UNVERIFIED)
ok,_=s.add_support("C1",Evidence("E1","support",2,"S1")); rec("T07 medium support -> tentative",ok and c.status==Status.TENTATIVE)
ok,_=s.add_conflict("C1",Evidence("E2","conflict",3,"S2")); rec("T08 conflict -> reaudit",ok and c.status==Status.NEEDS_REAUDIT)
s.reaudit("C1"); rec("T09 unresolved -> unverified",c.status==Status.UNVERIFIED)
s.retract("C1"); rec("T10 retraction separate",c.status==Status.UNVERIFIED and c.user_endorsement=="WITHDRAWN")

s=ClaimStore(); c=Claim("C11","X"); s.add_claim(c)
ok,r=s.add_support("C11",Evidence("EY","support",3,"AI_Y",derived_from_claim="C11")); rec("T11 circular blocked",not ok and r=="circular_lineage")
s=ClaimStore(); v1=Claim("C12v1","old"); s.add_claim(v1); s.revise("C12v1",Claim("C12v2","new")); rec("T12 obsolete blocked",not s.can_use_as_active_premise("C12v1"))
s=ClaimStore(); a=Claim("A","X"); b=Claim("B","not X"); s.add_claim(a);s.add_claim(b);s.add_support("A",Evidence("EA","support",3,"SA"));s.add_support("B",Evidence("EB","support",3,"SB"));s.check_cross_claim_contradiction("A","B",True);rec("T13 contradiction reaudit",a.status==Status.NEEDS_REAUDIT and b.status==Status.NEEDS_REAUDIT)
s=ClaimStore(); r=Claim("R","root");ch=Claim("CH","child");gc=Claim("GC","grand");s.add_claim(r);s.add_claim(ch);s.add_claim(gc);s.link_dependency("R","CH");s.link_dependency("CH","GC");r.status=ch.status=gc.status=Status.SUPPORTED;s.add_conflict("R",Evidence("EC","conflict",3,"SC"));s.reaudit("R");rec("T14 dependency cascade",ch.status==Status.NEEDS_REAUDIT and gc.status==Status.NEEDS_REAUDIT)
s=ClaimStore();c=Claim("D","Z");s.add_claim(c);s.add_support("D",Evidence("E1","support",2,"SRC"));ok,r=s.add_support("D",Evidence("E2","support",2,"SRC"));rec("T15 duplicate blocked",not ok and r=="duplicate_source")
s=ClaimStore();c=Claim("S","safe");s.add_claim(c);ok,r=s.add_support("S",Evidence("old","support",3,"OLD",age_days=3650));rec("T16 stale blocked",not ok and r=="stale_evidence")
s=ClaimStore();c=Claim("SC","children",scope="children");s.add_claim(c);ok,r=s.add_support("SC",Evidence("adult","support",3,"AD",scope="adults"));rec("T17 scope blocked",not ok and r=="scope_mismatch")
s=ClaimStore();c=Claim("AU","X");s.add_claim(c);ok,r=s.add_support("AU",Evidence("q","support",3,"reported",verified_source=False));rec("T18 authority blocked",not ok and r=="unverified_source")
s=ClaimStore();c=Claim("EN","bankrupt");s.add_claim(c);ok,r=s.add_support("EN",Evidence("rev","support",3,"filing",entails_claim=False));rec("T19 non-entailing blocked",not ok and r=="non_entailing")
s=ClaimStore();c=Claim("U","X");s.add_claim(c);c.user_endorsement="STRONGLY_ENDORSED";rec("T20 endorsement isolated",c.status==Status.UNVERIFIED)
s=ClaimStore();c=Claim("RL","X");s.add_claim(c);s.add_support("RL",Evidence("S1","support",2,"SRC1"));s.add_conflict("RL",Evidence("C1","conflict",2,"SRC2"));s.reaudit("RL");ok,r=s.add_support("RL",Evidence("S1x","support",3,"SRC1"));rec("T21 relaunder blocked",not ok and r=="duplicate_source" and c.status==Status.UNVERIFIED)
s=ClaimStore();p=Claim("P","A");ch=Claim("K","B");s.add_claim(p);s.add_claim(ch);s.link_dependency("P","K");s.add_support("K",Evidence("W","support",3,"SW"));rec("T22 ceiling violation detected",not s.derived_claim_ceiling_ok("K"))
s=ClaimStore();c=Claim("FT","A happened",claim_type=ClaimType.FACT);s.add_claim(c);ok,r=s.add_support("FT",Evidence("F","support",3,"SF",evidence_type=ClaimType.FORECAST));rec("T23 forecast cannot prove fact",not ok and r=="forecast_cannot_prove_fact")


# v0.1.3 adversarial enforcement tests
s=ClaimStore();p=Claim("P24","parent");ch=Claim("K24","child");s.add_claim(p);s.add_claim(ch);s.link_dependency("P24","K24");s.add_support("K24",Evidence("E24","support",3,"S24"));rec("T24 derived ceiling auto-caps child",ch.status==Status.UNVERIFIED and s.derived_claim_ceiling_ok("K24"))

s=ClaimStore();p=Claim("P25","parent");ch=Claim("K25","child");s.add_claim(p);s.add_claim(ch);s.add_support("K25",Evidence("E25","support",3,"S25"));s.link_dependency("P25","K25");rec("T25 late dependency enforces ceiling",ch.status==Status.UNVERIFIED)

s=ClaimStore();p=Claim("P26","parent");ch=Claim("K26","child");s.add_claim(p);s.add_claim(ch);s.link_dependency("P26","K26");s.add_support("P26",Evidence("PE26","support",3,"PS26"));s.add_support("K26",Evidence("KE26","support",3,"KS26"));s.add_conflict("P26",Evidence("PX26","conflict",5,"PXS26"));s.reaudit("P26");rec("T26 reaudit child blocked as premise",ch.status==Status.NEEDS_REAUDIT and not s.can_use_as_active_premise("K26"))

s=ClaimStore();p1=Claim("P27a","strong parent");p2=Claim("P27b","weak parent");ch=Claim("K27","child");s.add_claim(p1);s.add_claim(p2);s.add_claim(ch);s.add_support("P27a",Evidence("E27a","support",3,"S27a"));s.add_support("P27b",Evidence("E27b","support",2,"S27b"));s.link_dependency("P27a","K27");s.link_dependency("P27b","K27");s.add_support("K27",Evidence("E27c","support",3,"S27c"));rec("T27 weakest required parent sets ceiling",ch.status==Status.TENTATIVE)

s=ClaimStore();p=Claim("P28","parent");ch=Claim("K28","child");s.add_claim(p);s.add_claim(ch);s.link_dependency("P28","K28");s.add_support("K28",Evidence("E28","support",3,"S28"));s.reaudit("K28");rec("T28 child reaudit cannot outrun parent",ch.status==Status.UNVERIFIED)

s=ClaimStore();p=Claim("P29","parent");ch=Claim("K29","child");gc=Claim("G29","grandchild");s.add_claim(p);s.add_claim(ch);s.add_claim(gc);s.add_support("K29",Evidence("E29k","support",3,"S29k"));s.add_support("G29",Evidence("E29g","support",3,"S29g"));s.link_dependency("K29","G29");s.link_dependency("P29","K29");rec("T29 ceiling downgrade cascades descendants",ch.status==Status.UNVERIFIED and gc.status==Status.NEEDS_REAUDIT)

s=ClaimStore();p=Claim("P30","parent");ch=Claim("K30","child");s.add_claim(p);s.add_claim(ch);s.link_dependency("P30","K30");s.add_support("K30",Evidence("E30k","support",3,"S30k"));capped=(ch.status==Status.UNVERIFIED and len(ch.evidence)==1);s.add_support("P30",Evidence("E30p","support",3,"S30p"));s.reaudit("K30");rec("T30 capped child can recover from stored evidence",capped and ch.status==Status.SUPPORTED)


for n,p in results: print(f"{n}: {'PASS' if p else 'FAIL'}")
passed=sum(p for _,p in results)
print(f"\nTOTAL: {passed}/{len(results)} PASS")
if passed != len(results):
    raise SystemExit(1)
