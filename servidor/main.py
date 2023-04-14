from flask import Flask, jsonify, request
import requests
from waitress import serve
app = Flask(__name__)

queue = []
current_ticket_number = 1

@app.route('/queue', methods=['GET'])
def get_queue():
    return jsonify(queue)

@app.route('/queue', methods=['POST'])
def emit_ticket():
    global current_ticket_number
    name = request.form.get('name')
    document_number = request.form.get('document_number')
    if not name or not document_number:
        return jsonify({'error': 'Name and document number are required'}), 400
    ticket = {
        'ticket_number': f'T{current_ticket_number}',
        'name': name,
        'document_number': document_number
    }
    current_ticket_number += 1
    queue.append(ticket)
    return jsonify({'ticket': ticket})

# # Função para chamar uma senha
@app.route('/call', methods=['POST'])
def call_ticket():
    """
    Função para chamar a próxima senha da fila e mostrar na tela.
    """
    global queue

    # Verificar se a fila está vazia
    if not queue:
        return jsonify({'error': 'A fila está vazia.'}), 404

    # Obter os dados do nome e número do documento do corpo da requisição
    data = request.form
    name = data.get('name')
    document_number = data.get('document_number')

    # Procurar o ticket na fila pelo nome
    ticket_index = None
    for i, ticket in enumerate(queue):
        if ticket['name'] == name:
            ticket_index = i
            ticket_number = ticket['ticket_number']
            break

    if ticket_index is not None:
        # Remover o ticket da fila
        ticket = queue.pop(ticket_index)

        # Lógica para chamar o próximo ticket e retornar a resposta
        # ...

        # Fazer chamada à outra API para mostrar o conteúdo na tela
        display_response = requests.post('http://localhost:5001/display', json={'name': name, 'document_number': document_number,
                                                                                'ticket_number':ticket_number})
        if display_response.status_code == 200:
            return jsonify({'message': 'Senha chamada com sucesso e conteúdo mostrado na tela.'}), 200
        else:
            return jsonify({'error': 'Erro ao chamar a senha ou mostrar o conteúdo na tela.'}), 500
    else:
        return jsonify({'error': f'Senha com nome "{name}" não encontrada na fila.'}), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)
# if __name__ == "__main__":

#     serve(app, host="0.0.0.0", port=5000)