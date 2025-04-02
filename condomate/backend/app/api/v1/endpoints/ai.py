from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import Optional
from app.services.ai_service import AIService
from app.security.auth import verify_token
from app.schemas.ai import QueryResponse, DocumentAnalysis, SentimentAnalysis

router = APIRouter()
ai_service = AIService()

@router.post("/process-document", response_model=DocumentAnalysis)
async def process_document(
    file: UploadFile = File(...),
    file_type: str = "receipt",
    token: str = Depends(verify_token)
):
    """
    Process a document using OCR and extract relevant information.
    Supports various document types like receipts, invoices, etc.
    """
    try:
        content = await file.read()
        result = await ai_service.process_document(content, file_type)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}"
        )

@router.post("/query", response_model=QueryResponse)
async def answer_query(
    query: str,
    context: Optional[dict] = None,
    token: str = Depends(verify_token)
):
    """
    Answer user queries about condominium-related topics.
    """
    try:
        result = await ai_service.answer_query(query, context)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )

@router.post("/analyze-sentiment", response_model=SentimentAnalysis)
async def analyze_sentiment(
    text: str,
    token: str = Depends(verify_token)
):
    """
    Analyze the sentiment of user feedback or complaints.
    """
    try:
        result = await ai_service.analyze_sentiment(text)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing sentiment: {str(e)}"
        ) 