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
