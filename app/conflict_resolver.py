from app.models import KnowledgeClaim, ClaimStatus


def detect_conflicts(new_claim: KnowledgeClaim, existing_claims: list[KnowledgeClaim]) -> KnowledgeClaim:
    for old_claim in existing_claims:
        same_entity = old_claim.entity == new_claim.entity
        same_condition = old_claim.condition == new_claim.condition
        different_action = old_claim.recommended_action != new_claim.recommended_action

        if same_entity and same_condition and different_action:
            new_claim.status = ClaimStatus.CONFLICTING

            if old_claim.claim_id not in new_claim.contradicts:
                new_claim.contradicts.append(old_claim.claim_id)

            old_claim.status = ClaimStatus.CONFLICTING

            if new_claim.claim_id not in old_claim.contradicts:
                old_claim.contradicts.append(new_claim.claim_id)

    return new_claim