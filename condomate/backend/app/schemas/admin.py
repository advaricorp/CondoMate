from pydantic import BaseModel
from typing import List

class SentimentAnalysisResponse(BaseModel):
    sentiment: str
    confidence: float
    topics: List[str]
    recommendations: List[str] 