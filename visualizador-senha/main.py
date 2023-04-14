from flask import Flask, jsonify, request, Response

app = Flask(__name__)

# Variável global para armazenar o conteúdo da senha chamada
displayed_content = None

@app.route('/display')
def send_content():
    def generate():
        while True:
            # Obtém o conteúdo da senha chamada da variável global
            content = displayed_content

            # Se o conteúdo da senha chamada for atualizado, envie o evento SSE para a página
            if content:
                yield f"data: {content}\n\n"

    return Response(generate(), mimetype="text/event-stream")

@app.route('/display', methods=['POST'])
def display_content():
    global displayed_content
    # Obter os dados do nome, número do documento e número da senha do corpo da requisição
    data = request.json
    name = data.get('name')
    ticket_number = data.get('ticket_number')

    # Atualizar o conteúdo da senha chamada na variável global
    displayed_content = f"Nome: {name} Número da Senha: {ticket_number}"

    # Retornar uma resposta vazia com status 200 para indicar o sucesso
    return '', 200

@app.route('/display/painel')
def painel_exibicao():
    """
    Função para exibir a página inicial.
    """
    return """
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
            </style>
            <script>
                // Função para atualizar o conteúdo da senha chamada na página
                function updateContent(event) {
                    var contentElement = document.getElementById('content');
                    contentElement.innerHTML = event.data;

                    // Reproduzir o som de chamada
                    var audioElement = document.getElementById('audio');
                    audioElement.play();
                }

                
                // Criar um novo EventSource para receber eventos SSE
                var source = new EventSource('/display');

                // Associar a função de atualização ao evento 'message'
                source.onmessage = updateContent;
            </script>
        </head>
        <body>
            <h1>Bem-vindo ao Visualizador de Senhas</h1>
            <p>Conteúdo da Senha Chamada:</p>
            <div id="content"></div>

            <!-- Adicione o elemento de áudio -->
            <audio id="audio" src="bingbong.mp3"></audio>

        </body>
        </html>
    """

if __name__ == '__main__':
    app.run(port=5001, debug=True)
