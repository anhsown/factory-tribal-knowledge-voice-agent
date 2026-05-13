import json
from pathlib import Path

from app.extractor import extract_claims
from app.storage import load_claims, save_claims
from app.verifier import verify_claim
from app.conflict_resolver import detect_conflicts

def process_transcript(transcript: dict):
    existing_claims = load_claims()
    extracted_claims = extract_claims(transcript)
    processed_claims = []

    for claim in extracted_claims:
        claim = verify_claim(claim, existing_claims)

        if claim.status not in ["quarantined", "rejected"]:
            claim = detect_conflicts(claim, existing_claims)

        existing_claims.append(claim)
        processed_claims.append(claim)

    save_claims(existing_claims)
    return processed_claims

def process_transcripts_file(path: str = 'data/transcripts.jsonl'):
    results = []

    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            transcript = json.loads(line)
            processed = process_transcript(transcript)
            results.extend(processed)

    return results