# controllers/tarefa_controller.py
from datetime import datetime
import json
import os
from flask import jsonify

class TarefaController:
    @staticmethod
    def ler_tarefas():
        if os.path.exists('tarefas.json'):
            with open('tarefas.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    @staticmethod
    def salvar_tarefas(tarefas):
        with open('tarefas.json', 'w', encoding='utf-8') as f:
            json.dump(tarefas, f, ensure_ascii=False, indent=4)

    @staticmethod
    def listar_tarefas():
        tarefas = TarefaController.ler_tarefas()
        return jsonify(tarefas), 200

    @staticmethod
    def criar_tarefa(dados):
        # Validações
        if not dados:
            return {"error": "Corpo da requisição ausente ou inválido"}, 400
        
        if "id" in dados:
            return {"error": "ID não deve ser fornecido"}, 400
        
        if dados.get("dataCriacao"):
            return {"error": "Datas não podem ser definidas manualmente"}, 400
        
        descricao = dados.get("descricao", "").strip()
        if not descricao:
            return {"error": "Descrição da tarefa é obrigatória"}, 400
        
        dataconclusao = dados.get("dataConclusao")
        if dataconclusao:
            try:
                datetime.strptime(dataconclusao, "%d/%m/%Y %H:%M:%S")
            except ValueError:
                return {"error": "Formato de data de conclusão inválido. Use 'dd/mm/aaaa hh:mm:ss'"}, 400
        

        tarefas = TarefaController.ler_tarefas()
        if any(tarefa["descricao"] == descricao for tarefa in tarefas):
            return {"error": "Já existe uma tarefa com essa descrição"}, 409

        # Lógica de criação
        novo_id = max([tarefa['id'] for tarefa in tarefas], default=0) + 1
        nova_tarefa = {
            "id": novo_id,
            "descricao": descricao,
            "status": "pendente",
            "data_Criacao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "dataConclusao": dataconclusao
        }
        tarefas.append(nova_tarefa)
        TarefaController.salvar_tarefas(tarefas)
        
        return nova_tarefa, 201

    @staticmethod
    def atualizar_status(tarefa_id, novo_status):
        tarefas = TarefaController.ler_tarefas()
        tarefa = next((t for t in tarefas if t["id"] == tarefa_id), None)
        
        if not tarefa:
            return {"error": f"Tarefa com ID {tarefa_id} não encontrada"}, 404
        
        if novo_status not in ["pendente", "concluido"]:
            return {"error": "Status inválido. Use 'pendente' ou 'concluido'"}, 400
        
        if tarefa["status"] == novo_status:
            return {"error": f"Tarefa já está com status '{novo_status}'"}, 409
        
        tarefa["status"] = novo_status
        tarefa["dataConclusao"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S") if novo_status == "concluido" else None
        TarefaController.salvar_tarefas(tarefas)
        
        return tarefa, 200