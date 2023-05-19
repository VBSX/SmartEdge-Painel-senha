import requests
from time import sleep
import schedule
def zerar_contagem():
    url = "http://127.0.0.1:5000/queue"

    payload = 'reiniciar_contagem=true'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    response =requests.request("DELETE", url, headers=headers, data=payload)
    print(response.text)
    
zerar_contagem()

# schedule.every().day.at("10:07").do(resetar_senha)

# while True:
#     schedule.run_pending()
#     sleep(60) # wait one minute