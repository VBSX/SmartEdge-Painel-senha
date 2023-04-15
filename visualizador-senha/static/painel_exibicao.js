
// setTimeout(function() {
//     // Código que será executado após o atraso de 1 segundo
//     contentElement.innerHTML = '';
//     audioPlayed = false;
// }, 1000);
// // Criar um novo EventSource para receber eventos SSE
// var source = new EventSource('/display');

// // Associar a função de atualização ao evento 'message'
// source.onmessage = function(event) {    
//     var contentElement = document.getElementById('content');
//     contentElement.innerHTML = '';

//     // Dividir o conteúdo da senha chamada em nome e número da senha
//     var content = event.data.split(':');
//     var name = content[0].trim();
//     var ticketNumber = content[1].trim();
    
//     // Criar elementos de bloco para exibir o nome e o número da senha
//     var nameElement = document.createElement('div');
//     nameElement.className = 'content-item';
//     nameElement.textContent = 'Nome: ' + name;
    
//     var ticketNumberElement = document.createElement('div');
//     ticketNumberElement.className = 'content-item';
//     ticketNumberElement.textContent = 'Número da Senha: ' + ticketNumber;

//     // Adicionar o elemento ao elemento de conteúdo
//     contentElement.appendChild(nameElement);
//     contentElement.appendChild(document.createElement('br')); // Adicionar uma quebra de linha
//     contentElement.appendChild(ticketNumberElement);
// };

var timeoutId; // Variável para armazenar o ID do timeout

// Criar um novo EventSource para receber eventos SSE
var source = new EventSource('/display');

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
    nameElement.className = 'content-item';
    nameElement.textContent = 'Nome: ' + name;
    
    var ticketNumberElement = document.createElement('div');
    ticketNumberElement.className = 'content-item';
    ticketNumberElement.textContent = 'Número da Senha: ' + ticketNumber;

    // Adicionar o elemento ao elemento de conteúdo
    contentElement.appendChild(nameElement);
    contentElement.appendChild(document.createElement('br')); // Adicionar uma quebra de linha
    contentElement.appendChild(ticketNumberElement);
    source.removeEventListener('message', arguments.callee);
};


// // Limpar o timeout anterior, se existir
// clearTimeout(timeoutId);
// // Configurar um novo timeout de 1 segundo para limpar o conteúdo
// timeoutId = setTimeout(function() {
// }, 1000);