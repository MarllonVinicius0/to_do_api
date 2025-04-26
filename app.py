from flask import Flask, request, jsonify
from controllers.tarefa_controller import TarefaController  

app = Flask(__name__)  # Inicializa a aplicação Flask

@app.route('/')
def home():
    return "Bem-vindo à API de Tarefas! Use /tarefas para acessar as tarefas."  # Rota inicial com mensagem de boas-vindas

@app.route('/tarefas', methods=['GET'])
def listar_tarefas():
    try:
        tarefas = TarefaController.ler_tarefas()  # Chama o método para ler tarefas
        return  jsonify(tarefas), 200  # Retorna as tarefas em formato JSON com código de status 200
    except Exception as e:
        return jsonify({"error":f"Erro ao listar tarefas:  str(e)"}), 500


@app.route('/tarefas', methods=['POST'])
def criar_tarefa():
    if not request.is_json:
        return jsonify({"error": "Formato de requisição inválido"}), 415  # Verifica se o corpo da requisição é JSON
    
    try:
        dados = request.get_json()  # Obtém os dados da requisição
    except Exception as e:
        return jsonify({"error": f"Erro ao processar o corpo da requisição: {str(e)}"}), 400
    
    
    response, status_code = TarefaController.criar_tarefa(dados)  # Chama o método para criar uma tarefa
    return jsonify(response), status_code  # Retorna a resposta e o código de status

@app.route('/tarefas/<string:_id>/status', methods=['PATCH'])
def atualizar_status(_id):
    if not request.is_json:
        return jsonify({"error": "Formato de requisição inválido"}), 415  # Verifica se o corpo da requisição é JSON
    
    try:
        dados = request.get_json()  # Obtém os dados da requisição
    except Exception as e:
        return jsonify({"error": f"Erro ao processar o corpo da requisição: {str(e)}"}), 400
   
    if not dados:
        return jsonify({"error": "Corpo da requisição ausente ou inválido"}), 400  # Valida o corpo da requisição
    
    novo_status = dados.get("status", "").strip().lower()

    response, status_code = TarefaController.atualizar_status(_id, novo_status)
    return jsonify(response), status_code
if __name__ == "__main__":
    app.run(debug=True)  # Executa a aplicação em modo de depuração