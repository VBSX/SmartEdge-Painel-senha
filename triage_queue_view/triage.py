from flask import (
    Flask,
    request,
    render_template,
    redirect,
    send_from_directory,
    url_for)
import requests

class TriageQueue(Flask):
    def __init__(self,ip):
        super().__init__(__name__)
        self.ip = ip
        self.url_api_get_queue = f"http://{self.ip}:5000/queue"
        self.url_call_api = f"http://{self.ip}:5000/call"
        self.static_dir = '/static'
        self.config['SEND_FILE_MAX_AGE_DEFAULT'] = 300
        #Rota para servir o arquivo de imagem do favicon
        self.route('/favicon.ico')(self.favicon)
        self.route('/queue', methods=['GET'])(self.view_queue)
        self.route('/call', methods=['POST'])(self.call_in_panel_view)
        self.route('/delete_queue', methods=['POST'])(self.delete_queue)
        self.route('/', methods=['GET', 'POST'])(self.index)

    def favicon(self):
        return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

    def queue_add(self,name, document):
        payload=f'name={name}&document_number={document}'
        
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        requests.request("POST", self.url_api_get_queue, headers=headers, data=payload)
        
    def view_queue(self):
        response = requests.request("GET", self.url_api_get_queue)
        queue_data = response.json() 
        return render_template('queue.html', queue_data=queue_data)

    def call_in_panel_view(self):
        name = request.form['name']
        ticket_number = request.form['document_number']
        payload=f'name={name}&document_number={ticket_number}'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        requests.request("POST", self.url_call_api, headers=headers, data=payload)
        return redirect(url_for('view_queue'))
        
    def index(self):
        """
        Configuração da página inicial(Index)
        
        """
        if request.method == 'POST':
            nome = request.form['nome']
            documento = request.form['documento']
            self.queue_add(nome,documento)
            return render_template('index.html', sucesso=True, nome=nome)
        return render_template('index.html')

    def delete_queue(self):
        name = request.form['name']
        ticket_document_number = request.form['document_number']
        ticket_number = request.form['ticket_number']
        payload=f'name={name}&document_number={ticket_document_number}&ticket_number={ticket_number}'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        requests.request(method="DELETE",url=self.url_api_get_queue, headers=headers, data=payload)
        return redirect(url_for('view_queue'))
    
if __name__ == '__main__':
    app = TriageQueue(ip="localhost")
    app.run(port=5002, debug=True)
# if __name__ == "__main__":

#     serve(app, host="0.0.0.0", port=5001)