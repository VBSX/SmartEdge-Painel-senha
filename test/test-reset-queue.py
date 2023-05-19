import requests
from time import sleep
import schedule
def resetar_senha():
    url = "http://127.0.0.1:5000/queue"
    payload = 'zerar_fila=true'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("DELETE", url, headers=headers, data=payload)
    print(response.text)
    
resetar_senha()
# schedule.every().day.at("10:00").do(resetar_senha)

# while True:
#     schedule.run_pending()
#     sleep(55) # wait one minute