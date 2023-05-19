from flask import (
    Flask,
    jsonify,
    request)
import requests

class ApiQueue(Flask):
    def __init__(self,ip):
        super().__init__(__name__)
        self.url_panel_desktop = f'http://{ip}:5001/display'
        self.url_panel_smartphone = f'http://{ip}:5003/display'
        self.route('/queue', methods=['GET'])(self.get_queue)
        self.route('/queue', methods=['POST'])(self.emit_ticket)
        self.route('/call', methods=['POST'])(self.call_ticket)
        self.route('/queue', methods=['DELETE'])(self.delete_queue)
        self.queue = []
        self.current_ticket_number = 1

    def get_queue(self):
        return jsonify(self.queue)

    def emit_ticket(self):
        self.current_ticket_number
        name = request.form.get('name')
        document_number = request.form.get('document_number')
        if not name or not document_number:
            return jsonify({'error': 'Name and document number are required'}), 400
        if name in [ticket['name'] for ticket in self.queue] and document_number in [ticket['document_number'] for ticket in self.queue]:
            return jsonify({'error': 'Nome Ou numero do documento já está na fila'}), 400
           
        else:
            ticket = {
                'ticket_number': f'T{self.current_ticket_number}',
                'name': name,
                'document_number': document_number
            }
            self.current_ticket_number += 1
            self.queue.append(ticket)
            return jsonify({'ticket': ticket}), 200

    #Função para chamar uma senha
    def call_ticket(self):
        """
        Função para chamar a próxima senha da fila e mostrar na tela.
        """
        # Verificar se a fila está vazia
        if not self.queue:
            return jsonify({'error': 'A fila está vazia.'}), 404
        # Obter os dados do nome e número do documento do corpo da requisição
        data = request.form
        name = data.get('name')
        document_number = data.get('document_number')
        
        # Procurar o ticket na fila pelo nome
        ticket_index = None
        for i, ticket in enumerate(self.queue):
            if ticket['name'] == name and document_number == ticket['document_number']:
                ticket_index = i
                ticket_number = ticket['ticket_number']
                break
            
        if ticket_index is not None:
            # Remover o ticket da fila
            ticket = self.queue.pop(ticket_index)
            
            # Fazer chamada à outra API para mostrar o conteúdo na tela
            display_response = requests.post(self.url_panel_desktop, json={
                'name': name,
                'document_number': document_number,
                'ticket_number':ticket_number})
            requests.post(self.url_panel_smartphone, json={
                'name': name,
                'document_number': document_number,
                'ticket_number':ticket_number})
            
            if display_response.status_code == 200:
                with open('tickets.txt','a') as file:
                    file.write(f'\nname:{name}/document_number:{document_number}')
                    file.close()
                    
                return jsonify({'message': 'Senha chamada com sucesso e conteúdo mostrado na tela.'}), 200
            else:
                return jsonify({'error': 'Erro ao chamar a senha ou mostrar o conteúdo na tela.'}), 500
        else:
            return jsonify({'error': f'Senha com nome "{name}" não encontrada na fila.'}), 404
        
    def delete_queue(self):
        zerar_fila = request.form.get('zerar_fila')
        reiniciar_contagem = request.form.get('reiniciar_contagem')
        ticket_name = request.form.get('name')
        ticket_document_number = request.form.get('document_number')
        ticket_number = request.form.get('ticket_number')

        if zerar_fila == 'true':
            self.queue = []
            return jsonify({'message': 'Fila de senhas limpa.'}), 200
        elif reiniciar_contagem == 'true':
            self.current_ticket_number = 1
            return jsonify({'message': 'Contagem de senhas reiniciada.'}), 200
        
        elif ticket_name and ticket_document_number and ticket_number:
            for i, ticket in enumerate(self.queue):
                if ticket['name'] == ticket_name and ticket['document_number'] == ticket_document_number and ticket['ticket_number'] == ticket_number:
                    self.queue.pop(i)
                    return jsonify({'message': 'Senha removida da fila.'}), 200
            return jsonify({'error': 'Senha não encontrada na fila.'}), 404
        
        
if __name__ == '__main__':
    app = ApiQueue(ip="localhost")
    app.run(port=5000, debug=True)
# if __name__ == "__main__":

#     serve(app, host="0.0.0.0", port=5000)