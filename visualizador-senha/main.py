from flask import Flask, request, Response,send_from_directory
from waitress import serve
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

    # Adiciona as configurações de cache no cabeçalho da resposta
    response = Response(generate(), mimetype="text/event-stream")
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Connection'] = 'keep-alive'
    return response

@app.route('/display', methods=['POST'])
def display_content():
    global displayed_content
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
    <!-- Inclua a biblioteca Howler.js -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/howler/2.2.3/howler.min.js"></script>
    <script>
        var audioPlayed = false; // Variável para controlar se o áudio já foi reproduzido

        // Criar um novo EventSource para receber eventos SSE
        var source = new EventSource('/display');

        // Associar a função de atualização ao evento 'message'
        source.onmessage = function(event) {
            var contentElement = document.getElementById('content');
            contentElement.innerHTML = '';

            // Dividir o conteúdo da senha chamada em nome e número da senha
            var content = event.data.split(':');
            var name = content[1].trim();
            name = name.replace("Número da Senha", "");
            var ticketNumber = content[2].trim();
            
            // Criar elementos de bloco para exibir o nome e o número da senha
            var nameElement = document.createElement('div');
            nameElement.className = 'content-item';
            nameElement.textContent = 'Nome: ' + name;
            
            var ticketNumberElement = document.createElement('div');
            ticketNumberElement.className = 'content-item';
            ticketNumberElement.textContent = 'Número da Senha: ' + ticketNumber;

            // Adicionar o elemento ao elemento de conteúdo
            contentElement.appendChild(nameElement);
            contentElement.appendChild(document.createElement('br')); // Adicionar uma quebra de linha
            contentElement.appendChild(ticketNumberElement);


            // Reproduzir o som de chamada apenas se não tiver sido reproduzido ainda
            if (!audioPlayed) {
                var sound = new Howl({
                    src: ['/static/bingbong.mp3'],
                    onend: function() {
                        source.close(); // Fechar a conexão SSE quando o som terminar
                    }
                });
                sound.play();
                audioPlayed = true; // Marcar o áudio como reproduzido
            }
        };

        // Monitorar o evento 'ended' do elemento de áudio para parar a reprodução quando o som terminar
        var audioElement = document.getElementById('audio');
        audioElement.addEventListener('ended', function() {
            audioElement.currentTime = 0; // Reiniciar a reprodução para o início
        });

    </script>
    <script>
    // Função para fazer uma solicitação assíncrona para verificar se uma nova senha foi chamada
    function checkForNewContent() {
        fetch('/display')
        .then(function(response) {
            if (response.ok) {
                return response.text();
            } else {
                throw new Error('Erro na solicitação');
            }
        })
        .then(function(content) {
            // Verificar se o conteúdo da senha chamada foi atualizado
            if (content !== '') {
                // Recarregar a página para atualizar o conteúdo
                location.reload();
            }
        })
        .catch(function(error) {
            console.error(error);
        });
    }

    // Chamar a função de verificação de conteúdo a cada 5 segundos
    setInterval(checkForNewContent, 5000);
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