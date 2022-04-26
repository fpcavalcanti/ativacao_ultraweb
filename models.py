import datetime
import json

from peewee import *

mysql_db = MySQLDatabase('db_producao', user='root', password='qwerty',
                         host='localhost', port=3306)

class BaseModel(Model):

    class Meta:
        database = mysql_db

class ContaCliente(BaseModel):
    contacliente_id = IntegerField(primary_key=True, unique=True)
    contacliente_nomefantasia = CharField()
    contacliente_cnpj = CharField()
    contacliente_hashcode = CharField()

    class Meta:
        table_name = 'contacliente'

class Ativacao(BaseModel):
    ativacao_id = IntegerField(primary_key=True, unique=True)
    ativacao_lavanderia_id_fk = IntegerField()
    ativacao_data_ativado = DateField()
    ativacao_data_inativado = DateField()
    ativacao_nomecliente = CharField()
    ativacao_nomecontato = CharField()
    ativacao_numerocontato = CharField()
    ativacao_emailcontato = CharField()

class Lavanderia(BaseModel):
    lavanderia_id = IntegerField(primary_key=True, unique=True)
    lavanderia_nome = CharField()
    lavanderia_servicoativo = CharField()
    lavanderia_contacliente_id_fk = IntegerField()
    lavanderia_numero = IntegerField()
    lavanderia_telefone = CharField()
    lavanderia_inicio_jornada = TimeField()
    lavanderia_final_jornada = TimeField()
    lavanderia_tempomedio_processo = IntegerField()
    lavanderia_sinc_custo_quimico = CharField()
    lavanderia_custoagua = DoubleField()
    lavanderia_custoenergia = DoubleField()
    lavanderia_custovapor = DoubleField()
    lavanderia_custokg = DoubleField()
    lavanderia_tiposupervisao = IntegerField()
    lavanderia_data_cadastro = DateField()

    def get_conta(self):
        if not self.lavanderia_contacliente_id_fk is None:
            return ContaCliente.get(ContaCliente.contacliente_id == self.lavanderia_contacliente_id_fk)
        else:
            return None

    def is_servico_ativo(self):
        lAtv = Ativacao.select(Ativacao.ativacao_id).where(
            Ativacao.ativacao_lavanderia_id_fk == self.lavanderia_id & Ativacao.ativacao_data_inativado.is_null()
        )
        return len(lAtv) == 1

    def get_plano(self):
        l_eqp = Equipamento.select(Equipamento.equipamento_id).where(Equipamento.equipamento_lavanderia_id_fk == self.lavanderia_id)
        l_usr = UsuarioLavanderia.select(UsuarioLavanderia.usuariolavanderia_id).where(UsuarioLavanderia.usuariolavanderia_lavanderia_id_fk == self.lavanderia_id & UsuarioLavanderia.usuariolavanderia_usuario_id_fk != 1)

        token_eqp = 1
        token_usr = 1

        qtd_eqp = len(l_eqp)
        qtd_usr = len(l_usr)

        match qtd_eqp:
            case qtd if 0 == qtd < 4:
                token_eqp = 1
            case qtd if 4 == qtd < 6:
                token_eqp = 2
            case qtd if 7 <= qtd:
                token_eqp = 3

        match qtd_usr:
            case qtd if 0 == qtd <= 2:
                token_usr = 1
            case qtd if 2 < qtd <= 3:
                token_usr = 2
            case qtd if 4 <= qtd:
                token_usr = 3

        if token_eqp > token_usr:
            token_plano = token_eqp
        else:
            token_plano = token_usr

        plano = {'nome': 'Basic', 'valor': 34.38}

        match token_plano:
            case token if 1 == token:
                plano = {'nome': 'Basic', 'valor': 34.38, 'limit_usuario': 2, 'limite_eqp': 3}
            case token if 2 == token:
                plano = {'nome': 'Standard', 'valor': 68.88, 'limit_usuario': 3, 'limite_eqp': 6}
            case token if 3 == token:
                plano = {'nome': 'Professional', 'valor': 114.88, 'limit_usuario': 6, 'limite_eqp': 10}

        return plano


class UsuarioLavanderia(BaseModel):
    usuariolavanderia_id = IntegerField(primary_key=True, unique=True)
    usuariolavanderia_usuario_id_fk = IntegerField()
    usuariolavanderia_lavanderia_id_fk = IntegerField()
    usuariolavanderia_data_cadastro = DateField()

    class Meta:
        table_name = 'usuariolavanderia'

class SystemUser(BaseModel):
    id = IntegerField(primary_key=True, unique=True)
    name = CharField()
    login = CharField()
    password = CharField()

    class Meta:
        table_name = 'system_user'

class Equipamento(BaseModel):
    equipamento_id = IntegerField(primary_key=True, unique=True)
    equipamento_nome = CharField()
    equipamento_imei = CharField()
    equipamento_equipamentomodo_id_fk = IntegerField()
    equipamento_identificacao = IntegerField()
    equipamento_lavanderia_id_fk = IntegerField()

    def get_modo(self):
        return "Datamapper" if self.equipamento_equipamentomodo_id_fk == 6 else "Webtouch"

class JSONField(TextField):
    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)

class CSNRequest(BaseModel):
    codigo = IntegerField(primary_key=True, unique=True)
    objeto = JSONField()
    data_requisicao = DateTimeField(default=datetime.datetime.now())
    status_proc = IntegerField(default=0)

    class Meta:
        table_name = 'csn_request'