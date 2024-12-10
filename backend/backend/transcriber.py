import requests
import uuid
import json

rquid = str(uuid.uuid4()) # Нужен для работы всех функций
auth_token = '' # Кину отдельно, чтобы его в .env добавить
#img_path = input() # Здесь должна быть функция получения изображения с фронта

""" Токен должен быть один для всех и обновляться раз в 30 минут """
def get_access_token(rquid, auth_token):
  url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

  payload='scope=GIGACHAT_API_PERS'

  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
    'RqUID': rquid,
    'Authorization': 'Basic ' + auth_token
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)

  if response.status_code == 200:
    return response.json()['access_token']
  else:
    return response.status_code

# Получение токена для работы остальных функций
acces_token = get_access_token(rquid, auth_token)

""" Это функция загрузки изобржения в API. 
Когда изображение приходит с фронта, сначала нужно добавить его в API, а потом получить id """
def load_img(access_token, img_path):
  url = "https://gigachat.devices.sberbank.ru/api/v1/files"

  payload = {'purpose': 'general'}

  files=[
  ('file',('file',open(str(img_path),'rb'),'image/png'))
  ]

  headers = {
  'Authorization': 'Bearer ' + access_token
  }

  response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False)

  if response.status_code == 200:
    return response.json()['id']
  else:
    return response.status_code

def load_pdf(access_token, img_path):
  url = "https://gigachat.devices.sberbank.ru/api/v1/files"

  payload = {'purpose': 'general'}

  files=[
  ('file',('file',open(str(img_path),'rb'),'image/pdf'))
  ]

  headers = {
  'Authorization': 'Bearer ' + access_token
  }

  response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False)

  if response.status_code == 200:
    return response.json()['id']
  else:
    return response.status_code

""" Для того, чтобы не хранить персональные данные и не перегружать API, все изоюбражения удаляются после обработки """
def delete_img(access_token, img_id):
  url = "https://gigachat.devices.sberbank.ru/api/v1/files/:" + img_id + "/delete"

  payload={}

  headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer ' + access_token
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)

  if response.status_code == 200:
    return response.json()
  else:
    return response.status_code

""" Обработка чеков """
def get_reciept_info(access_token, img_id):

  url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

  payload = json.dumps({
    "model": "GigaChat-Pro",
    "messages": [
      {
        "role": "user",
        "content": "Получи информацию о названии компании, дате совершения операции в формате dd.mm.yy, способе оплате (Наличными/Безналичными) и итоговой стоимости и ответ представь в json-формате с полями: Название компании, Дата операции, Итоговая сумма, Способ оплаты. В ответе укажи только json",
        "attachments": [
          img_id
        ]
      }
    ],
    "stream": False,
    "update_interval": 0
  })

  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + access_token
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)
  delete_img(acces_token, img_id)

  if response.status_code == 200:
    return response.json()['choices'][0]['message']['content']
  else:
    return response.status_code

""" Обработка свидетельства о рождении (нормально воспринимает только pdf) """
def get_birth_info(access_token, img_id):

  url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

  payload = json.dumps({
    "model": "GigaChat-Pro",
    "messages": [
      {
        "role": "user",
        "content": "Достань из этого файла ФИО ребёнка, ФИО матери, ФИО отца и дату рождения. Ответ предоставь в json формате",
        "attachments": [
          img_id
        ]
      }
    ],
    "stream": False,
    "update_interval": 0
  })

  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + access_token
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)
  delete_img(acces_token, img_id)

  if response.status_code == 200:
    return response.json()['choices'][0]['message']['content']
  else:
    return response.status_code

""" Обработка свидетельства о браке """
def get_marriage_info(access_token, img_id):

  url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

  payload = json.dumps({
    "model": "GigaChat-Pro",
    "messages": [
      {
        "role": "user",
        "content": "Достань из изображения информацию о названии документа, ФИО мужа и ФИО жены и ответ представь в json-формате с полями: Название документа, Отец: Фамилия, Имя, Отчество; Мать: Фамилия, Имя, Отчество. В ответе укажи только json",
        "attachments": [
          img_id
        ]
      }
    ],
    "stream": False,
    "update_interval": 0
  })

  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + access_token
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)
  delete_img(acces_token, img_id)

  if response.status_code == 200:
    return response.json()['choices'][0]['message']['content']
  else:
    return response.status_code

""" Обработка справок об операции """
def get_reference_info(access_token, img_id):

  url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

  payload = json.dumps({
    "model": "GigaChat-Pro",
    "messages": [
      {
        "role": "user",
        "content": "Получи информацию о дате совершения операции в формате dd.mm.yy, ФИО держателя карты и итоговой стоимости и ответ представь в json-формате с полями: Дата операции, Итоговая сумма, ФИО. В ответе укажи только json",
        "attachments": [
          img_id
        ]
      }
    ],
    "stream": False,
    "update_interval": 0
  })

  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + access_token
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)
  delete_img(acces_token, img_id)

  if response.status_code == 200:
    return response.json()['choices'][0]['message']['content']
  else:
    return response.status_code

""" Обработка договора об оказании услуг """
def get_contract_info(access_token, img_id):

  url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

  payload = json.dumps({
    "model": "GigaChat-Pro",
    "messages": [
      {
        "role": "user",
        "content": "Получи информацию о данных мед-организации и наличие подписи и печати (В ответе подпись и печать указать как True, если есть) и ответ представь в json-формате с полями: Мед-организация, Подпись, Печать. В ответе укажи только json",
        "attachments": [
          img_id
        ]
      }
    ],
    "stream": False,
    "update_interval": 0
  })

  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + access_token
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)
  delete_img(acces_token, img_id)

  if response.status_code == 200:
    return response.json()['choices'][0]['message']['content']
  else:
    return response.status_code
