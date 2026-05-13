from app.models import KnowledgeClaim, ClaimStatus

def verify_claim(claim: KnowledgeClaim, exsiting_claims: list[KnowledgeClaim]) -> KnowledgeClaim:
    if claim.confidence < 0.3:
        claim.status = ClaimStatus.QUARANTINED
        return claim
    
    joke_indicators = ['go home early', '200°c','just run everything']
    if any(indicator in claim.source_quote.lower() for indicator in joke_indicators):
        claim.status = ClaimStatus.QUARANTINED
        claim.confidence = min(claim.confidence, 0.15)
        return claim
    
    matching_claims = [
        c for c in exsiting_claims
        if c.entity == claim.entity
        and c.recommended_action == claim.recommended_action
        and c.source_worker_id == claim.source_worker_id
    ]
    
    if matching_claims:
        claim.evidence_count = len(matching_claims) + 1
        claim.confidence = min(1.0, claim.confidence + 0.15 * len(matching_claims))

        if claim.confidence >= 0.80:
            claim.status = ClaimStatus.VERIFIED
        else:
            claim.status = ClaimStatus.CANDIDATE
        return claim
    
    claim.status = ClaimStatus.CANDIDATE
    return claim

