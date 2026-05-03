from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class Claim(BaseModel):
    claim_id: str
    text: str
    type: str  # (numerical, regulatory, causal, comparative)
    materiality: str  # (low, medium, high)
    paragraph_ref: str

    sources: List[str]
    source_excerpt: Optional[str] = None

    verification_verdict: str  # (supported, partial, unsupported, wrong_number, needs_review)
    verification_reason: Optional[str] = None
    proposed_correction: Optional[str] = None

    source_policy_status: str  # (approved, restricted, disallowed)
    risk_language_status: str  # (pass, needs_hedge, overclaim)

    review_status: str  # (open, corrected, approved)
    reviewer: Optional[str] = None

    timestamp: datetime

class EvidencePack(BaseModel):
    dossier_title: str
    version: str
    generated_at: datetime

    total_claims: int
    numerical_claims: int
    corrected_claims: int
    needs_review: int

    claims: List[Claim]