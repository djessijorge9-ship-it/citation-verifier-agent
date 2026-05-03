def verify_claims(claims):
    verified_claims = []

    for claim in claims:
        text = claim["text"]
        lower = text.lower()

        claim_type = "unknown"
        verdict = "supported"
        severity = "low"
        reason = "Claim appears supported on current evidence."
        correction = None

        has_number = "%" in text or any(char.isdigit() for char in text)
        is_regulatory = any(term in lower for term in ["fca", "compliance", "regulatory", "consumer duty", "financial promotion"])
        is_causal = any(term in lower for term in ["because", "therefore", "drives", "leads to", "results in"])
        is_comparative = any(term in lower for term in ["versus", "compared", "spread", "gap", "higher", "lower", "better", "worse"])

        if has_number:
            claim_type = "numerical"
        elif is_regulatory:
            claim_type = "regulatory"
        elif is_causal:
            claim_type = "causal"
        elif is_comparative:
            claim_type = "comparative"

        # HIGH: approval-blocking issues
        if "not directly comparable" in lower and ("dominant" in lower or "points to" in lower):
            verdict = "unsupported"
            severity = "high"
            reason = "Benchmark/comparative claim may mislead without clear caveats."
            correction = "Add explicit caveat about comparability or methodology."

        # MEDIUM: needs softer wording / caveat
        elif any(term in lower for term in ["dominant", "most parsimonious", "too large to attribute", "primary performance"]):
            verdict = "needs_review"
            severity = "medium"
            reason = "Claim wording or context could affect interpretation."
            correction = "Qualify the claim or provide stronger substantiation."

        elif has_number and any(term in lower for term in ["versus", "spread", "gap", "comparison"]):
            verdict = "needs_review"
            severity = "medium"
            reason = "Numerical comparison may need additional context."
            correction = "Add qualifying language, clarify methodology, or contextualise numbers."

        # LOW: supported claims
        else:
            verdict = "supported"
            severity = "low"
            reason = "Claim appears supported on current evidence."
            correction = None

        claim["type"] = claim_type
        claim["verification_verdict"] = verdict
        claim["verification_reason"] = reason
        claim["proposed_correction"] = correction or "No correction required."
        claim["source_policy_status"] = "approved"
        claim["risk_language_status"] = severity
        claim["review_status"] = "approved" if verdict == "supported" else "pending"
        claim["reviewer"] = "system_v0"

        verified_claims.append(claim)

    return verified_claims