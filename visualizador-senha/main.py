from flask import Flask, request, Response,send_from_directory,render_template
from waitress import serve
from time import sleep
app = Flask(__name__)

# Variável global para armazenar o conteúdo da senha chamada
displayed_content = None
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1 MB

@app.route('/display')
def send_content():
    def generate():
        while True:
            # Obtém o conteúdo da senha chamada da variável global
            content = f'{name}:{ticket_number}'
            yield f"data: {content}\n\n"

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
    global displayed_content
    global name
    global ticket_number
    # Obter os dados do nome, número do documento e número da senha do corpo da requisição
    data = request.json
    name = data.get('name')
    ticket_number = data.get('ticket_number')

    # Atualizar o conteúdo da senha chamada na variável global
    displayed_content = f"Nome: {name} Número da Senha: {ticket_number}"

    #Retornar uma resposta vazia com status 200 para indicar o sucesso
    return '', 200


@app.route('/display/painel')
def painel_exibicao():
    """
    Função para exibir a página inicial.
    """

    return """

<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
        }
        h1 {
            color: #007BFF;
        }
        p {
            color: #212529;
        }
        #content {
            margin-top: 50px;
        }
        .content-item {
            margin-bottom: 10px;
        }
    </style>
    <!-- Inclua a biblioteca Howler.js 
    <script src="https://cdnjs.cloudflare.com/ajax/libs/howler/2.2.3/howler.min.js"></script> -->
    <script src="/static/painel_exibicao.js">
    </script>

</head>
<body>
    <h1>Bem-vindo ao Visualizador de Senhas</h1>
    <p>Conteúdo da Senha Chamada:</p>
    <div id="content"></div>

    <!-- Adicione o elemento de áudio -->
    <audio id="audio" src="/static/bingbong.mp3"></audio>

</body>
</html>

"""

if __name__ == '__main__':
    app.run(port=5001, debug=True)
# if __name__ == "__main__":

#     serve(app, host="0.0.0.0", port=5001)