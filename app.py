from flask import Flask, jsonify 
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


if __name__ == "__main__":
    app.run(debug=True)