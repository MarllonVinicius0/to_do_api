# controllers/tarefa_controller.py
from datetime import datetime
import json
import os
from database import get_db_connection  # Importa a função de conexão com o banco de dados
from flask import jsonify  # Importa jsonify para retornar respostas JSON
from bson import ObjectId  # Importa ObjectId para manipulação de IDs do MongoDB


class TarefaController:
    @staticmethod
    def serializar_tarefa(tarefa):
        # Serializa a tarefa para JSON, convertendo ObjectId para string
        tarefa["_id"] = str(tarefa["_id"])
        return tarefa

    @staticmethod
    def ler_tarefas():
        tarefas_collection = get_db_connection()  # Obtém a coleção de tarefas do banco de dados
        tarefas = tarefas_collection.find()  # Busca todas as tarefas na coleção
        tarefas_serializadas = [TarefaController.serializar_tarefa(tarefa) for tarefa in tarefas]  # Serializa cada tarefa
        return tarefas_serializadas  # Retorna a lista de tarefas serializadas

    @staticmethod
    def salvar_tarefas(tarefas):
        tarefas_collection = get_db_connection()
        for tarefa in tarefas:
            tarefas_collection.insert_one(tarefa)  # Insere cada tarefa na coleção

    @staticmethod
    def validar_data_conclusao(data_conclusao, data_criacao):
        try:
            data_conclusao = datetime.strptime(data_conclusao, "%d/%m/%Y %H:%M:%S")
            data_criacao = datetime.strptime(data_criacao, "%d/%m/%Y %H:%M:%S")
            if data_conclusao <= data_criacao:
                return False
            return True
        except ValueError:
            return False

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

        status = dados.get("status", "pendente").strip().lower()
        if status not in ["pendente", "concluido", "em andamento"]:
            return {"error": "Status inválido. Use 'pendente', 'em andamento' ou 'concluido'"}, 400

        dataconclusao = dados.get("dataConclusao")
        data_criacao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        if status == "concluido" and not dataconclusao:
            return {"error": "Data de conclusão é obrigatória para status 'concluido'"}, 400  # Se o status for 'concluido', a dataConclusao deve ser fornecida

        if dataconclusao:
            try:
                datetime.strptime(dataconclusao, "%d/%m/%Y %H:%M:%S")
            except ValueError:
                return {"error": "Formato de data de conclusão inválido. Use 'dd/mm/aaaa hh:mm:ss'"}, 400

            # Se o status for 'pendente' ou 'em andamento', a dataConclusao deve ser posterior à dataCriacao
            if status in ["pendente", "em andamento"] and not TarefaController.validar_data_conclusao(dataconclusao, data_criacao):
                return {"error": "Data de conclusão deve ser posterior à data de criação"}, 400

        tarefas_collection = get_db_connection()
        if any(tarefa["descricao"] == descricao for tarefa in tarefas_collection.find()):
            return {"error": "Já existe uma tarefa com essa descrição"}, 409

        # Lógica de criação
        nova_tarefa = {
            "descricao": descricao,
            "status": status,
            "dataCriacao": data_criacao,
            "dataConclusao": dataconclusao
        }

        resultado = tarefas_collection.insert_one(nova_tarefa)  # Insere a nova tarefa na coleção

        nova_tarefa["_id"] = str(resultado.inserted_id)  # Adiciona o ID gerado pelo MongoDB à nova tarefa

        return TarefaController.serializar_tarefa(nova_tarefa), 201  # Retorna a tarefa criada com status 201 (Criado)

    @staticmethod
    def atualizar_tarefa(_id, descricao,status,data_conclusao):
        tarefas_collection = get_db_connection()

        tarefa = tarefas_collection.find_one({"_id": ObjectId(_id)})
        if not tarefa:
            return {"error": "Tarefa não encontrada"}, 404
        
        updates = {}

        if descricao:
            descricao = descricao.strip()
            if not descricao:
                return {"error": "Descrição da tarefa é obrigatória"}, 400
            updates["descricao"] = descricao
        
        if status:
            status = status.strip().lower()
            if status not in ["pendente", "concluido", "em andamento"]:
                return {"error": "Status inválido. Use 'pendente', 'em andamento' ou 'concluido'"}, 400
            updates["status"] = status

            if status == "concluido":
                updates["dataConclusao"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            
                            
                
            if data_conclusao :
                try:
                    datetime.strptime(data_conclusao, "%d/%m/%Y %H:%M:%S")
                except ValueError:
                    return {"error": "Formato de data de conclusão inválido. Use 'dd/mm/aaaa hh:mm:ss'"}, 400

                if status in ["pendente", "em andamento"] and not TarefaController.validar_data_conclusao(data_conclusao, tarefa["dataCriacao"]):
                    return {"error": "Data de conclusão deve ser posterior à data de criação"}, 400

                updates["dataConclusao"] = data_conclusao
        if updates:
            tarefas_collection.update_one({"_id": ObjectId(_id)}, {"$set": updates})

        tarefa_atualizada = tarefas_collection.find_one({"_id": ObjectId(_id)})  # Busca a tarefa atualizada
        
        return TarefaController.serializar_tarefa(tarefa_atualizada), 200  # Retorna a tarefa atualizada com status 200 (OK)

        
    @staticmethod
    def atualizar_status(_id, novo_status):
        if novo_status not in ["pendente", "concluido", "em andamento"]:
            return {"error": "Status inválido. Use 'pendente', 'em andamento' ou 'concluido'"}, 400

        tarefas_collection = get_db_connection()

        tarefa = tarefas_collection.find_one({"_id": ObjectId(_id)})  # Converter _id para ObjectId

        if not tarefa:
            return {"error": "Tarefa não encontrada"}, 404

        if tarefa["status"] == novo_status:
            return {"error": "Status já está definido como o valor fornecido"}, 200

        tarefas_collection.update_one({"_id": ObjectId(_id)}, {"$set": {"status": novo_status}})  # Atualiza o status da tarefa

        if novo_status == "concluido":
            tarefas_collection.update_one({"_id": ObjectId(_id)}, {"$set": {"dataConclusao": datetime.now().strftime("%d/%m/%Y %H:%M:%S")}})
        if novo_status == "pendente":
            tarefas_collection.update_one({"_id": ObjectId(_id)}, {"$set": {"dataConclusao": None}})

        if novo_status == "em andamento":
            tarefas_collection.update_one({"_id": ObjectId(_id)}, {"$set": {"dataConclusao": None}})

        tarefa_atualizada = tarefas_collection.find_one({"_id": ObjectId(_id)})

        return TarefaController.serializar_tarefa(tarefa_atualizada), 200

    @staticmethod
    def remover_tarefa(_id):
        tarefas_collection = get_db_connection()

        tarefa = tarefas_collection.find_one({"_id": ObjectId(_id)})  # Converter _id para ObjectId
        if not tarefa:
            return {"error": "Tarefa não encontrada"}, 404

        tarefas_collection.delete_one({"_id": ObjectId(_id)})  # Deleta a tarefa da coleção
        return {"message": f"Tarefa {tarefa} deletada com sucesso"}, 200  # Retorna mensagem de sucesso com status 200 (OK)