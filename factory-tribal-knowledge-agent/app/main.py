from app.pipeline import process_transcripts_file
from app.storage import load_claims

if __name__ == "__main__":
    results = process_transcripts_file()

    print("\nProcessed Claims:")
    for claim in results:
        print(f'- {claim.entity} | {claim.status} | {claim.recommended_action}')

    print('\nKnowledge Base:')
    for claim in load_claims():
        print(f'- {claim.entity} | {claim.status} | confidence={claim.confidence}')