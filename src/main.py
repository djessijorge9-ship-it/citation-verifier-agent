from datetime import datetime

from extract import load_dossier, extract_claims
from verify import verify_claims
from render import render_report
from schema import Claim, EvidencePack


def main():
    dossier_text = load_dossier("data/dossier.txt")

    raw_claims = verify_claims(extract_claims(dossier_text))

    raw_claims = raw_claims[:30]

    claims = [
        Claim(
            claim_id=claim["claim_id"],
            text=claim["text"],
            type=claim["type"],
            materiality=claim["materiality"],
            paragraph_ref=claim["paragraph_ref"],
            sources=[],
            source_excerpt=None,
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