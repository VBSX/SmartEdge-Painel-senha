from flask import (
    Flask,
    request,
    render_template,
    redirect,
    send_from_directory)
import requests

class TriageQueue(Flask):
    def __init__(self,ip):
        super().__init__(__name__)
        self.ip = ip
        self.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1 MB
        self.static_dir = '/static'
        #Rota para servir o arquivo de imagem do favicon
        self.route('/favicon.ico')(self.favicon)
        self.route('/queue', methods=['GET', 'POST'])(self.view_queue)
        self.route('/call', methods=['POST'])(self.call_in_panel_view)
        self.route('/', methods=['GET', 'POST'])(self.index)

    def favicon(self):
        return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

    def queue_add(self,name, document):
        payload=f'name={name}&document_number={document}'
        url = f"http://{self.ip}:5000/queue"
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        response_server = requests.request("POST", url, headers=headers, data=payload)
        if response_server:
            
            return 200
        
    def view_queue(self):
        url = f"http://{self.ip}:5000/queue"
        response = requests.request("GET", url)
        queue_data = response.json() 

        return render_template('queue.html', queue_data=queue_data)

    def call_in_panel_view(self):
        name = request.form['name']
        ticket_number = request.form['document_number']
        url = f"http://{self.ip}:5000/call"

        payload=f'name={name}&document_number={ticket_number}'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return redirect('/queue') 

    def index(self):
        """
        Configuração da página inicial(Index)
        
        """
        if request.method == 'POST':
            nome = request.form['nome']
            documento = request.form['documento']
            # Lógica para colocar os dados na fila
            self.queue_add(nome,documento)
            return render_template('index.html', sucesso=True, nome=nome)
        return render_template('index.html')

if __name__ == '__main__':
    app = TriageQueue(ip="localhost")
    app.run(port=5002, debug=True)
# if __name__ == "__main__":

#     serve(app, host="0.0.0.0", port=5001)