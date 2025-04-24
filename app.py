from flask import Flask, request, jsonify
from controllers.tarefa_controller import TarefaController  

app = Flask(__name__)  # Inicializa a aplicação Flask

@app.route('/')
def home():
    return "Bem-vindo à API de Tarefas! Use /tarefas para acessar as tarefas."  # Rota inicial com mensagem de boas-vindas

@app.route('/tarefas', methods=['GET'])
def listar_tarefas():
    return TarefaController.listar_tarefas()  # Chama o método para listar tarefas

@app.route('/tarefas', methods=['POST'])
def criar_tarefa():
    if not request.is_json:
        return jsonify({"error": "Formato de requisição inválido"}), 415  # Verifica se o corpo da requisição é JSON
    
    dados = request.get_json(silent=True)  # Obtém os dados da requisição
    response, status_code = TarefaController.criar_tarefa(dados)  # Chama o método para criar uma tarefa
    return jsonify(response), status_code  # Retorna a resposta e o código de status

@app.route('/tarefas/<int:tarefa_id>/status', methods=['PATCH'])
def atualizar_status(tarefa_id):
    if not request.is_json:
        return jsonify({"error": "Formato de requisição inválido"}), 415  # Verifica se o corpo da requisição é JSON
    
    dados = request.get_json(silent=True)  # Obtém os dados da requisição
    if not dados:
        return jsonify({"error": "Corpo da requisição ausente ou inválido"}), 400  # Valida o corpo da requisição
    
    novo_status = dados.get("status")  # Obtém o novo status da tarefa
    response, status_code = TarefaController.atualizar_status(tarefa_id, novo_status)  # Atualiza o status da tarefa
    return jsonify(response), status_code  # Retorna a resposta e o código de status

if __name__ == "__main__":
    app.run(debug=True)  # Executa a aplicação em modo de depuração