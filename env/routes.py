# routes.py
import os
import json
import openai
from flask import Blueprint, request, jsonify
from db import get_db
from model_language import nlp, ruler, patterns, PATTERNS_FILE, lock
from io import BytesIO
from pdfminer.high_level import extract_text
from dotenv import load_dotenv
# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# 1) Configure sua API key do OpenAI via variável de ambiente
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    raise RuntimeError("Defina a variável OPENAI_API_KEY no ambiente")
openai.api_key = OPENAI_KEY

bp = Blueprint("routes", __name__)

CATEGORIES = ["hard_skill", "soft_skill", "experiencia", "formacao", "certificacao"]


@bp.route("/entities", methods=["POST"])
def add_entities():
    data = request.get_json()
    new_patterns = data.get("patterns", [])
    if not isinstance(new_patterns, list) or not new_patterns:
        return jsonify(error="Envie uma lista 'patterns' não-vazia."), 400

    with lock:
        ruler.add_patterns(new_patterns)
        patterns.extend(new_patterns)
        with open(PATTERNS_FILE, "w", encoding="utf8") as f:
            json.dump(patterns, f, ensure_ascii=False, indent=2)

    return jsonify(added=len(new_patterns)), 201


@bp.route("/analyze-cv", methods=["POST"])
def analyze_cv():
    if "file" not in request.files:
        return jsonify(error="Nenhum arquivo enviado com a chave 'file'."), 400

    pdf_file = request.files["file"]
    filename = pdf_file.filename

    # 1) Extrai texto do PDF
    try:
        stream = BytesIO(pdf_file.read())
        text = extract_text(stream)
    except Exception as e:
        return jsonify(error=f"Falha ao extrair texto do PDF: {e}"), 500

    # 2) Extrai entidades via spaCy + EntityRuler
    output = {cat: [] for cat in CATEGORIES}
    doc = nlp(text)
    for ent in doc.ents:
        txt, lbl = ent.text.strip(), ent.label_
        if lbl == "HARDSKILL":
            output["hard_skill"].append(txt)
        elif lbl == "SOFTSKILL":
            output["soft_skill"].append(txt)
        elif lbl == "EXPERIENCIA":
            output["experiencia"].append(txt)
        elif lbl == "FORMACAO":
            output["formacao"].append(txt)
        elif lbl == "CERTIFICACAO":
            output["certificacao"].append(txt)
        elif lbl == "ORG" and "Universidade" in txt:
            output["formacao"].append(txt)
    # Remove duplicatas mantendo ordem
    for cat in output:
        output[cat] = list(dict.fromkeys(output[cat]))

    # 3) Persiste no SQLite
    db = get_db()
    db.execute("INSERT OR IGNORE INTO cvs (filename) VALUES (?)", (filename,))
    row = db.execute("SELECT id FROM cvs WHERE filename = ?", (filename,)).fetchone()
    cv_id = row["id"] if row else None
    if cv_id:
        for cat in CATEGORIES:
            db.execute(f"DELETE FROM {cat} WHERE cv_id = ?", (cv_id,))
        for cat, items in output.items():
            for item in items:
                db.execute(
                    f"INSERT INTO {cat} (cv_id, entity) VALUES (?, ?)",
                    (cv_id, item)
                )
        db.commit()

    # 4) Chamada ao GPT-4 para gerar só o summary e o score
    raw_ai = None
    summary_obj = {"summary": None, "score": None}
    try:
        # Limita o texto para não estourar tokens
        snippet = text[:3000] + ("..." if len(text) > 3000 else "")
        payload = {
            "curriculo_nome": filename,
            "texto": snippet
        }
        messages = [
            {
                "role": "system",
                "content": (
                    "Você é um assistente de RH que lê um currículo e retorna APENAS um JSON com duas chaves:\n"
                    "  • 'summary': um breve resumo profissional do candidato.\n"
                    "  • 'score': uma nota inteira de 0 a 100 avaliando a qualidade e completude do currículo.\n"
                    "Não inclua nada além desse JSON."
                )
            },
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)}
        ]
        resp = openai.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0
        )
        raw_ai = resp.choices[0].message.content.strip()
        summary_obj = json.loads(raw_ai)
    except Exception as e:
        # em caso de qualquer erro com o GPT, mantemos summary_obj com None
        summary_obj["gpt_error"] = str(e)
        summary_obj["raw_ai"] = raw_ai

    # 5) Retorna as entidades + summary + score
    return jsonify({
        **output,
        "curriculo_nome": filename,
        "summary": summary_obj.get("summary"),
        "score": summary_obj.get("score"),
        "gpt_error": summary_obj.get("gpt_error"),
        "raw_ai": summary_obj.get("raw_ai"),
    }), 200



@bp.route("/search", methods=["GET"])
def search():
    """
    GET /search?category=hard_skill&value=python
    """
    category = request.args.get("category", "")
    value = request.args.get("value", "").strip().lower()
    if category not in CATEGORIES or not value:
        return jsonify(error="Use ?category=<categoria>&value=<valor>"), 400

    db = get_db()
    rows = db.execute(f"""
        SELECT cvs.filename
        FROM cvs
        JOIN {category} ON cvs.id = {category}.cv_id
        WHERE lower({category}.entity) = ?
    """, (value,)).fetchall()

    files = [r["filename"] for r in rows]
    return jsonify(cvs=files), 200
