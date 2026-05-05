from sources import get_source, validate_citation_ids


def verify_with_sources(claim, sources):
    citation_ids = claim.get("citation_ids", [])
    validation = validate_citation_ids(citation_ids, sources)

    if not citation_ids or validation["missing"]:
        return claim

    matched_sources = validation["resolved"]
    evidence_excerpt = None

    for source_id in matched_sources:
        source = get_source(source_id, sources)
        if source and source.get("excerpt"):
            evidence_excerpt = source["excerpt"]
            break

    claim["source_grounded"] = True
    claim["verification_method"] = "source_grounded"
    claim["matched_sources"] = matched_sources
    claim["evidence_excerpt"] = evidence_excerpt
    claim["verification_verdict"] = "supported"
    claim["verification_reason"] = "Claim cites registered source records."
    claim["proposed_correction"] = "No correction required."
    claim["source_policy_status"] = "approved"
    claim["risk_language_status"] = "low"
    claim["review_status"] = "approved"
    claim["reviewer"] = "source_registry_v0"
    claim["fallback_used"] = False

    return claim
