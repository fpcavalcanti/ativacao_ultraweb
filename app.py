from flask import Flask, jsonify

app = Flask(__name__)

web_service_version = 0.1

@app.route("/")
@app.route("/ping")
def req_ping():
    return jsonify({ 'status': 'Ativo', 'mensagem': f'Web service executando v:{web_service_version}'})

@app.route("/do_ativa", methods=['GET', 'POST'])
def do_ativacao():
    return jsonify({'status': True, 'received': 'ok'})