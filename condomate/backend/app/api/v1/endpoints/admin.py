from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.security.auth import get_current_user
from app.models.user import User
from app.services.sentiment_analysis import analyze_conversation
from app.schemas.admin import SentimentAnalysisResponse

router = APIRouter()

@router.get("/conversations")
async def get_tenant_conversations(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")
    
    # TODO: Implement actual conversation fetching from database
    # This is a mock response for now
    return [
        {
            "id": "1",
            "tenant_name": "Juan Pérez",
            "last_message": "El elevador está funcionando mal",
            "last_updated": "2024-04-02T10:00:00"
        },
        {
            "id": "2",
            "tenant_name": "María García",
            "last_message": "Gracias por arreglar la puerta",
            "last_updated": "2024-04-02T09:30:00"
        }
    ]

@router.post("/analyze-sentiment/{conversation_id}")
async def analyze_sentiment(
    conversation_id: str,
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")
    
    # TODO: Implement actual conversation fetching from database
    # This is a mock response for now
    conversation = {
        "id": conversation_id,
        "messages": [
            {"text": "El elevador está funcionando mal", "sender": "tenant"},
            {"text": "Lo siento por las molestias. ¿Podría describir el problema?", "sender": "admin"},
            {"text": "Se detiene en el piso 3 y hace ruidos extraños", "sender": "tenant"}
        ]
    }
    
    analysis = await analyze_conversation(conversation)
    
    return {
        "sentiment": analysis["sentiment"],
        "confidence": analysis["confidence"],
        "topics": analysis["topics"],
        "recommendations": analysis["recommendations"]
    }

@router.post("/sentiment-analysis", response_model=SentimentAnalysisResponse)
async def analyze_conversation_sentiment(
    conversation: dict,
    current_admin: dict = Depends(get_current_admin)
):
    """
    Analiza el sentimiento de una conversación y proporciona recomendaciones.
    """
    try:
        analysis = await analyze_conversation(conversation)
        return analysis
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al analizar la conversación: {str(e)}"
        ) 