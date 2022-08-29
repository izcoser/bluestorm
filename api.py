import json
from flask import Flask
from flask import request
import sqlite3

queries = {
    'patients': 'select * from patients',
    'pharmacies': 'select * from pharmacies',
    'transactions': 'select * from transactions',
}

conn = sqlite3.connect('backend_test.db', check_same_thread=False)
cur = conn.cursor()

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.get("/patients")
def list_patients():
    patients = []
    for i in cur.execute(queries['patients']):
        p = {
            'id': i[0],
            'nome': i[1],
            'sobrenome': i[2],
            'dataDeNascimento': i[3],
        }
        patients.append(p)
    return patients
    
@app.get("/pharmacies")
def list_pharmacies():
    pharmacies = []
    for i in cur.execute(queries['pharmacies']):
        p = {
            'id': i[0],
            'nome': i[1],
            'cidade': i[2],
        }
        pharmacies.append(p)
    return pharmacies

@app.get("/transactions")
def list_transactions():
    transactions = []
    for i in cur.execute(queries['transactions']):
        t = {
            'id': i[0],
            'paciente_id': i[1],
            'farmacia_id': i[2],
            'valor': i[3],
            'data': i[4]
        }
        transactions.append(t)
    return transactions