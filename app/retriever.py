from app.models import ClaimStatus
from app.storage import load_claims


STOPWORDS = {
    "what", "should", "i", "do", "when", "how", "the", "a", "an",
    "at", "on", "in", "for", "to", "from", "of", "use", "run",
    "is", "are", "it", "everything", "temperature", "current"
}


def tokenize(text: str) -> set[str]:
    cleaned = (
        text.lower()
        .replace("?", "")
        .replace(".", "")
        .replace(",", "")
        .replace("°", "")
        .replace("_", " ")
    )

    return {
        word
        for word in cleaned.split()
        if word not in STOPWORDS and len(word) > 2
    }


def retrieve_knowledge(query: str):
    claims = load_claims()
    query_tokens = tokenize(query)

    safe_claims = [
        claim for claim in claims
        if claim.status in [ClaimStatus.VERIFIED, ClaimStatus.CANDIDATE]
        and claim.confidence >= 0.60
        and len(claim.contradicts) == 0
    ]

    scored_matches = []

    for claim in safe_claims:
        searchable_text = " ".join([
            claim.entity or "",
            claim.process or "",
            claim.condition or "",
            claim.observation or "",
            claim.recommended_action or ""
        ])

        claim_tokens = tokenize(searchable_text)

        overlap = query_tokens.intersection(claim_tokens)
        score = len(overlap)

        if score >= 2:
            scored_matches.append((score, claim))

    scored_matches.sort(key=lambda item: item[0], reverse=True)

    return [claim for score, claim in scored_matches]