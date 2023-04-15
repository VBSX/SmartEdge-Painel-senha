from flask import Flask, request, render_template, redirect, url_for,send_from_directory
import os
import requests

app = Flask(__name__)
app.static_folder = 'static'
# Variável global para armazenar o conteúdo da senha chamada
displayed_content = None
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1 MB

#Rota para servir o arquivo de imagem do favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

def queue_add(name, document):
    payload=f'name={name}&document_number={document}'
    url = "http://127.0.0.1:5000/queue"
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    response_server = requests.request("POST", url, headers=headers, data=payload)
    if response_server:
        
        return 200

@app.route('/queue', methods=['GET', 'POST'])
def view_queue():
    url = "http://127.0.0.1:5000/queue"
    response = requests.request("GET", url)
    queue_data = response.json() 

    return render_template('queue.html', queue_data=queue_data)


@app.route('/call', methods=['POST'])
def call_in_panel_view():

    name = request.form['name']
    ticket_number = request.form['document_number']
    url = "http://127.0.0.1:5000/call"

    payload=f'name={name}&document_number={ticket_number}'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    
    return redirect('/queue') 


@app.route('/', methods=['GET', 'POST'])
def index():
    
    """
    Configuração da página inicial(Index)
    
    """
    if request.method == 'POST':
        nome = request.form['nome']
        documento = request.form['documento']
        # Lógica para colocar os dados na fila
        queue_add(nome,documento)
        return render_template('index.html', sucesso=True, nome=nome)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5002, debug=True)
    
# if __name__ == "__main__":

#     serve(app, host="0.0.0.0", port=5001)