import json

from flask import Flask, request

from models import CSNRequest

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

    if json_data['event']['name'] in ['close', 'auto_close', 'sign']:
        #     proc aqui o armazenamento da requisicao
        print('persistir req')
        CSNRequest.create(objeto=json_data)
    else:
        print('retorno sem persistir')

    return {'status': True}