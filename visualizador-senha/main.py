from flask import Flask, request, Response,send_from_directory,render_template, url_for
import os
from time import sleep
app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1 MB

#Rota para servir o arquivo de imagem do favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/display')
def send_content():
    def generate():
        while True:
            # Obtém o conteúdo da senha chamada da variável global
            content = f'{name}:{ticket_number}'
            sleep(1)
            yield f"data: {content}\n\n"
    sleep(0.1)
    # Adiciona as configurações de cache no cabeçalho da resposta
    response = Response(generate(), mimetype="text/event-stream")
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Connection'] = 'keep-alive'
    return response

static_dir = '/static'

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(static_dir, filename)

@app.route('/display', methods=['POST'])
def display_content():

    global name
    global ticket_number
    # Obter os dados do nome, número do documento e número da senha do corpo da requisição
    data = request.json
    name = data.get('name')
    ticket_number = data.get('ticket_number')

    # Atualizar o conteúdo da senha chamada na variável global


    #Retornar uma resposta vazia com status 200 para indicar o sucesso
    return '', 200

@app.route('/display/painel')
def painel_exibicao():
    """
    Função para exibir a página inicial.
    """

    return render_template('painel_exibicao.html')

if __name__ == '__main__':
    app.run(port=5001, debug=True)

# if __name__ == "__main__":

#     serve(app, host="0.0.0.0", port=5001)