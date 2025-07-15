# Reconhecedor de Entidades em Currículos (API RH)

Uma API REST em Flask para extrair habilidades, experiências, formações e certificações de currículos em PDF, armazenar no SQLite e gerar um breve resumo e pontuação via OpenAI GPT-4.

---

## 📝 Descrição

Este projeto fornece:

- **Extração de entidades** (hard skills, soft skills, experiência, formação, certificação) de currículos em PDF usando **spaCy** + **EntityRuler** e padrões customizáveis.
- **Persistência** dos resultados em banco de dados **SQLite**.
- **Endpoint** para adicionar novos padrões de entidades dinamicamente.
- **Chamada ao GPT-4** para gerar um pequeno resumo profissional e uma nota de 0 a 100 avaliando o currículo.
- **Busca** de currículos já processados por categoria e valor de entidade.

---

## 🚀 Funcionalidades

- `/entities` (POST):  
  Adiciona novos padrões JSON ao `EntityRuler`.  
  ```json
  // Exemplo de payload
  {
    "patterns": [
      { "label": "HARDSKILL", "pattern": "Go" },
      { "label": "SOFTSKILL", "pattern": [{"LOWER":"resiliência"}] }
    ]
  }

/analyze-cv (POST):
Recebe um PDF (campo file), extrai texto, reconhece entidades, persiste no DB e retorna JSON com:

Listas de entidades por categoria

summary: breve resumo gerado pelo GPT-4

score: nota do currículo

/search (GET):
Busca currículos já processados por ?category=<categoria>&value=<valor>, retornando lista de nomes de arquivos.

🛠 Tecnologias
Python 3.8+

Flask

spaCy (pt_core_news_sm)

EntityRuler + padrões em patterns.json

SQLite (via sqlite3)

OpenAI GPT-4 (biblioteca openai)

pdfminer.six para extração de texto de PDF

dotenv para variáveis de ambiente

📦 Pré-requisitos
Git

Python 3.8 ou superior

Conta e API Key do OpenAI (variável OPENAI_API_KEY)

(Opcional) virtualenv

⚙️ Instalação
Clone o repositório

bash
Copiar
Editar
git clone https://github.com/Coelhomicka/Reconhecedor-Entidades.git
cd Reconhecedor-Entidades
Crie e ative o ambiente virtual

bash
Copiar
Editar
python -m venv env
source env/bin/activate    # Linux/macOS
env\Scripts\Activate       # Windows
Instale as dependências

bash
Copiar
Editar
pip install -r requirements.txt
Configure a variável de ambiente
Crie um arquivo .env na raiz com:

env
Copiar
Editar
OPENAI_API_KEY=seu_token_aqui
🚀 Como usar
Inicialize o banco e suba a API

bash
Copiar
Editar
flask run
Por padrão roda em http://localhost:5000/.

Endpoints principais

GET / → Serve o index.html front-end em static/.

POST /entities → Adiciona padrões de entidade.

POST /analyze-cv → Envia um PDF (form-data com campo file).

GET /search?category=<>&value=<> → Busca currículos por entidade.

📂 Estrutura de pastas
graphql
Copiar
Editar
.
├── app.py             # Cria e configura o Flask App
├── db.py              # Inicialização e conexão SQLite
├── model_language.py  # Carrega spaCy + patterns.json + EntityRuler
├── patterns.json      # Padrões iniciais de entidades
├── routes.py          # Definição dos endpoints
├── schema.sql         # DDL das tabelas SQLite
├── tests.py           # Testes básicos de importação
├── instance/          # Pasta onde fica o arquivo de DB (`cvs.db`)
├── static/            # Front-end estático (index.html, CSS, JS…)
└── .env               # Variáveis de ambiente (não versionado)
✅ Testes
Verifique se todos os módulos importam sem erro:

tests.py

📝 Licença
Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para detalhes.