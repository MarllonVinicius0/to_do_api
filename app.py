from flask import Flask, jsonify , request 
from datetime import datetime
import json
import os

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
        dados = request.get_json()

        if not dados:
            return jsonify({"error": "Corpo da requisição ausente ou inválido"}), 400 # Verifica se o corpo da requisição está vazio ou inválido
        
        descricao = dados.get("descricao","").strip()

        if not descricao:
            return jsonify({"error": "Descrição da tarefa é obrigatória"}), 400 # Verifica se a descrição da tarefa está vazia
        
        tarefas = ler_tarefas()
        novo_id = max([tarefa['id'] for tarefa in tarefas], default=0) + 1

        nova_tarefa = {
            "id": novo_id,
            "descricao": descricao,
            "status": "pendente",
            "data_criacao": datetime.now().strftime("%d/%m;%Y %H:%M:%S"),
            "dataConclusao": None
        }

        tarefas.append(nova_tarefa)
        salvar_tarefas(tarefas)

        return jsonify(nova_tarefa), 201
    
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor", "detalhes" : str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)