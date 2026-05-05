import json


def load_sources(path="data/sources.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_source(source_id, sources):
    return sources.get(source_id.upper())


def validate_citation_ids(citation_ids, sources):
    resolved = []
    missing = []

    for citation_id in citation_ids:
        normalized_id = citation_id.upper()
        if normalized_id in sources:
            resolved.append(normalized_id)
        else:
            missing.append(normalized_id)

    return {
        "resolved": resolved,
        "missing": missing,
    }
