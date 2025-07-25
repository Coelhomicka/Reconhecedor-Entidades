# db.py
import sqlite3
from flask import g, current_app

def get_db():
    """Abre uma conexão por request, guarda em g."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """Fecha a conexão ao final do request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Inicializa o schema no banco."""
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
