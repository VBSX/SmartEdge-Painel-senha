from multiprocessing import Process
from waitress import serve
from api_queue.api import ApiQueue
from panel_ticket_view.web_view import DisplayApp
from triage_queue_view.triage import TriageQueue

debug_server = True
if debug_server:
    ip_machine = "localhost"
else:
    ip_machine = "yourIp"

ticket_visualizator = DisplayApp('', '')
ticketing_and_queue_manager = TriageQueue(ip=ip_machine)
api_server = ApiQueue(ip=ip_machine)

def start_api_server():
    if debug_server:
        api_server.run(port=5000, debug=True)
    else:
        serve(ticket_visualizator, host="0.0.0.0", port=5000)


def start_ticket_visualizator():
    if debug_server:
        ticket_visualizator.run(port=5001, debug=True)
    else:
        serve(ticket_visualizator, host="0.0.0.0", port=5001)


def start_ticketing_and_queue_manager():
    if debug_server:
        ticketing_and_queue_manager.run(port=5002, debug=True)
    else:
        serve(ticket_visualizator, host="0.0.0.0", port=5002)


if __name__ == '__main__':
    api_process = Process(target=start_api_server)
    ticket_visualizator_process = Process(target=start_ticket_visualizator)
    ticketing_and_queue_manager_process = Process(target=start_ticketing_and_queue_manager)

    api_process.start()
    ticket_visualizator_process.start()
    ticketing_and_queue_manager_process.start()

    api_process.join()
    ticket_visualizator_process.join()
    ticketing_and_queue_manager_process.join()
