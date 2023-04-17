import requests
from time import sleep


def criar_senha():
    url = "http://localhost:5000/queue"

    payload='name=cleber&document_number=123'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

def chamar_senha():
    url = "http://localhost:5000/call"

    payload='name=cleber&document_number=123'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    
criar_senha()

chamar_senha()
sleep(2)
    
    