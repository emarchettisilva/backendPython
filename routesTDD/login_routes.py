rotasLoginPost = [
    {
        "method": "POST", 
           "url": "http://localhost:5000/api/usuario",   
          "data": {"codUsuarioCPF": "11111111111", 
                   "nomUsuario": "José Antônio",
                   "desEmail": "jose@gmail.com",
                   "idtAdministrador": False,
                   "idtFuncionario": True,
                   "idtGestor": True,
                   "idtAtivo": True
             }
    },
    {
        "method": "POST", 
           "url": "http://localhost:5000/api/usuario",   
          "data": {"codUsuarioCPF": "", 
                   "nomUsuario": "",
                   "desEmail": "",
                   "idtAdministrador": "",
                   "idtFuncionario": "",
                   "idtGestor": "",
                   "idtAtivo": ""
             }
    }
]

rotasLoginGetPutGet = [
    #codUsuarioCPF
    {
        "method": "GET",
           "url": "http://localhost:5000/api/loginAcesso/11111111111"
    },
    {
        "method": "PUT", "url": "http://localhost:5000/api/alterarSenha",
          "data": {"codUsuarioCPF": "11111111111", 
                   "desSenha": "123456"
                  }
    },    
    {
        "method": "POST",
           "url": "http://localhost:5000/api/loginAcesso",
          "data": {"codUsuarioCPF": "50087622654", 
                   "desSenha": "123456"
                  }
    },

    {
        "method": "PUT",
           "url": "http://localhost:5000/api/usuario",
          "data": {"nomUsuario": "José Antônio Alterado",
                   "desEmail": "jose@gmail.com",
                   "idtAdministrador": False,
                   "idtFuncionario": True,
                   "idtGestor": True,
                   "idtAtivo": True,
                   "codUsuarioCPF": "11111111111"
                  }
    }  
]

rotasLoginDelete = [
]