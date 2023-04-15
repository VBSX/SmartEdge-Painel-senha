var source = new EventSource('/display');
var previousTicketNumber = ''; // Variável para armazenar o número do ticket anteriormente reproduzido

// Associar a função de atualização ao evento 'message'
source.onmessage = function(event) {   
    
    var contentElement = document.getElementById('content');
    contentElement.innerHTML = '';

    // Dividir o conteúdo da senha chamada em nome e número da senha
    var content = event.data.split(':');
    var name = content[0].trim();
    var ticketNumber = content[1].trim();
    
    // Criar elementos de bloco para exibir o nome e o número da senha
    var nameElement = document.createElement('div');
    var nameDescriptionElement = document.createElement('div');
    nameDescriptionElement.className = 'content-item';
    nameDescriptionElement.textContent = 'Nome: '

    nameElement.className = 'content-item';
    nameElement.id = 'name-content';
    nameElement.textContent = name;
    
    var ticketNumberElement = document.createElement('div');
    var ticketDescriptionElement = document.createElement('div');
    ticketDescriptionElement.className = 'content-item';
    ticketDescriptionElement.textContent= 'Número da Senha: '
    ticketNumberElement.className = 'content-item';
    ticketNumberElement.id = 'ticket-content';
    ticketNumberElement.textContent = ticketNumber;

    // Adicionar o elemento ao elemento de conteúdo
    contentElement.appendChild(nameDescriptionElement)
    contentElement.appendChild(nameElement);
    contentElement.appendChild(document.createElement('br')); // Adicionar uma quebra de linha
    contentElement.appendChild(ticketDescriptionElement);
    contentElement.appendChild(ticketNumberElement);

    // Comparar o número do ticket atual com o número do ticket anteriormente reproduzido
    if (ticketNumber !== previousTicketNumber) {
        var sound = new Howl({
            src: ['/static/bingbong.mp3'],
        });
        previousTicketNumber = ticketNumber; // Atualizar o número do ticket anteriormente reproduzido
        sound.play();
    }
};

// Monitorar o evento 'ended' do elemento de áudio para parar a reprodução quando o som terminar
var audioElement = document.getElementById('audio');
audioElement.addEventListener('ended', function() {
    audioElement.currentTime = 0; // Reiniciar a reprodução para o início
});
