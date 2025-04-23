from flask import Flask, jsonify , request 
from datetime import datetime
import logging
import json
import os

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Função utilitária para ler as tarefas do arquivo JSON
def ler_tarefas():
    if os.path.exists('tarefas.json'):
        with open('tarefas.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Endpoint principal
@app.route('/')
def home():
    return "Bem-vindo à API de Tarefas! - Está Funcionando!"

# Endpoint para listar as tarefas cadastradas
@app.route('/tarefas', methods=['GET'])
def listar_tarefas():
    tarefas = ler_tarefas()
    return jsonify(tarefas), 200

# Função auxiliar para salvar tarefas no arquivo JSON
def salvar_tarefas(tarefas):
    with open('tarefas.json', 'w', encoding='utf-8') as f:
        json.dump(tarefas, f, ensure_ascii=False, indent=4)

# Endpoint para criar uma nova tarefa
@app.route('/tarefas', methods=['POST'])
def create_tarefa():
    try:
        if not request.is_json:
            return jsonify({"error": "Formato de requisição inválido"}), 415 # Verifica se o formato da requisição é JSON

        dados = request.get_json(silent=True) # Tenta obter os dados JSON da requisição

        if dados is None:
            return jsonify({"error": "Corpo da requisição ausente ou inválido"}), 400 # Verifica se o corpo da requisição está vazio ou inválido
        
        if "id" in dados: 
            return jsonify({"error": "ID não deve ser fornecido"}), 400 # Verifica se o ID foi fornecido manualmente

        if dados.get("dataCriacao") is not None:
            return jsonify({"error": "Você não pode definir a data de criação manualmente"}), 400 # Verifica se a data de criação foi fornecida manualmente
        
        if dados.get("dataConclusao") is not None:
            return jsonify({"error": "Você não pode definir a data de conclusão manualmente"}), 400 # Verifica se a data de conclusão foi fornecida manualmente
        
        descricao = dados.get("descricao","").strip()  # Obtém a descrição da tarefa, se não existir retorna uma string vazia e remove espaços em branco

        if not descricao:
            return jsonify({"error": "Descrição da tarefa é obrigatória"}), 400 # Verifica se a descrição da tarefa está vazia
        
        tarefas = ler_tarefas() # Lê as tarefas do arquivo JSON

        for tarefa in tarefas:
            if tarefa["descricao"] == descricao:
                return jsonify({"error": "Já existe uma tarefa com essa descrição"}), 409
        # Verifica se a tarefa já existe com a mesma descrição
        
        novo_id = max([tarefa['id'] for tarefa in tarefas], default=0) + 1 # Gera um novo ID para a tarefa, começando de 1 se não houver tarefas cadastradas

        # Cria um dicionário com os dados da nova tarefa
        nova_tarefa = { 
            "id": novo_id,
            "descricao": descricao,
            "status": "pendente",
            "data_Criacao": datetime.now().strftime("%d/%m;%Y %H:%M:%S"),
            "dataConclusao": None
        }

        tarefas.append(nova_tarefa) # Adiciona a nova tarefa à lista de tarefas
        salvar_tarefas(tarefas) # Salva as tarefas atualizadas no arquivo JSON

        return jsonify(nova_tarefa), 201 # Retorna a nova tarefa criada com status 201 (Criado)
    
    except Exception as e: # Captura qualquer exceção que ocorra durante o processamento
        logging.error(f"Erro interno: {e}") # Registra o erro no log
        return jsonify({"erro": "Erro interno do servidor"}), 500 # Retorna um erro 500 (Erro interno do servidor)

if __name__ == "__main__": # Executa o aplicativo Flask
    app.run(debug=True) # Ativa o modo de depuração para facilitar o desenvolvimento