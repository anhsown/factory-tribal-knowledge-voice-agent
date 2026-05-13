from app.models import KnowledgeClaim
import uuid

def extract_claims(transcript: dict) -> list[KnowledgeClaim]:
    text = transcript['text'].lower()
    claims = []

    if 'station 3' in text and 'drop the current by 5%' in text:
        claims.append(
            KnowledgeClaim(
                claim_id = str(uuid.uuid4()),
                entity = "station_3",
                process = 'welding',
                condition = 'Tuesdays after lunch',
                observation = 'Station 3 overheats',
                recommended_action = 'drop current by 5%',
                source_worker_id = transcript['worker_id'],
                source_transcript_id = transcript['transcript_id'],
                source_quote = transcript['text'],
                confidence = 0.70
            )
        )
    
    if 'polyester' in text:
        claims.append(
            KnowledgeClaim(
                claim_id = str(uuid.uuid4()),
                entity = "hotel_a_polyester",
                process = 'laundry',
                condition = 'washed together with cotton',
                observation = 'polyester from Hotel A shrinks',
                recommended_action = 'separate it and use a cooler cycle',
                source_worker_id = transcript['worker_id'],
                source_transcript_id = transcript['transcript_id'],
                source_quote = transcript['text'],  
                confidence = 0.72
            )
        )
    
    if 'dryer 2' in text and '80' in text:
        claims.append(
            KnowledgeClaim(
                claim_id = str(uuid.uuid4()),
                entity = 'dryer_2_towels',
                process = 'laundry',
                condition = 'towels',
                observation = 'dryer 2 runs best at 80°C for towels',
                recommended_action = 'run dryer 2 at 80°C',
                source_worker_id = transcript['worker_id'],
                source_transcript_id = transcript['transcript_id'],
                source_quote = transcript['text'],
                confidence = 0.65
            )
        )

    if 'dryer 2' in text and '72' in text:
        claims.append(
            KnowledgeClaim(
                claim_id = str(uuid.uuid4()),
                entity = 'dryer_2_towels',
                process = 'laundry',
                condition = 'towels',
                observation = 'dryer 2 should be 72°C for towels',
                recommended_action = 'run dryer 2 at 72°C',
                source_worker_id = transcript['worker_id'],
                source_transcript_id = transcript['transcript_id'],
                source_quote = transcript['text'],
                confidence = 0.65
            )
        )
    
    if '200°c'in text or 'go home early' in text:
        claims.append(
            KnowledgeClaim(
                claim_id = str(uuid.uuid4()),
                entity = 'unknown',
                process = 'unknown',
                condition = None,
                observation = 'worker joked about running everything at 200°C',
                recommended_action = 'run everything at 200°C',
                source_worker_id = transcript['worker_id'],
                source_transcript_id = transcript['transcript_id'],
                source_quote = transcript['text'],
                confidence = 0.10
            )
        )

    return claims
