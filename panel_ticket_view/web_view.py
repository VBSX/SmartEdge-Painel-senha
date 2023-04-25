from flask import (
    Flask,
    request,
    Response,
    send_from_directory,
    render_template,
    redirect)
from time import sleep

class DisplayApp(Flask):
    def __init__(self, name, ticket_number):
        super().__init__(__name__)
        self.name = name
        self.ticket_number = ticket_number
        self.static_dir = '/static'
        self.config['SEND_FILE_MAX_AGE_DEFAULT'] = 300
        self.route('/favicon.ico')(self.favicon)
        self.route('/display')(self.send_content)
        self.route('/static/<path:filename>')(self.serve_static)
        self.route('/display', methods=['POST'])(self.display_content)
        self.route('/display/painel')(self.painel_exibicao)
        self.route('/')(self.index_redirect)

    def favicon(self):
        return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

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

    def serve_static(self, filename):
        return send_from_directory(self.static_dir, filename)

    def display_content(self):
        data = request.json
        self.name = data.get('name')
        self.ticket_number = data.get('ticket_number')
        return '', 200

    def painel_exibicao(self):
        return render_template('painel_exibicao.html')

    def index_redirect(self):
        return redirect('/display/painel')
    

if __name__ == '__main__':
    app = DisplayApp('', '')
    app.run(port=5001, debug=True)