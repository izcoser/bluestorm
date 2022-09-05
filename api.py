import json
import sqlite3
import string
from flask import Flask
from flask import request
from secrets import choice

queries = {
    "patients": "SELECT * FROM patients",
    "pharmacies": "SELECT * FROM pharmacies",
    "transactions": "SELECT * FROM transactions",
    "create_auth_table": """ CREATE TABLE IF NOT EXISTS auth (
	token_id INTEGER PRIMARY KEY,
	token_hash TEXT NOT NULL);""",
}

conn = sqlite3.connect("backend_test.db", check_same_thread=False)
cur = conn.cursor()

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

# Verifica se o usuário passou o token corretamente nos headers do GET request.
def check_auth(headers: dict) -> bool:
    if "token" not in headers:
        return False

    h = hash(headers["token"])
    return (
        len(conn.execute(f"SELECT * FROM auth WHERE token_hash = '{h}'").fetchall()) > 0
    )


# Endpoint POST para criar um token e ter acesso aos dados.
# O token de autenticação tem 15 caracteres alfanuméricos.
# A hash do token é salva na tabela 'auth' do banco de dados.
@app.post("/create_auth")
def create_auth():
    cur.execute(queries["create_auth_table"])
    conn.commit()
    token = "".join([choice(string.ascii_uppercase + string.digits) for _ in range(15)])
    cur.execute(f"INSERT INTO auth VALUES (NULL, {str(hash(token))})")
    conn.commit()
    return {"token": token}


# Para todos os endpoints abaixo, é necessário
# passar o token nos headers do GET request,
# no formato: "token": "${token}".

# Endpoint para obter os pacientes.
@app.get("/patients")
def list_patients():
    if not check_auth(request.headers):
        return {"erro": "Token de autenticação inválido ou inexistente."}, 401
    patients = []
    for i in cur.execute(queries["patients"]):
        p = {
            "id": i[0],
            "nome": i[1],
            "sobrenome": i[2],
            "dataDeNascimento": i[3],
        }
        patients.append(p)
    return patients


# Endpoint para obter as farmácias.
@app.get("/pharmacies")
def list_pharmacies():
    if not check_auth(request.headers):
        return {"erro": "Token de autenticação inválido ou inexistente."}, 401
    pharmacies = []
    for i in cur.execute(queries["pharmacies"]):
        p = {
            "id": i[0],
            "nome": i[1],
            "cidade": i[2],
        }
        pharmacies.append(p)
    return pharmacies


# Endpoint para obter as transações.
@app.get("/transactions")
def list_transactions():
    if not check_auth(request.headers):
        return {"erro": "Token de autenticação inválido ou inexistente."}, 401
    transactions = []
    for i in cur.execute(queries["transactions"]):
        t = {
            "id": i[0],
            "paciente_id": i[1],
            "farmacia_id": i[2],
            "valor": i[3],
            "data": i[4],
        }
        transactions.append(t)
    return transactions
