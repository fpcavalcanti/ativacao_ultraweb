from flask import Flask, jsonify, request
import json

app = Flask(__name__)

web_service_version = 0.1
web_service_release_date = '22/04/2022'

@app.route("/")
@app.route("/ping")
def req_ping():
    return ({
        'status': 'Ativo',
        'mensagem': 'API executando',
        'versao': web_service_version,
        'data_release': web_service_release_date
    })

@app.route("/do_ativacao", methods=['POST'])
def do_ativacao():

    o_body = request.get_data()
    json_data = json.loads(o_body)

    response_obj = {
        'status': True,
        'received': json_data
    }

    return response_obj