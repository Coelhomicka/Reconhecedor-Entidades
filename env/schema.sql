-- schema.sql

CREATE TABLE IF NOT EXISTS cvs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT UNIQUE NOT NULL
);

-- Uma tabela por categoria de entidade
CREATE TABLE IF NOT EXISTS hard_skill (
    cv_id INTEGER NOT NULL,
    entity TEXT NOT NULL,
    FOREIGN KEY (cv_id) REFERENCES cvs (id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS soft_skill (
    cv_id INTEGER NOT NULL,
    entity TEXT NOT NULL,
    FOREIGN KEY (cv_id) REFERENCES cvs (id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS experiencia (
    cv_id INTEGER NOT NULL,
    entity TEXT NOT NULL,
    FOREIGN KEY (cv_id) REFERENCES cvs (id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS formacao (
    cv_id INTEGER NOT NULL,
    entity TEXT NOT NULL,
    FOREIGN KEY (cv_id) REFERENCES cvs (id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS certificacao (
    cv_id INTEGER NOT NULL,
    entity TEXT NOT NULL,
    FOREIGN KEY (cv_id) REFERENCES cvs (id) ON DELETE CASCADE
);
