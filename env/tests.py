#Teste de importação de módulos
# Verifica se os módulos 'app' e 'routes' podem ser importados corretamente
def test_imports():
    try:
        import app
        print("App modulo importado com sucesso.")

    except ImportError:
        print("Falha ao importar o módulo app.")

    try:
        import routes
        print("Módulo routes importado com sucesso.")

    except ImportError:
        print("Falha ao importar o módulo routes.")

    try: 
        import model_language
        print("Módulo model_language importado com sucesso.")

    except ImportError:
        print("Falha ao importar o módulo model_language.")

    try: 
        import spacy
        print("Módulo spaCy importado com sucesso.")

    except ImportError:
        print("Falha ao importar o módulo spaCy.")

    try: 
        import pdfminer.high_level
        print("Módulo pdfminer importado com sucesso.")

    except ImportError:
        print("Falha ao importar o módulo pdfminer.")

