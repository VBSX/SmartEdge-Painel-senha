import threading
from waitress import serve
from api_queue.api import ApiQueue
from api_queue.ticket_manager import TicketManager
from panel_ticket_view.web_view import DisplayApp
from triage_queue_view.triage import TriageQueue
from totem_smartphone.totem import TotemPhone
from time import sleep
import schedule

debug_server = False
if debug_server:
    ip_machine = "localhost"
else:
    ip_machine = "0.0.0.0"

ticket_visualizator = DisplayApp('', '')
ticketing_and_queue_manager = TriageQueue(ip="127.0.0.1")
api_server = ApiQueue(ip="127.0.0.1")
totem_server = TotemPhone("127.0.0.1", '', '')

def start_api_server():
    if debug_server:
        api_server.run(port=5000, debug=True)
    else:
        serve(api_server, host=ip_machine, port=5000)

def start_ticket_visualizator():
    if debug_server:
        ticket_visualizator.run(port=5001, debug=True)
    else:
        serve(ticket_visualizator, host=ip_machine, port=5001)

def start_ticketing_and_queue_manager():
    if debug_server:
        ticketing_and_queue_manager.run(port=5002, debug=True)
    else:
        serve(ticketing_and_queue_manager, host=ip_machine, port=5002)

def start_totem_server():
    if debug_server:
        totem_server.run(port=5003, debug=True)
    else:
        serve(totem_server, host=ip_machine, port=5003)
        
def reset_ticket():
    ticket = TicketManager(ip_machine)
    ticket.resetar_senha()
    ticket.zerar_contagem()

def schedule_reset():
    schedule.every().day.at("00:00").do(reset_ticket)
    while True:
        schedule.run_pending()
        sleep(60) # wait one minute

# Iniciar as funções em threads separadas
api_thread = threading.Thread(target=start_api_server)
ticket_visualizator_thread = threading.Thread(target=start_ticket_visualizator)
ticketing_and_queue_manager_thread = threading.Thread(target=start_ticketing_and_queue_manager)
totem_server_thread = threading.Thread(target=start_totem_server)
reset_thread = threading.Thread(target=schedule_reset)

# Iniciar as threads em paralelo
api_thread.start()
ticket_visualizator_thread.start()
ticketing_and_queue_manager_thread.start()
totem_server_thread.start()
