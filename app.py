from flask import Flask, request, jsonify
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

app = Flask(__name__)

# Lista de códigos válidos
base_codigo = [
    "4115451",
    "4145454",
    "8558255",
    "8948941",
    "8794756"
]

# Autenticação com Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)
client = gspread.authorize(creds)

# Acesse a planilha e aba
sheet = client.open("codigos_usuarios").worksheet("codigos")  # Use o nome correto da aba!

# Função para salvar novo registro
def salvar_no_google_sheets(codigo, telefone):
    datahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([codigo, telefone, datahora])
    return datahora

# Função para verificar se código já foi usado
def codigo_ja_usado(codigo):
    registros = sheet.get_all_records()
    for r in registros:
        if str(r['Codigo']) == codigo:
            return r
    return None

# Rota principal da API
@app.route('/validar-codigo', methods=['POST'])
def validar_codigo():
    dados = request.json
    codigo = dados.get("Codigo")
    telefone = dados.get("Telefone")

    if not codigo or not telefone:
        return jsonify({"status": "Erro", "mensagem": "Informe o código e o telefone."})

    if codigo not in base_codigo:
        return jsonify({
            "status": "Nao_encontrado",
            "mensagem": "Código não identificado."
        })

    registro = codigo_ja_usado(codigo)
    if registro:
        return jsonify({
            "status": "Codigo_ja_utilizado",
            "mensagem": "Este código já foi usado.",
            "utilizado_por": registro
        })

    datahora = salvar_no_google_sheets(codigo, telefone)
    return jsonify({
        "status": "Sucesso",
        "mensagem": "Código registrado com sucesso.",
        "registro": {
            "codigo": codigo,
            "telefone": telefone,
            "data_hora": datahora
        }
    })

# Execução
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 11000))
    app.run(debug=True, host='0.0.0.0', port=port)
