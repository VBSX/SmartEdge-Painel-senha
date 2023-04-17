import threading
from waitress import serve
from api_queue.api import ApiQueue
from panel_ticket_view.web_view import DisplayApp
from triage_queue_view.triage import TriageQueue

debug_server = False
if debug_server:
    ip_machine = "localhost"
else:
    ip_machine = "10.16.100.119"

ticket_visualizator = DisplayApp('', '')
ticketing_and_queue_manager = TriageQueue(ip=ip_machine)
api_server = ApiQueue(ip=ip_machine)

def start_api_server():
    if debug_server:
        api_server.run(port=5000, debug=True)
    else:
        serve(api_server, host="10.16.100.119", port=5000)

def start_ticket_visualizator():
    if debug_server:
        ticket_visualizator.run(port=5001, debug=True)
    else:
        serve(ticket_visualizator, host="10.16.100.119", port=5001)

def start_ticketing_and_queue_manager():
    if debug_server:
        ticketing_and_queue_manager.run(port=5002, debug=True)
    else:
        serve(ticketing_and_queue_manager, host="10.16.100.119", port=5002)

# Iniciar as funções em threads separadas
api_thread = threading.Thread(target=start_api_server)
ticket_visualizator_thread = threading.Thread(target=start_ticket_visualizator)
ticketing_and_queue_manager_thread = threading.Thread(target=start_ticketing_and_queue_manager)

# Iniciar as threads em paralelo
api_thread.start()
ticket_visualizator_thread.start()
ticketing_and_queue_manager_thread.start()
