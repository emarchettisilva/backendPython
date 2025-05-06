import datetime 

def data(data):
    if data is None:
        return f"Data não informada!"
    elif isinstance(data, str):
        try:
            datetime.strptime(data, '%Y-%m-%d').date()
            return ''
        except:
            return f"Data {data} inválida!"
 

def CPF(codCPF):
    if not isinstance(codCPF, str):
        return f"CPF tipo {type(codCPF)} inválido: valor não é uma string!"

    cpf = codCPF.strip()

    if len(cpf) != 11:
        return "Quantidade de dígitos do CPF diferente de 11!"
    
    if not cpf.isdigit():
        return "CPF possui caracteres não numéricos!"
    
    return ''

def desSenha(desSenha):
    if len(desSenha) >= 4:
        return ''
    else:
        return "A senha tem de ter pelo menos 4 caracteres!"
   
def nomUsuario(nomUsuario):
    if nomUsuario is not None and len(nomUsuario) > 0:
        return ''
    else:
        return 'Nome do usuário é obrigatório!'
    
def desEmail(desEmail):
    if desEmail is not None and len(desEmail) > 0:
        return ''
    else:
        return 'E-mail do usuario é obrigatório!'
      
def idtPapel(idtAdministrador, idtFuncionario, idtGestor):
    if idtAdministrador or idtFuncionario or idtGestor:
        return ''
    else:  
        return "Tipo de usuário tem estar associado a no mínimo um papel!"

def idtAtivo(idtAtivo):
    if idtAtivo is not None and isinstance(idtAtivo, bool):
        return ''
    else:
        return "Indicador de usuario ativo/inativo inválido!"
  
