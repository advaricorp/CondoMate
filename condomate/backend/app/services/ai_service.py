from typing import Optional, Dict, Any
import pytesseract
from PIL import Image
import io
import json
from datetime import datetime

class AIService:
    def __init__(self):
        # Configure pytesseract to use the system Tesseract installation
        pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
        
    async def process_document(self, file_content: bytes, file_type: str) -> Dict[str, Any]:
        """
        Process a document using OCR and extract relevant information.
        Supports various document types like receipts, invoices, etc.
        """
        try:
            # Convert bytes to image
            image = Image.open(io.BytesIO(file_content))
            
            # Extract text using OCR
            text = pytesseract.image_to_string(image)
            
            # Parse the extracted text based on document type
            if file_type == "receipt":
                return self._parse_receipt(text)
            elif file_type == "invoice":
                return self._parse_invoice(text)
            else:
                return {"text": text, "type": "unknown"}
                
        except Exception as e:
            return {"error": str(e), "type": "error"}
    
    def _parse_receipt(self, text: str) -> Dict[str, Any]:
        """Parse receipt text to extract relevant information."""
        # Basic receipt parsing logic
        # This can be enhanced with more sophisticated NLP
        lines = text.split('\n')
        amount = None
        date = None
        description = None
        
        for line in lines:
            # Look for amount patterns (e.g., $123.45)
            if '$' in line:
                try:
                    amount = float(line.split('$')[1].strip())
                except:
                    continue
                    
            # Look for date patterns
            if any(month in line.lower() for month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']):
                date = line.strip()
                
            # Use the first non-empty line as description
            if not description and line.strip():
                description = line.strip()
        
        return {
            "type": "receipt",
            "amount": amount,
            "date": date,
            "description": description,
            "raw_text": text
        }
    
    def _parse_invoice(self, text: str) -> Dict[str, Any]:
        """Parse invoice text to extract relevant information."""
        # Similar to receipt parsing but with invoice-specific fields
        return {
            "type": "invoice",
            "raw_text": text,
            "parsed_data": self._parse_receipt(text)  # Reuse receipt parsing for now
        }
    
    async def answer_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Answer user queries about condominium-related topics.
        Can be enhanced with RAG (Retrieval-Augmented Generation) for better answers.
        """
        # Basic query answering logic
        # This can be enhanced with more sophisticated NLP and RAG
        query = query.lower()
        
        # Common condominium queries and their answers
        common_answers = {
            "payment": {
                "keywords": ["payment", "pay", "due", "fee", "maintenance"],
                "answer": "Maintenance fees are typically due on the first of each month. You can make payments through the online portal or contact the administration office for alternative payment methods."
            },
            "maintenance": {
                "keywords": ["maintenance", "repair", "fix", "issue", "problem"],
                "answer": "For maintenance requests, please submit a ticket through the online portal or contact the maintenance department directly. Emergency repairs are available 24/7."
            },
            "meeting": {
                "keywords": ["meeting", "assembly", "gathering", "event"],
                "answer": "Regular board meetings are held monthly. The schedule is available in the calendar section. Special meetings will be announced with at least 48 hours notice."
            }
        }
        
        # Find the most relevant answer based on keywords
        best_match = None
        max_matches = 0
        
        for category, data in common_answers.items():
            matches = sum(1 for keyword in data["keywords"] if keyword in query)
            if matches > max_matches:
                max_matches = matches
                best_match = data["answer"]
        
        if best_match:
            return {
                "answer": best_match,
                "confidence": max_matches / len(common_answers),
                "source": "knowledge_base"
            }
        else:
            return {
                "answer": "I apologize, but I couldn't find a specific answer to your query. Please contact the administration office for assistance.",
                "confidence": 0,
                "source": "fallback"
            }
    
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze the sentiment of user feedback or complaints.
        """
        # Basic sentiment analysis
        # This can be enhanced with more sophisticated NLP models
        positive_words = {"good", "great", "excellent", "happy", "satisfied", "thank"}
        negative_words = {"bad", "poor", "terrible", "unhappy", "dissatisfied", "complain"}
        
        words = set(text.lower().split())
        positive_count = len(words.intersection(positive_words))
        negative_count = len(words.intersection(negative_words))
        
        if positive_count > negative_count:
            sentiment = "positive"
        elif negative_count > positive_count:
            sentiment = "negative"
        else:
            sentiment = "neutral"
            
        return {
            "sentiment": sentiment,
            "positive_score": positive_count,
            "negative_score": negative_count,
            "timestamp": datetime.utcnow().isoformat()
        } 