import re


CITATION_BLOCK_RE = re.compile(r"\[([Ss]\d{3}(?:\s*,\s*[Ss]\d{3})*)\]")


def extract_citation_ids(text):
    citation_ids = []

    for match in CITATION_BLOCK_RE.finditer(text):
        citation_block = match.group(1)
        for citation_id in citation_block.split(","):
            citation_ids.append(citation_id.strip().upper())

    return citation_ids
