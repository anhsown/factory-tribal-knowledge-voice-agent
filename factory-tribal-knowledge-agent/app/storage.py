import json
from pathlib import Path
from app.models import KnowledgeClaim

DB_PATH = Path('knowledge_base.json')

def load_claims() -> list[KnowledgeClaim]:
    if not DB_PATH.exists():
        return []
    
    with open(DB_PATH, 'r') as f:
        data = json.load(f)

    return [KnowledgeClaim(**item) for item in data]

def save_claims(claims: list[KnowledgeClaim]) -> None:
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(
            [claim.model_dump(mode='json') for claim in claims],
            f,
            indent = 2,
            ensure_ascii = False
        )

def add_claim(claim: KnowledgeClaim) -> None:
    claims = load_claims()
    claims.append(claim)
    save_claims(claims)