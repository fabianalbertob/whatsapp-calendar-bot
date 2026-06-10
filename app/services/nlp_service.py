import spacy
from app.utils.logger import logger

class NLPService:
    def __init__(self):
        try:
            self.nlp = spacy.load("es_core_news_md")
        except OSError:
            logger.warning("Modelo spaCy no encontrado. Ejecuta: python -m spacy download es_core_news_md")
            self.nlp = None

    def extract_intent(self, text: str) -> dict:
        if not self.nlp:
            # Fallback a reglas simples
            text_lower = text.lower()
            if any(k in text_lower for k in ["turno", "horario", "disponible"]):
                return {"intent": "check_availability", "entities": {}}
            if any(k in text_lower for k in ["reservar", "agendar", "quiero"]):
                return {"intent": "book_appointment", "entities": {}}
            return {"intent": "greeting", "entities": {}}
        
        doc = self.nlp(text)
        
        # Extracción básica de entidades y keywords
        entities = {
            "dates": [ent.text for ent in doc.ents if ent.label_ == "DATE"],
            "times": [ent.text for ent in doc.ents if ent.label_ == "TIME"],
        }
        
        intent = "unknown"
        text_lower = text.lower()
        if any(word in text_lower for word in ["horario", "turno", "disponible", "cuando"]):
            intent = "check_availability"
        elif any(word in text_lower for word in ["reservar", "agendar", "quiero", "sacar"]):
            intent = "book_appointment"
        
        return {"intent": intent, "entities": entities, "doc": doc}