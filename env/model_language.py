# model_language.py
import os
import threading
import json
import spacy
from spacy.pipeline import EntityRuler

# 1) Carrega o modelo base do spaCy
nlp = spacy.load("pt_core_news_sm")

# 2) Cria e registra o EntityRuler **antes** do 'ner'
ruler = nlp.add_pipe("entity_ruler", before="ner")

# 3) Carrega seus padrões do JSON
PATTERNS_FILE = os.path.join(os.path.dirname(__file__), "patterns.json")
with open(PATTERNS_FILE, "r", encoding="utf8") as f:
    patterns = json.load(f)

# 4) Adiciona os padrões
ruler.add_patterns(patterns)

# 5) Lock para thread-safety na rota de add_entities
lock = threading.Lock()
