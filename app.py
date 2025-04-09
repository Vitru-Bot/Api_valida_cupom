from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

app = Flask(__name__)

# Lista dos cupons
base_codigo = [
"5F7JQ3",
"K4Z9A7",
"P0UWD8",
"H3KNW1",
"X9J3L8",
"N2Z6Q3",
"T1PLK3",
"Y5VRD0",
"F8W4U3",
"B6MDY6",
"C7XEU7",
"S3JDZ9",
"A5WPH8",
"J9BLM5",
"M1CNE8",
"Q2RTV1",
"G0YKQ9",
"V8FJZ2",
"R2XKN7",
"D9GHY3",
"E4LWP8",
"L7PZQ5",
"Z0KRT1",
"U3XDY6",
"O2NVR4",
"W8FKL9",
"I1QMC5",
"K3NVR4",
"Y9JLD3",
"N6FPQ5",
"P5RKZ6",
"F2MWL7",
"H7ZHQ2",
"T9NCD6",
"P3UZY9",
"C5RWN3",
"J2LGV8",
"A8ZPD4",
"F6RLK2",
"X0DYS4",
"L9KMD7",
"B7QFL6",
"Z4JXU5",
"R0CWP3",
"O5SVK9",
"G8LFY8",
"W2QCJ3",
"E1KZL6",
"S6MVK6",
"D4HYZ1",
"U5LQC9",
"Q1RWF7",
"V3PJD5",
"M8WZQ3",
"I7NLK2",
"Z2XTC0",
"R4JKW6",
"T0CMP9",
"F3RLW7",
"P9QHD8",
"H5JNZ7",
"S1VMC8",
"A7RLG5",
"J4QKU1",
"K2YPD4",
"N8VXW6",
"B0CMK9",
"C3RJL2",
"E5HQM0",
"X7NZR8",
"Y6QFD6",
"D9MRP5",
"L3PJK4",
"V0CLW3",
"G5RMZ7",
"U9XYN4",
"O4JVK2",
"W3DQY7",
"I6PZH8",
"F1RLJ3",
"T2XRK9",
"J5YNV6",
"K7PDG5",
"S0QLW0",
"M4NKY8",
"H2VXJ3",
"N5QKD7",
"A9JMP5",
"G0WFL6",
"R3CKZ8",
"L1DHV3",
"C8QMW4",
"X5PVJ4",
"Z9LRT9",
"B3NYD2",
"Y7XKP5",
"U2RFL6",
"E0WDK8",
"I9MLZ5",
"W4PCD9",
"Q7VLN2",
"D3YKR1",
"V6RQJ7",
"N0XWF3",
"K5JZL6",
"M3CPK7",
"P8LFD9",
"A1NXY2",
"J2RVW8",
"T4PQZ3",
"B7KLM4",
"P6XRD5",
"H0QFZ8",
"C4LKJ2",
"S9ZWN3",
"K2RLD7",
"Y6QPJ0",
"R1FVC5",
"O8NZP6",
"G4YKV2",
"J3LZW5",
"U7QMJ8",
"A5KNY3",
"T9DVL7",
"M0QXH4",
"L6RPC2",
"E8ZYW2",
"N4FVJ5",
"W1JMK7",
"Z5YLK9",
"Q0PKD8",
"V2RFX4",
"F8ZQY3",
"P3JWZ5",
"K7DXC6",
"S5LYP7",
"B9NWD2",
"C1QZL3",
"R0VFL6",
"H4WMR8",
"I3GKV5",
"O7JKZ6",
"D2PRL9",
"A6LDY4",
"J5WXZ2",
"G0QVD9",
"Y8FKC3",
"Z2LNR6",
"V5RWJ7",
"U9ZVG2",
"E4KDN7",
"M6RLC1",
"P1JMF8",
"A7QXV3",
"N3FPL5",
"T0DLZ6",
"B5MKV8",
"K8RQW4",
"J2XYZ9",
"Q7LCF1",
"H6MDZ8",
"S4QRP4",
"F9GKC5",
"D8WLV3",
"O1ZNR7",
"G3PMD2",
"L7JKX5",
"W2VLC9",
"R0ZQP6",
"Y3KMW7",
"N9FJZ6",
"E6RXY2",
"B1PQD4",
"U5WXN9",
"V4JFK3",
"P8LGR8",
"T9KLM6",
"M2ZHJ3",
"Z7RLP7",
"S0NYV2",
"K1JQC8",
"D4WFJ7",
"C6RPK4",
"L9ZMK5",
"F3NLW8",
"I8JXZ9",
"Q2VYD5",
"O9XGK2",
"H5WQL7",
"Y0JFV3",
"X8ZKD1",
"W3RJC9",
"R7LVH8",
"N0YKZ6",
"U2PQZ4",
"E5MLC3",
"T6KRV9",
"Z8JXP7",
"G4VYL5",
"A1WKJ2"
]

# Autenticação com a planilha do sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)
client = gspread.authorize(creds)

# Acesse a planilha e aba
sheet = client.open("codigos_usuarios").worksheet("codigos")  # coloque o nome da aba da planilha

# Função para salvar um registro na planilha
def salvar_no_google_sheets(codigo, telefone):
    datahora = (datetime.utcnow() - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([codigo, telefone, datahora])
    return datahora

# Função para verificar se o cupom existe na planilha
def codigo_ja_usado(codigo):
    registros = sheet.get_all_records()
    for r in registros:
        if str(r['Codigo']) == codigo:
            return r
    return None

# Rota da API
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
