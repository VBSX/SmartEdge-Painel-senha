from flask import (
    Flask,
    request,
    render_template,
    redirect,
    Response,
    url_for)
import requests
import uuid
from time import sleep

class TotemPhone(Flask):
    def __init__(self, ip, name, ticket_number):
        super().__init__(__name__)
        self.name = name
        self.ticket_number = ticket_number
        self.ip = ip
        self.url_api_get_queue = f"http://{self.ip}:5000/queue"
        self.route('/', methods=['GET', 'POST'])(self.index)
        self.route('/gerar_link/<numero_senha>')(self.gerar_link)
        self.route('/display/<identificador>/<numero_senha>')(self.display_smartphone)
        self.route('/display', methods=['POST'])(self.display_content)
        self.route('/display')(self.send_content)
    def gerar_link(self, numero_senha):
        # Gerar um identificador único
        identificador = str(uuid.uuid4())

        # Redirecionar para a nova página com o identificador e o número da senha como parte da URL
        return redirect(url_for('display_smartphone', identificador=identificador, numero_senha=numero_senha))

    def display_smartphone(self, identificador, numero_senha):
        # Aqui você pode usar o identificador e o número da senha para obter as informações necessárias
        # e renderizar a nova página conforme necessário.
        return render_template('index_smartphone.html', numero_senha=numero_senha)
    
    def send_content(self):
        def generate():
            while True:
                content = f'{self.name}:{self.ticket_number}'
                sleep(0.7)
                yield f"data: {content}\n\n"
        sleep(0.1)
        response = Response(generate(), mimetype="text/event-stream")
        response.headers['Cache-Control'] = 'no-cache'
        return response

    def display_content(self):
        data = request.json
        self.name = data.get('name')
        self.ticket_number = data.get('ticket_number')
        return '', 200
    
    def queue_add(self, name, document):
        payload = f'name={name}&document_number={document}'

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", self.url_api_get_queue, headers=headers, data=payload)
        if response.status_code == 200:
            data = response.json()
            ticket_number = data['ticket']['ticket_number']
            return ticket_number
        elif response.status_code == 400:
            return ['error', response.json()['error']]

    def index(self):
        """
        Configuração da página inicial(Index)

        """
        if request.method == 'POST':
            nome = request.form['nome']
            documento = request.form['documento']
            ticket_number = self.queue_add(nome, documento)
            print(ticket_number)
            if ticket_number[0] == 'error':
                return render_template('index.html', error=ticket_number[1])
                
            else:
                
                return redirect(url_for('gerar_link', numero_senha=ticket_number))

        return render_template('index.html')

if __name__ == '__main__':
    app = TotemPhone('localhost', '', '')
    app.run(port=5003, debug=True)