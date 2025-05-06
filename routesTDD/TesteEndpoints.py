import requests
import json
from login_routes import rotasLoginPost, rotasLoginGetPutGet, rotasLoginDelete
from cadastro_routes import rotasCadastroPost, rotasCadastroGetPutGet, rotasCadastroDelete

# Cabeçalhos comuns (se necessário token ou content-type)
headers = {
    "Content-Type": "application/json",
}

def testaRota(rotas, headers=None):
    headers = headers or {}
    for rota in  rotas:
        try:
            method = rota.get("method")
            url = rota.get("url")
            data = rota.get("data")

            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, json=data, headers=headers)
            elif method == "PUT":
                response = requests.put(url, json=data, headers=headers)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers)
            else:
                print(f"🚫 Método {method} não suportado: {url}")
                continue
        
            status = response.status_code
            try:
                conteudo = response.json()
                if conteudo == '':
                   continue

            except json.JSONDecodeError:
                print(f"❌ Método: {method} Erro no formato da resposta JSON em {url}:")
                continue
            except requests.exceptions.RequestException as err:
                print(f"Erro de conexão: {err}")
                continue

            print(f"{'✅' if status < 400 else '❌'} {method} {url} - Status: {status}")
            if data is not None:
                print(f"Dados recebidos para atualização: {json.dumps(data, indent=4)}")
           
            if isinstance(conteudo, dict):
                mensagem = conteudo.get("mensagem", "")
                
                if "qtdAtu" in conteudo:
                    # Se dict tem atributo qtdAtu atualização OK
                    print(f"🔍 Resposta {status} - linhas atualizadas: {conteudo['qtdAtu']}\n")
                elif isinstance(mensagem, str):
                    print(f"ℹ️ ---------------------------------------------------------")
                    for linha in mensagem.split("!"):
                        if linha.strip():
                            print(linha.strip())
                    print(f"-----------------------------------------------------------ℹ️")
            else:
                print(f"🔍 Resposta Select:\n{json.dumps(conteudo, indent=2, ensure_ascii=False)}")

        except Exception as e:
            print(f"❌ ERRO ao acessar {url}: {str(e)}")


print("✅ Validando rotas...\n")


#testaRota(rotasCadastroDelete)
#testaRota(rotasCadastroPost)
#testaRota(rotasCadastroGetPutGet)

#testaRota(rotasLoginDelete)
testaRota(rotasLoginPost)
testaRota(rotasLoginGetPutGet)



