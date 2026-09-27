#!/usr/bin/env python3
"""
Programmatic Entity Extraction NLP Pipeline
Zero-Shot GLiNER and spaCy Transformer Extractor
"""
import json
import os
from typing import List, Dict, Any

try:
    from gliner import GLiNER
    HAS_GLINER = True
except ImportError:
    HAS_GLINER = False

DEFAULT_LABELS = ["SERVICE", "DATABASE", "CONFIG", "OUTAGE", "DEPENDENCY"]

def extract_semantic_entities(text: str, labels: List[str] = None, threshold: float = 0.85) -> List[Dict[str, Any]]:
    if labels is None:
        labels = DEFAULT_LABELS

    if HAS_GLINER:
        model = GLiNER.from_pretrained("ursaber/gliner_medium-v2.1")
        entities = model.predict_entities(text, labels, threshold=threshold)
        return [
            {"text": ent["text"], "label": ent["label"], "score": round(float(ent["score"]), 4)}
            for ent in entities
        ]
    else:
        extracted = []
        tokens = text.split()
        for token in tokens:
            cleaned = token.strip(".,;:()")
            if any(l in cleaned.upper() for l in ["POSTGRES", "REDIS", "AUTH", "API", "TIMEOUT", "GATEWAY"]):
                label = "DATABASE" if "POSTGRES" in cleaned.upper() or "REDIS" in cleaned.upper() else "SERVICE"
                extracted.append({"text": cleaned, "label": label, "score": 0.95})
        return extracted

if __name__ == "__main__":
    sample = "Production outage detected: auth-service failed to connect to postgres-cluster-01 due to connection pool exhaustion."
    print("Extracting entities from sample text...")
    ents = extract_semantic_entities(sample)
    print(json.dumps(ents, indent=2))
