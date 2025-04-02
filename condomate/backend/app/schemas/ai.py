from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class DocumentAnalysis(BaseModel):
    type: str
    amount: Optional[float] = None
    date: Optional[str] = None
    description: Optional[str] = None
    raw_text: Optional[str] = None
    parsed_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    confidence: float
    source: str
    context: Optional[Dict[str, Any]] = None

class SentimentAnalysis(BaseModel):
    sentiment: str
    positive_score: int
    negative_score: int
    timestamp: str
    details: Optional[Dict[str, Any]] = None 