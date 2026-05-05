from datetime import datetime

from extract import load_dossier, extract_claims
from verify import verify_claims
from sources import load_sources
from source_verify import verify_with_sources
from render import render_report
from schema import Claim, EvidencePack


def main():
    dossier_text = load_dossier("data/dossier.txt")
    sources = load_sources()

    raw_claims = []

    for claim in extract_claims(dossier_text):
        claim = verify_with_sources(claim, sources)

        if not claim.get("source_grounded"):
            claim = verify_claims([claim])[0]
            claim["source_grounded"] = False
            claim["matched_sources"] = []
            claim["evidence_excerpt"] = None
            claim["verification_method"] = "heuristic"
            claim["fallback_used"] = True

        raw_claims.append(claim)

    raw_claims = raw_claims[:30]

    claims = [
        Claim(
            claim_id=claim["claim_id"],
            text=claim["text"],
            type=claim["type"],
            materiality=claim["materiality"],
            paragraph_ref=claim["paragraph_ref"],
            sources=claim.get("matched_sources", []),
            source_excerpt=claim.get("evidence_excerpt"),
            verification_verdict=claim["verification_verdict"],
            verification_reason=claim["verification_reason"],
            proposed_correction=claim["proposed_correction"],
            source_policy_status=claim["source_policy_status"],
            risk_language_status=claim["risk_language_status"],
            review_status=claim["review_status"],
            reviewer=claim["reviewer"],
            timestamp=datetime.now(),
        )
        for claim in raw_claims
    ]

    pack = EvidencePack(
        dossier_title="Building Reliable AI Agents for Institutional Equity Research",
        version="v0.1",
        generated_at=datetime.now(),
        total_claims=len(claims),
        numerical_claims=sum(1 for c in claims if c.type == "numerical"),
        corrected_claims=sum(1 for c in claims if c.verification_verdict != "supported"),
        needs_review=sum(1 for c in claims if c.verification_verdict == "needs_review"),
        claims=claims,
    )

    output_path = render_report(pack)

    print("Evidence Pack generated:")
    print(output_path)


if __name__ == "__main__":
    main()
