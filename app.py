import json

from flask import Flask, request

from models import CSNRequest

from threading import Timer

import datetime

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
    # ['close', 'auto_close', 'sign']
    if json_data['event']['name'] in ['sign']:
        #     proc aqui o armazenamento da requisicao
        print('persistir req')
        req = CSNRequest.create(objeto=json_data)
        print(req)

        thread = Timer(2, run_ativacao, ([req]))
        thread.start()
    else:
        print('retorno sem persistir')

    print(f'requisicao finalizada em: {datetime.datetime.now()}')
    return {'status': True}

def run_ativacao(args):
    print(f'ativacao executada pós retorno web em: {datetime.datetime.now()}')
    print(f'executar codigo: {args}')

    # req = CSNRequest.get(CSNRequest.codigo == args).get()
    #
    # print(f'Nome da empresa: {req.objeto["event"]["data"]["user"]["name"]}')