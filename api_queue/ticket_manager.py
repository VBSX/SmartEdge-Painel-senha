import requests

class TicketManager():
    def __init__(self, ip) -> None:
        self.ip = ip
        self.url = f"http://{ip}:5000/queue"
        
    def resetar_senha(self):
        payload = 'zerar_fila=true'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("DELETE", self.url, headers=headers, data=payload)
        print(response.text)
        
    def zerar_contagem(self):
        payload = 'reiniciar_contagem=true'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        response =requests.request("DELETE", self.url, headers=headers, data=payload)
        print(response.text)

