# API de Tarefas 📝

[![Status](https://img.shields.io/badge/status-active-brightgreen)](https://to-do-api-fi7j.onrender.com)

Esta é uma API de gerenciamento de tarefas desenvolvida com Flask e MongoDB. Ela permite criar, listar, atualizar e remover tarefas de forma simples e eficiente. A API está hospedada no Render e pode ser acessada em [https://to-do-api-fi7j.onrender.com](https://to-do-api-fi7j.onrender.com).


### Atenção sobre o Link da API

O link da API pode demorar alguns segundos para carregar em alguns momentos, devido à configuração do serviço gratuito de hospedagem **Render**. Quando a aplicação não é acessada por um tempo, o servidor entra em **sleep** e demora para acordar, mas isso não afeta o funcionamento da API após a inicialização. Esse comportamento é esperado em serviços gratuitos.

---
# Como Executar o Projeto Localmente 🛠️
1. Clone este repositório:
   
```bash
   git clone https://github.com/MarllonVinicius0/to_do_api.git
```

2. Ambiente Virtualizado (Opcional)
Para organização e facilitar em rodar o projeto, sugiro criar um ambiente virtualizado. Para isso, basta usar o comando abaixo:
```Bash
  python -m venv .venv
```
```Bash
  .venv\Scripts\activate
```

3. Instale as dependências: 

```bash
   pip install -r requirements.txt
```
   
4. Configuração do MongoDB:
   A API usa o MongoDB para armazenar os dados.
   Se você não tem o MongoDB configurado, crie uma conta no MongoDB Atlas (ou use uma instância local do MongoDB)
   e gere as credenciais de acesso. Adicione a URL de conexão do MongoDB ao arquivo .env (exemplo abaixo): 

```bash
   MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority
```
5. Rodando a API:
   Após instalar as dependências e configurar o banco de dados, inicie a API localmente com o seguinte comando:

```bash
   python app.py
```
6. Acessando a API:
   A API estará disponível em http://127.0.0.1:5000, e você pode testar os endpoints localmente usando ferramentas como o [Postman](https://www.postman.com) ou o navegador.
   
## Tecnologias Utilizadas 🌐

- **Flask**: Framework utilizado para a construção da API.
- **Python**: Linguagem de programação principal.
- **MongoDB Atlas**: Serviço de banco de dados para armazenar as tarefas.
- **Flask-RESTX**: Biblioteca utilizada para criar a API RESTful e documentar com Swagger.


## Recursos da API 🔧

- **Criar Tarefa**: Adicione novas tarefas com descrição, status e data de conclusão.
- **Listar Tarefas**: Obtenha todas as tarefas cadastradas.
- **Atualizar Tarefa**: Modifique os detalhes de uma tarefa existente.
- **Remover Tarefa**: Delete tarefas que não são mais necessárias.
- **Atualizar Status**: Altere o status de uma tarefa (pendente, em andamento, concluído).

---

## Endpoints 📡

### POST `/tarefas` - Criar uma nova tarefa
**Request Body:**
```json
{
    "descricao": "Estudar Flask",
    "status": "pendente",
    "dataconclusao": "27/04/2025 12:00:00"
}
```
## GET `/tarefas` - Listar todas as tarefas

**Respostas:**
- `200 OK`: Lista de tarefas retornada com sucesso.

---

## PATCH `/tarefas/{_id}` - Atualizar uma tarefa

**Request Body:**
```json
{
  "_id" : "680daa65d83a1839c9fac560"
  "descricao": "Estudar Flask Avançado",
  "status": "concluido",
  "dataConclusao": "28/04/2025 12:00:00"
}
```

---

### DELETE /tarefas/{_id} - Remover uma tarefa
**Request Body:**
```json
{
  "_id" : "680daa65d83a1839c9fac560"
}
```
**Respostas:**

- `204 No Content`: Tarefa removida com sucesso.
- `404 Not Found`: Tarefa não encontrada.

### PATCH /tarefas/{_id}/status - Atualizar o status de uma tarefa

**Request Body:**

```json
{
  "status": "em andamento"
}
```
- `204 No Content`: Status atualizado com sucesso.
- `400 Bad Request`: Status inválido.
- `404 Not Found`: Tarefa não encontrada.
