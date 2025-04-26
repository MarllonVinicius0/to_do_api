import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

print(os.getenv("MONGODB_URI"))  # Verifica se a variável de ambiente está sendo carregada corretamente
def get_db_connection():
    uri = os.getenv("MONGODB_URI")  # Obtém a URI do MongoDB a partir das variáveis de ambiente
    print(f"URI do MongoDB: {uri}")  # Isso deve imprimir a URI completa

    if not uri:
        raise ValueError("URI do MongoDB não encontrada. Verifique seu arquivo .env.")
    
    # Conectar ao MongoDB com a URI
    client = MongoClient(uri, server_api=ServerApi('1'))
    
    # Teste de conexão (ping)
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print("Erro ao conectar ao MongoDB:", e)
        raise e  # Levanta o erro novamente para ser tratado onde necessário
    
    # Conecta ao banco de dados

    db = client['sample_todo']  # Obtém o banco de dados
    tarefas_collection = db.tarefas  # Acessa a coleção 'tarefas'

    return tarefas_collection