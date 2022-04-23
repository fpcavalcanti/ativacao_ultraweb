from flask import Flask, jsonify, request

app = Flask(__name__)

web_service_version = 0.1
web_service_release_date = '22/04/2022'

@app.route("/")
@app.route("/ping")
def req_ping():
    return jsonify({ 'status': 'Ativo', 'mensagem': f'Web service executando v:{web_service_version} - Release: {web_service_release_date}'})

@app.route("/do_ativacao", methods=['POST'])
def do_ativacao():
    json_body = request.get_json(force=True)
    print(json_body)
    return jsonify({'status': True, 'received': json_body})