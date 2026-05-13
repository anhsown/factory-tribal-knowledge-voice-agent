from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime


class ClaimStatus(str, Enum):
    CANDIDATE = 'candidate'
    VERIFIED = 'verified'
    CONFLICTING = 'conflicting'
    QUARANTINED = 'quarantined'
    REJECTED = 'rejected'
    NEED_HUMAN_REVIEW = 'need_human_review'

class KnowledgeClaim(BaseModel):
    claim_id: str
    entity: str
    process: Optional[str] = None
    condition: Optional[str] = None
    observation: str
    recommended_action: Optional[str] = None

    source_worker_id: Optional[str] = None
    source_transcript_id: str
    source_quote: str

    confidence: float = Field(ge=0.0, le=1.0)
    status: ClaimStatus = ClaimStatus.CANDIDATE

    contradicts: List[str] = []
    evidence_count: int = 1

    created_at: datetime = Field(default_factory=datetime.utcnow)
