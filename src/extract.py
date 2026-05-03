import re
import nltk
from nltk.tokenize import sent_tokenize

nltk.download("punkt")
nltk.download("punkt_tab")


def load_dossier(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def is_real_claim(sentence):
    sentence = sentence.strip()

    if len(sentence) < 40:
        return False

    bad_starts = ("<", ">", "*", "#", "-", "---", "</")
    if sentence.startswith(bad_starts):
        return False

    if sentence.count("\n") > 3:
        return False

    if not re.search(r"[A-Za-z]", sentence):
        return False

    return True


def extract_claims(text):
    sentences = sent_tokenize(text)
    claims = []

    for index, sentence in enumerate(sentences, start=1):
        clean_sentence = sentence.strip()

        if not is_real_claim(clean_sentence):
            continue

        claims.append({
            "claim_id": f"C{len(claims) + 1:03}",
            "text": clean_sentence,
            "type": "unknown",
            "materiality": "medium",
            "paragraph_ref": f"sentence_{index}",
        })

    return claims