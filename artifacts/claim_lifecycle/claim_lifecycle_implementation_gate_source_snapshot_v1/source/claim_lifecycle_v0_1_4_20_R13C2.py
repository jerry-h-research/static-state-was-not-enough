"""R13-C2: require strict boolean semantic discriminators at admission."""
from pathlib import Path as _Path

_prior_path = _Path.cwd() / "src" / "claim_lifecycle_v0_1_4_19_R13C1.py"
_prior_source = _prior_path.read_text(encoding="utf-8").split("\nresults=[]", 1)[0]
exec(compile(_prior_source, str(_prior_path), "exec"), globals())
_R13C1ClaimStore = ClaimStore


class ClaimStore(_R13C1ClaimStore):
    def _validate_evidence(self, e):
        if not isinstance(e.verified_source, bool):
            return False, "invalid_verified_source_type"
        if not isinstance(e.entails_claim, bool):
            return False, "invalid_entails_claim_type"
        return super()._validate_evidence(e)


results=[]
