# routes/login_routes.py
from flask import Blueprint, request
from db import Db, Mode
from . import valida

import bcrypt

# Definindo o blueprint
login_bp = Blueprint("login_bp", __name__)


#Validar login (CPF) de acesso do usuario
@login_bp.route("/loginAcesso/<codUsuarioCPF>", methods=["GET"])
def get_loginAcesso(codUsuarioCPF):
    mensagem = valida.CPF(codUsuarioCPF)
    if mensagem != '':
        return {'mensagem': mensagem}
        
    sql = """
        SELECT desSenha,
               idtAtivo
          FROM Usuario
         WHERE codUsuarioCPF = %s
    """
    params = (codUsuarioCPF,)

    db = Db()
    try:
        usuarios = db.execSql(sql, params, Mode.SELECT)
    except Exception as e:
        return db.getErro()
        
    if len(usuarios) == 0:
        return {"mensagem": "Usuario não encontrado!"}
    
    usuario = usuarios[0]
    desSenha = usuario[0]
    idtAtivo = usuario[1]
    
    if not idtAtivo:
        return {"mensagem": "Usuario não está ativo!"}
    
    idtTemSenha = desSenha is not None

    return {"idtTemSenha": idtTemSenha}
  

#Validar senha de acesso do usuario
@login_bp.route("/loginAcesso", methods=["POST"])
def post_login_acesso():
    data = request.json
    codUsuarioCPF = data.get("codUsuarioCPF")
    desSenhaInfo = data.get("desSenha")
    
    mensagem = valida.CPF(codUsuarioCPF)
    mensagem += valida.desSenha(desSenhaInfo)
    if mensagem != '':
        return {'mensagem': mensagem}

    sql = """
        SELECT nomUsuario,
               desSenha,
               idtAdministrador,
               idtFuncionario,
               idtGestor,
               idtAtivo
          FROM Usuario
         WHERE codUsuarioCPF = %s
    """
    params = (codUsuarioCPF,)
    db = Db()
    try:
        resultado = db.execSql(sql, params, Mode.SELECT)
    except Exception as e:
        return db.getErro()

    if not resultado: 
        return {"mensagem": "Usuario não encontrado!"}
    
    usuario = resultado[0]
    
    nomUsuario = usuario[0]
    desSenha = usuario[1]
    idtAdministrador = usuario[2]
    idtFuncionario = usuario[3]
    idtGestor = usuario[4]
    idtAtivo = usuario[5]
    
    if not idtAtivo:
        return {"mensagem": "Usuario não está ativo!"}
    
    if desSenha is not None:
        desSenhaInfoBytes = desSenhaInfo.encode('utf-8')
        desSenhaBytes = desSenha.encode('utf-8')  
        if not bcrypt.checkpw(desSenhaInfoBytes, desSenhaBytes):
            return {"mensagem": "Usuário ou senha inválidos!"}

    usuario_formatado = []

    usuario_formatado.append({
        "codUsuarioCPF" : codUsuarioCPF,
        "nomUsuario": nomUsuario,
        "idtAdministrador": idtAdministrador,
        "idtFuncionario": idtFuncionario,
        "idtGestor": idtGestor
    })

    return usuario_formatado


# Rota para registrar usuário. A senha é informada somente 1o acesso.
@login_bp.route("/usuario", methods=["POST"])
def post_usuario():
    data = request.json
    codUsuarioCPF    = data.get('codUsuarioCPF')
    nomUsuario       = data.get('nomUsuario')
    desEmail         = data.get('desEmail')
    idtAdministrador = data.get('idtAdministrador')
    idtFuncionario   = data.get('idtFuncionario')
    idtGestor        = data.get('idtGestor')
        
    mensagem = valida.CPF(codUsuarioCPF)
    mensagem += valida.nomUsuario(nomUsuario)
    mensagem += valida.desEmail(desEmail)
    mensagem += valida.idtPapel(idtAdministrador, idtFuncionario, idtGestor)
    
    if mensagem != '':
        return {'mensagem': mensagem}

    sql = """
        INSERT INTO Usuario 
           (codUsuarioCPF, nomUsuario, desEmail, 
            idtAdministrador, idtFuncionario, idtGestor,
            idtAtivo )
        VALUES (%s, %s, %s, %s, %s, %s, True)
    """
    params = (codUsuarioCPF, nomUsuario, desEmail,  
              idtAdministrador, idtFuncionario, idtGestor,)

    try: 
        db = Db() 
        return db.execSql(sql, params)
    except Exception as e:
        return db.getErro()

# Rota para alterar usuário
@login_bp.route("/usuario", methods=["PUT"])
def put_usuario():
    data = request.json
    codUsuarioCPF    = data.get('codUsuarioCPF')
    nomUsuario       = data.get('nomUsuario')
    desEmail         = data.get('desEmail')
    idtAdministrador = data.get('idtAdministrador')
    idtFuncionario   = data.get('idtFuncionario')
    idtGestor        = data.get('idtGestor')
    idtAtivo         = data.get('idtAtivo')
    
    mensagem = valida.CPF(codUsuarioCPF)
    mensagem += valida.nomUsuario(nomUsuario)
    mensagem += valida.desEmail(desEmail)
    mensagem += valida.idtPapel(idtAdministrador, idtFuncionario, idtGestor)
    mensagem += valida.idtAtivo(idtAtivo)
    if mensagem != '':
        return {'mensagem': mensagem}
    
    sql = """
        UPDATE Usuario 
           SET nomUsuario = %s,
               desEmail = %s,
               idtAdministrador = %s,
               idtFuncionario = %s,
               idtGestor = %s,
               idtAtivo = %s
         WHERE codUsuarioCPF = %s
    """
    params = (nomUsuario, desEmail, idtAdministrador, 
              idtFuncionario, idtGestor, idtAtivo, codUsuarioCPF,)

    db = Db()
    try:
        return db.execSql(sql, params)
    except Exception as e:
        return db.getErro()

         
# Rota para alterar a senha
@login_bp.route("/alterarSenha", methods=["PUT"])
def put_alterarSenha():
    data = request.json
    codUsuarioCPF = data.get('codUsuarioCPF')
    desSenha      = data.get('desSenha')
 
    mensagem = valida.CPF(codUsuarioCPF)
    mensagem += valida.desSenha(desSenha)
    if mensagem != '':
        return {'mensagem': mensagem}
       
    # Gerar hash da senha
    desSenhaCripto = bcrypt.hashpw(desSenha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    sql = """
        UPDATE Usuario 
           SET desSenha = %s
         WHERE codUsuarioCPF = %s
    """
    params = (desSenhaCripto, codUsuarioCPF,)
    try:
        db = Db()
        return db.execSql(sql, params)
    except Exception as e:
        return db.getErro()
    