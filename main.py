from flask import Flask, request, render_template_string
import os
import datetime

app = Flask(__name__)
dados_atendimentos = []

HTML_DASHBOARD = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Dashboard UFit - EvoTalks</title>
    <style>
        body { background-color: #000; color: #fff; font-family: sans-serif; margin: 0; padding: 20px; }
        .header { display: flex; align-items: center; justify-content: space-between; border-bottom: 4px solid #FFD200; padding-bottom: 10px; margin-bottom: 30px; }
        .logo { color: #FFD200; font-size: 24px; font-weight: bold; }
        .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
        .card { background: #1a1a1a; padding: 20px; border-radius: 10px; border-left: 8px solid #FFD200; }
        .card h3 { margin: 0; color: #ccc; font-size: 14px; text-transform: uppercase; }
        .card p { margin: 10px 0 0; font-size: 32px; color: #FFD200; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; margin-top: 30px; background: #111; }
        th { background: #FFD200; color: #000; padding: 12px; text-align: left; }
        td { padding: 12px; border-bottom: 1px solid #333; font-size: 14px; }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">UFIT ACADEMIA - DASHBOARD EVOTALKS</div>
        <div style="color: #FFD200;">Status: Online</div>
    </div>
    <div class="cards">
        <div class="card">
            <h3>Total de Atendimentos</h3>
            <p>{{ total }}</p>
        </div>
        <div class="card">
            <h3>Ultima Atualizacao</h3>
            <p style="font-size: 18px;">{{ ultima }}</p>
        </div>
    </div>
    <h2>Log de Atendimentos (Tempo Real)</h2>
    <table>
        <thead><tr><th>Hora</th><th>Dados</th></tr></thead>
        <tbody>
            {% for item in lista %}
            <tr><td>{{ item.hora }}</td><td>{{ item.conteudo }}</td></tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

@app.route('/')
def index():
    total = len(dados_atendimentos)
    ultima = dados_atendimentos[-1]['hora'] if dados_atendimentos else "Aguardando..."
    return render_template_string(HTML_DASHBOARD, total=total, ultima=ultima, lista=reversed(dados_atendimentos))

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.json
    agora = datetime.datetime.now().strftime("%H:%M:%S")
    dados_atendimentos.append({"hora": agora, "conteudo": str(payload)})
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
