import requests
import uuid
import json
from fpdf import FPDF
from PIL import Image
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat

rquid = str(uuid.uuid4()) # Нужен для работы всех функций
auth_token = '' # Кину отдельно, чтобы его в .env добавить 
# img_path = input() # Здесь должна быть функция получения изображения с фронта

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
access_token = get_access_token(rquid, auth_token)

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
  ('file',('file',open(str(img_path),'rb'),'application/pdf'))
  ]

  headers = {
  'Authorization': 'Bearer ' + access_token
  }

  response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False)

  if response.status_code == 200:
    return response.json()['id']
  else:
    return response

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

def image_to_pdf(image_path, output_pdf_path):

    pdf = FPDF()

    with Image.open(image_path) as img:
        width, height = img.size

    pdf.add_page()

    pdf_width = 210
    pdf_height = 297

    if width > height:
        scale_factor = pdf_width / width
        img_width = pdf_width
        img_height = height * scale_factor
    else:
        scale_factor = pdf_height / height
        img_width = width * scale_factor
        img_height = pdf_height

    pdf.image(image_path, x=0, y=0, w=img_width, h=img_height)
      
    pdf.output(output_pdf_path)



def images_to_pdf(image_paths, output_pdf_path):

    pdf = FPDF()

    for image_path in image_paths:
        with Image.open(image_path) as img:
            width, height = img.size

        pdf.add_page()

        pdf_width = 210
        pdf_height = 297

        if width > height:
            scale_factor = pdf_width / width
            img_width = pdf_width
            img_height = height * scale_factor
        else:
            scale_factor = pdf_height / height
            img_width = width * scale_factor
            img_height = pdf_height

        pdf.image(image_path, x=0, y=0, w=img_width, h=img_height)

    pdf.output(output_pdf_path)

"""Очищение вывода в запросах"""
def extract_content(s):
    start_index = s.find('{')
    end_index = s.rfind('}')

    if start_index != -1 and end_index != -1:
        return s[start_index:end_index + 1]
    else:
        return ""

"""PDF методы"""

def get_statement_info(access_token, img_id):
  
  url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

  payload = json.dumps({
    "model": "GigaChat-Max",
    "messages": [
      {
        "role": "user",
        "content": "Прочитай данный текст заявления и выведи из него всю важную информацию в виде списка, а именно: Название, ФИО заявителя, ФИО ребенка, ДР ребенка, Дата подписи, Наличие подписи.",
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
  delete_img(access_token, img_id)

  if response.status_code == 200:
    return response.json()['choices'][0]['message']['content']
  else:
    return response.status_code


def get_marriage_info(access_token, img_id):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    payload = json.dumps({
        "model": "GigaChat-Max",
        "messages": [
            {
                "role": "user",
                "content": "Прочитай данный текст свидетельства о браке и выведи из него всю важную информацию в виде списка, а именно: Название, ФИО мужа с использованием присвоенной фамилии, ФИО жены с присвоенной фамилией",
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
    delete_img(access_token, img_id)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return response.status_code

def get_reference_six_info(access_token, img_id):
  
  url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

  payload = json.dumps({
    "model": "GigaChat-Max",
    "messages": [
      {
        "role": "user",
        "content": "Прочитай данный текст справки и выведи из него всю важную информацию в виде списка, а именно: ФИО плательщика, ФИО ребенка, ДР ребенка, Дата начала страхования, Дата окончания страхования, Номер полиса по которому произведена оплата.",
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
  delete_img(access_token, img_id)

  if response.status_code == 200:
    return response.json()['choices'][0]['message']['content']
  else:
    return response.status_code

def get_reciept_info(access_token, img_id):
  
  url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

  payload = json.dumps({
    "model": "GigaChat-Max",
    "messages": [
      {
        "role": "user",
        "content": "Ты валидатор данных, который получает информацию и образует json-файл по полям на выходе. Даты переводи в формат dd/mm/yyyy. В НАЗВАНИИ АБСОЛЮТНО ВСЕГДА ВЫВОДИ - Чек. В сумме укажи только число, указанное в итоговой сумме к оплате в формате float, согласно образцу (20000.00), но внутри строки. В поле Место укажи название компании, в которой произведена оплата. Если в способе оплаты встречаются слова VISA или Mastercard, в поле Способ Оплаты пиши Безналичный. Если в способе оплаты написано Наличными, пиши Наличными. ВЫВЕДИ ТОЛЬКО СЛЕДУЮЩИЕ ПОЛЯ: Название, Способ оплаты, ФИО плательщика, Дата оплаты, Cумма, Место оплаты.",
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
  delete_img(access_token, img_id)

  if response.status_code == 200:
    return extract_content(response.json()['choices'][0]['message']['content'])
  else:
    return response.status_code
 

def get_info(access_token, img_id):
  
  url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

  payload = json.dumps({
    "model": "GigaChat-Max",
    "messages": [
      {
        "role": "user",
        "content": "Получи информацию из этого файла и выведи её в виде списка",
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
  delete_img(access_token, img_id)

  if response.status_code == 200:
    return response.json()['choices'][0]['message']['content']
  else:
    return response.status_code

"""Свидетельство о рождении"""
def birth_response(user_content, auth_token):

  model = GigaChat(
      credentials=auth_token,
      scope="GIGACHAT_API_PERS",
      model="GigaChat",
      verify_ssl_certs=False,
  )

  messages = [
      SystemMessage(
          content="Ты валидатор данных, который получает информацию и образует json-файл по полям на выходе. Даты переводи в формат dd/mm/yyyy В поле Название всегда указывай СВИДЕТЕЛЬСТВО О РОЖДЕНИИ. Выведи только следующие поля строго с такими же названиями: Название, ФИО ребенка, ФИО отца, ФИО матери, ДР ребенка"
    )
  ] 

  messages.append(HumanMessage(content=user_content))
  res = model.invoke(messages)
  messages.append(res)
  return json.loads(extract_content(res.content))

"""Свидетельство о браке"""
def marriage_response(user_content, auth_token):

  model = GigaChat(
      credentials=auth_token,
      scope="GIGACHAT_API_PERS",
      model="GigaChat",
      verify_ssl_certs=False,
  )

  messages = [
      SystemMessage(
          content="Ты валидатор данных, который получает информацию и образует json-файл по полям на выходе. Даты переводи в формат dd/mm/yyyy В поле Название всегда указывай СВИДЕТЕЛЬСТВО О БРАКЕ. Сформируй ФИО мужа и ФИО жены, полученные после заключения брака с использованием ПРИСВОЕННЫХ ФАМИЛИЙ, И ОРИГИНАЛЬНЫХ ИМЕНИ И ОТЧЕСТВА. Выведи только следующие поля: Название, ФИО мужа, ФИО жены"
    )
  ] 

  messages.append(HumanMessage(content=user_content))
  res = model.invoke(messages)
  messages.append(res)
  return json.loads(extract_content(res.content))

"""Заявление"""
def statement_response(user_content, auth_token):

  model = GigaChat(
      credentials=auth_token,
      scope="GIGACHAT_API_PERS",
      model="GigaChat",
      verify_ssl_certs=False,
  )

  messages = [
      SystemMessage(
          content="Ты валидатор данных, который получает информацию и выдает ответ строго в формате JSON. Поля JSON всегда одинаковые и строго соответствуют следующим названиям:\
          - Название\
          - ФИО заявителя\
          - ФИО ребенка\
          - ДР ребенка\
          - Дата подписи\
          - Наличие подписи\
          \
          Поле 'Название' всегда имеет значение 'Заявление'.\
          Все даты переводятся в формат dd/mm/yyyy.\
          Обрати внимание: название полей в JSON не меняется независимо от входных данных.\
          Выводи только перечисленные поля в указанном порядке."
      )
  ]

  messages.append(HumanMessage(content=user_content))
  res = model.invoke(messages)
  print(res)
  messages.append(res)
  return json.loads(extract_content(res.content))

"""Справка 6.15"""
def reference_six_response(user_content, auth_token):

  model = GigaChat(
      credentials=auth_token,
      scope="GIGACHAT_API_PERS",
      model="GigaChat",
      verify_ssl_certs=False,
  )

  messages = [
      SystemMessage(
          content="Ты валидатор данных, который получает информацию и выводит ответ в json-формате без указания, что это json по полям на выходе. В ответе не должно быть ничего лишнего, только json. В поле Название всегда пиши Справка от страховой компании. Даты переводи в формат dd/mm/yyyy. Для номера полиса ДМС используй номер полиса, по которому произведена оплата, он находится после указания №. Выведи только следующие поля: Название, ФИО плательщика, ФИО ребенка, ДР ребенка, Дата начала страхования, Дата окончания страхования, Номер полиса ДМС."
    )
  ] 

  messages.append(HumanMessage(content=user_content))
  res = model.invoke(messages)
  messages.append(res)
  return json.loads(extract_content(res.content))

"""Справка об оплате медицинских услуг"""
def double_page_response(user_content, auth_token):

  model = GigaChat(
      credentials=auth_token,
      scope="GIGACHAT_API_PERS",
      model="GigaChat",
      verify_ssl_certs=False,
  )

  messages = [
      SystemMessage(
          content="Ты валидатор данных, который получает информацию и выдаёт ответ в json-формате, без указания, что это json по полям на выходе. Даты переводи в формат dd/mm/yyyy В поле Название всегда пиши - Справка об оплате медицинских услуг. Выведи только следующие поля: Название, ФИО налогоплательщика, ДР налогоплательщика, Название организации, ИНН, Паспортные данные, Сумма расходов, ФИО выдавшего справку, ФИО ребенка, ДР ребенка, Дата, Подпись."
    )
  ] 

  messages.append(HumanMessage(content=user_content))
  res = model.invoke(messages)
  messages.append(res)
  return json.loads(extract_content(res.content))

"""Выписка по чеку"""
def reference_response(user_content, auth_token):

  model = GigaChat(
      credentials=auth_token,
      scope="GIGACHAT_API_PERS",
      model="GigaChat",
      verify_ssl_certs=False,
  )

  messages = [
      SystemMessage(
          content='''Ты валидатор данных. Твоя задача — принимать входную информацию, валидировать её и возвращать JSON-объект с преобразованными данными. Требования:\
          Поле 'Название':
          Всегда должно быть строкой "Выписка", независимо от входных данных.
          Поле "Дата":
          Преобразуй любую входную дату в формат dd/mm/yyyy.
          Поле "Итоговая сумма":
          Извлеки только числовую часть суммы и преобразуй её в float.
          Поле "ФИО плательщика":
          Должно быть строкой.
          Вывод:
          Верни только эти четыре поля в JSON-объекте:
          Название
          Дата
          Итоговая сумма
          ФИО плательщика'''
      )
  ]

  messages.append(HumanMessage(content=user_content))
  res = model.invoke(messages)
  messages.append(res)
  return json.loads(extract_content(res.content))

"""Чек"""
def reciept_response(user_content, auth_token):

  model = GigaChat(
      credentials=auth_token,
      scope="GIGACHAT_API_PERS",
      model="GigaChat",
      verify_ssl_certs=False,
  )

  messages = [
      SystemMessage(
          content="Ты валидатор данных, который получает информацию и образует json-файл по полям на выходе. Даты переводи в формат dd/mm/yyyy. В названии всегда указывай - Чек. Выведи только следующие поля: Название, Способ оплаты, ФИО плтельщика, Дата оплаты, Сумма, Место, Подпись, Печать."
    )
  ] 

  messages.append(HumanMessage(content=user_content))
  res = model.invoke(messages)
  messages.append(res)
  return json.loads(extract_content(res.content))

"""Полис ДМС"""
def insurance_response(user_content, auth_token):

  model = GigaChat(
      credentials=auth_token,
      scope="GIGACHAT_API_PERS",
      model="GigaChat",
      verify_ssl_certs=False,
  )

  messages = [
      SystemMessage(
          content="Ты валидатор данных, который получает информацию и выдаёт ответ в json формате, без указания того, что это json по полям на выходе. Даты переводи в формат dd/mm/yyyy. В названии всегда указывай - Полис ДМС. Выведи только следующие поля: Название, ФИО ребенка, ДР ребенка, Номер полиса, Начало действия страхования, Окончание действия страхования."
    )
  ] 

  messages.append(HumanMessage(content=user_content))
  res = model.invoke(messages)
  messages.append(res)
  return json.loads(extract_content(res.content))

"""Методы для картинок"""

"""Свидетельство о рождении"""
def process_birth_certificate(access_token, img_id):
    """
    Функция для обработки свидетельства о рождении:
    1. Извлекает текст с изображения.
    2. Преобразует текст в JSON на основе заданного промпта.
    """
    base_url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }


    prompt = """
    Прочитай предоставленный текст из свидетельства о рождении и преобразуй его в формат JSON с полями:
    - "Название" — фиксированное значение: "СВИДЕТЕЛЬСТВО О РОЖДЕНИИ".
    - "ФИО ребенка" — Фамилия, Имя, Отчество ребенка.
    - "ДР ребенка" — дата рождения ребенка в формате DD/MM/YYYY.
    - "ФИО отца" — Фамилия, Имя, Отчество отца.
    - "ФИО матери" — Фамилия, Имя, Отчество матери.
        НЕМНОГО ИСПОЛЬЗУЙ ЛОГИКУ, В СЛУЧАЕ ЕСЛИ ФАМИЛИИ ОТЛИЧАЮТСЯ НА ОДНУ БУКВУ ВАЛИДИРУЙ КАК ТЫ БУДЕШЬ ЧТО БЫЛО И ТД
    Убедись, что данные корректны. Игнорируй информацию о месте рождения, национальности, гражданстве и других дополнительных данных. Пример результата:
    {
      "Название": "СВИДЕТЕЛЬСТВО О РОЖДЕНИИ",
      "ФИО ребенка": "Иванов Иван Иванович",
      "ДР ребенка": "15/05/2010",
      "ФИО отца": "Иванов Петр Сергеевич",
      "ФИО матери": "Иванова Мария Васильевна"
    }

    В ответ дай только JSON который я запрашиваю
    """
    
    # Шаг 1: Извлечение текста с изображения
    extract_text_payload = json.dumps({
        "model": "GigaChat-Max",
        "messages": [
            {
                "role": "user",
                "content": """Выведи информацию со снимка текстом всю, сделай это качественно /
                Свидетельство о рождении на стандартном бланке. Верхняя часть документа содержит заголовок. Указаны следующие поля: ФИО ребенка, дата рождения (прописью и цифрами), место рождения, гражданство, сведения об отце (ФИО, гражданство, национальность), сведения о матери (ФИО, гражданство, национальность), орган ЗАГС, дата составления записи, дата выдачи документа, подпись и печать. В документе используются зелёные декоративные элементы, печать синяя.""",
                "attachments": [img_id]
            }
        ],
        "stream": False,
        "update_interval": 0
    })

    extract_response = requests.post(base_url, headers=headers, data=extract_text_payload, verify=False)
    if extract_response.status_code != 200:
        delete_img(access_token, img_id)
        return {"error": f"Ошибка извлечения текста: {extract_response.status_code}", "details": extract_response.text}

    extracted_text = extract_response.json()['choices'][0]['message']['content']
    # print("Извлечённый текст:")
    # print(extracted_text)

    # Шаг 2: Преобразование текста в JSON
    process_payload = json.dumps({
        "model": "GigaChat-Max",
        "messages": [
            {
                "role": "user",
                "content": f"{prompt}\n\nТекст документа:\n{extracted_text}"
            }
        ],
        "stream": False,
        "update_interval": 0
    })

    process_response = requests.post(base_url, headers=headers, data=process_payload, verify=False)
    delete_img(access_token, img_id)  # Удаляем изображение после обработки
    if process_response.status_code == 200:
        try:
            raw_content = process_response.json()['choices'][0]['message']['content']
            json_start = raw_content.find("{")
            json_end = raw_content.rfind("}") + 1
            if json_start != -1 and json_end != -1:
                cleaned_json = raw_content[json_start:json_end]
                return json.loads(cleaned_json)
            else:
                return {"error": "JSON не найден в ответе", "response": raw_content}
        except Exception as e:
            return {"error": f"Ошибка обработки JSON: {str(e)}", "response": process_response.json()}
    else:
        return {"error": f"Ошибка запроса на преобразование: {process_response.status_code}", "details": process_response.text}

"""Свидетельство о браке"""
def process_marriage_certificate(access_token, img_id):
    """
    Функция для обработки свидетельства о браке:
    1. Извлекает текст с изображения.
    2. Преобразует текст в JSON на основе заданного промпта.
    """
    base_url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }


    prompt = """
    Прочитай предоставленный текст из свидетельства о браке и преобразуй его в формат JSON с полями:
    - "Название" — фиксированное значение: "СВИДЕТЕЛЬСТВО О БРАКЕ".
    - "ФИО мужа" — Фамилия, Имя, Отчество мужа.
    - "ФИО жены" — Фамилия, Имя, Отчество жены.
        НЕМНОГО ИСПОЛЬЗУЙ ЛОГИКУ, В СЛУЧАЕ ЕСЛИ ФАМИЛИИ ОТЛИЧАЮТСЯ НА ОДНУ БУКВУ ВАЛИДИРУЙ КАК ТЫ БУДЕШЬ ЧТО БЫЛО И ТД
    Убедись, что данные корректны. Игнорируй информацию о месте рождения, национальности, гражданстве и других дополнительных данных. Пример результата:
    {
      "Название": "СВИДЕТЕЛЬСТВО О БРАКЕ",
      "ФИО мужа": "Иванов Петр Сергеевич",
      "ФИО жены": "Иванова Мария Васильевна"
    }

    В ответ дай только JSON который я запрашиваю
    """
    
    # Шаг 1: Извлечение текста с изображения
    extract_text_payload = json.dumps({
        "model": "GigaChat-Max",
        "messages": [
            {
                "role": "user",
                "content": """Выведи информацию со снимка текстом всю, сделай это качественно /
                Свидетельство о браке на стандартном бланке. Верхняя часть документа содержит заголовок. Указаны следующие поля: информация про мужа (ФИО и Дата рождения), информация про жену (ФИО и Дата рождения), дата заключения брака и дата оформления брака (прописью и цифрами), присвоенные фамилии, место регистрации, дата выдачи, подпись и печать. В документе используются красные декоративные элементы, печать синяя.""",
                "attachments": [img_id]
            }
        ],
        "stream": False,
        "update_interval": 0
    })

    extract_response = requests.post(base_url, headers=headers, data=extract_text_payload, verify=False)
    if extract_response.status_code != 200:
        delete_img(access_token, img_id)
        return {"error": f"Ошибка извлечения текста: {extract_response.status_code}", "details": extract_response.text}

    extracted_text = extract_response.json()['choices'][0]['message']['content']
    # print("Извлечённый текст:")
    # print(extracted_text)

    # Шаг 2: Преобразование текста в JSON
    process_payload = json.dumps({
        "model": "GigaChat-Max",
        "messages": [
            {
                "role": "user",
                "content": f"{prompt}\n\nТекст документа:\n{extracted_text}"
            }
        ],
        "stream": False,
        "update_interval": 0
    })

    process_response = requests.post(base_url, headers=headers, data=process_payload, verify=False)
    delete_img(access_token, img_id)  # Удаляем изображение после обработки
    if process_response.status_code == 200:
        try:
            raw_content = process_response.json()['choices'][0]['message']['content']
            json_start = raw_content.find("{")
            json_end = raw_content.rfind("}") + 1
            if json_start != -1 and json_end != -1:
                cleaned_json = raw_content[json_start:json_end]
                return json.loads(cleaned_json)
            else:
                return {"error": "JSON не найден в ответе", "response": raw_content}
        except Exception as e:
            return {"error": f"Ошибка обработки JSON: {str(e)}", "response": process_response.json()}
    else:
        return {"error": f"Ошибка запроса на преобразование: {process_response.status_code}", "details": process_response.text}

"""Чек"""
def process_reciept(access_token, img_id):
    """
    Функция для обработки чеков:
    1. Извлекает текст с изображения.
    2. Преобразует текст в JSON на основе заданного промпта.
    """
    base_url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }


    prompt = """
    Прочитай предоставленный текст из чека и преобразуй его в формат JSON с полями:
    - "Название" — Чек.
    - "Способ оплаты" — Способ оплаты наличиными или безналично.
    - "ФИО плательщика" — Фамилия, Имя, Отчество плательщика.
    - "Дата оплаты" — дата оплаты в формате DD/MM/YYYY.
    - "Сумма" — Итоговая сумма по операции.
    - "Место оплаты" — Название организации, где была проведена оплата.
    - "Подпись" — Наличие подписи в формате true/false.
    - "Печать" — Наличие печати в формате true/false.
        НЕМНОГО ИСПОЛЬЗУЙ ЛОГИКУ, В СЛУЧАЕ ЕСЛИ ФАМИЛИИ ОТЛИЧАЮТСЯ НА ОДНУ БУКВУ ВАЛИДИРУЙ КАК ТЫ БУДЕШЬ ЧТО БЫЛО И ТД
    Убедись, что данные корректны. Игнорируй информацию о месте рождения, национальности, гражданстве и других дополнительных данных. Пример результата:
    {
      "Название": "Чек",
      "Способ оплаты": "Безналично",
      "ФИО плательщика": "Иванов Иван Иванович",
      "Дата оплаты": "15/05/2024",
      "Сумма": "16000.00",
      "Место оплаты": "Больница",
      "Подпись": True,
      "Печать": True
    }

    В ответ дай только JSON который я запрашиваю
    """
    
    # Шаг 1: Извлечение текста с изображения
    extract_text_payload = json.dumps({
        "model": "GigaChat-Max",
        "messages": [
            {
                "role": "user",
                "content": """Выведи информацию со снимка текстом всю, сделай это качественно /
                Стандартный чек, сверху находится шапка с названием места оплаты, далее идут пункты по которым была произведена оплата, количество и цена. В конце указана итоговая стоимость, способ оплаты, дата оплаты, подпись и печать. Печать синяя.""",
                "attachments": [img_id]
            }
        ],
        "stream": False,
        "update_interval": 0
    })

    extract_response = requests.post(base_url, headers=headers, data=extract_text_payload, verify=False)
    if extract_response.status_code != 200:
        delete_img(access_token, img_id)
        return {"error": f"Ошибка извлечения текста: {extract_response.status_code}", "details": extract_response.text}

    extracted_text = extract_response.json()['choices'][0]['message']['content']
    # print("Извлечённый текст:")
    # print(extracted_text)

    # Шаг 2: Преобразование текста в JSON
    process_payload = json.dumps({
        "model": "GigaChat-Max",
        "messages": [
            {
                "role": "user",
                "content": f"{prompt}\n\nТекст документа:\n{extracted_text}"
            }
        ],
        "stream": False,
        "update_interval": 0
    })

    process_response = requests.post(base_url, headers=headers, data=process_payload, verify=False)
    delete_img(access_token, img_id)  # Удаляем изображение после обработки
    if process_response.status_code == 200:
        try:
            raw_content = process_response.json()['choices'][0]['message']['content']
            json_start = raw_content.find("{")
            json_end = raw_content.rfind("}") + 1
            if json_start != -1 and json_end != -1:
                cleaned_json = raw_content[json_start:json_end]
                return json.loads(cleaned_json)
            else:
                return {"error": "JSON не найден в ответе", "response": raw_content}
        except Exception as e:
            return {"error": f"Ошибка обработки JSON: {str(e)}", "response": process_response.json()}
    else:
        return {"error": f"Ошибка запроса на преобразование: {process_response.status_code}", "details": process_response.text}

"""Выписка по чеку"""
def process_reference(access_token, img_id):
    """
    Функция для обработки справок по чекам:
    1. Извлекает текст с изображения.
    2. Преобразует текст в JSON на основе заданного промпта.
    """
    base_url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }


    prompt = """
    Прочитай предоставленный текст из выписки об операции и преобразуй его в формат JSON с полями:
    - "Название" — "Выписка"
    - "ФИО плательщика" — Фамилия, Имя, Отчество плательщика.
    - "Дата оплаты" — дата оплаты в формате DD/MM/YYYY.
    - "Сумма" — Итоговая сумма по операции.
    - "Место оплаты" — Название организации, где была проведена оплата.
        НЕМНОГО ИСПОЛЬЗУЙ ЛОГИКУ, В СЛУЧАЕ ЕСЛИ ФАМИЛИИ ОТЛИЧАЮТСЯ НА ОДНУ БУКВУ ВАЛИДИРУЙ КАК ТЫ БУДЕШЬ ЧТО БЫЛО И ТД
    Убедись, что данные корректны. Игнорируй дополнительные данные. Пример результата:
    {
      "Название": "Выписка",
      "ФИО плательщика": "Иванов Иван Иванович",
      "Дата оплаты": "15/05/2024",
      "Сумма": "16000.00",
      "Место оплаты": "Больница",
    }

    В ответ дай только JSON который я запрашиваю
    """
    
    # Шаг 1: Извлечение текста с изображения
    extract_text_payload = json.dumps({
        "model": "GigaChat-Max",
        "messages": [
            {
                "role": "user",
                "content": """Выведи информацию со снимка текстом всю, сделай это качественно /
                Стандартная выписка по операции, сверху находится шапка с названием банка, который был использован для оплаты. В центре указаны сумма оплаты, ФИО плательщика,дата оплаты, место оплаты, номера счетов. В документе могут быть декоративные элементы разного цвета.""",
                "attachments": [img_id]
            }
        ],
        "stream": False,
        "update_interval": 0
    })

    extract_response = requests.post(base_url, headers=headers, data=extract_text_payload, verify=False)
    if extract_response.status_code != 200:
        delete_img(access_token, img_id)
        return {"error": f"Ошибка извлечения текста: {extract_response.status_code}", "details": extract_response.text}

    extracted_text = extract_response.json()['choices'][0]['message']['content']
    # print("Извлечённый текст:")
    # print(extracted_text)

    # Шаг 2: Преобразование текста в JSON
    process_payload = json.dumps({
        "model": "GigaChat-Max",
        "messages": [
            {
                "role": "user",
                "content": f"{prompt}\n\nТекст документа:\n{extracted_text}"
            }
        ],
        "stream": False,
        "update_interval": 0
    })

    process_response = requests.post(base_url, headers=headers, data=process_payload, verify=False)
    delete_img(access_token, img_id)  # Удаляем изображение после обработки
    if process_response.status_code == 200:
        try:
            raw_content = process_response.json()['choices'][0]['message']['content']
            json_start = raw_content.find("{")
            json_end = raw_content.rfind("}") + 1
            if json_start != -1 and json_end != -1:
                cleaned_json = raw_content[json_start:json_end]
                return json.loads(cleaned_json)
            else:
                return {"error": "JSON не найден в ответе", "response": raw_content}
        except Exception as e:
            return {"error": f"Ошибка обработки JSON: {str(e)}", "response": process_response.json()}
    else:
        return {"error": f"Ошибка запроса на преобразование: {process_response.status_code}", "details": process_response.text}

"""Полис ДМС"""
def process_insurance(access_token, img_id):
    """
    Функция для обработки полиса ДМС:
    1. Извлекает текст с изображения.
    2. Преобразует текст в JSON на основе заданного промпта.
    """
    base_url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }


    prompt = """
    Прочитай предоставленный текст из полиса ДМС и преобразуй его в формат JSON с полями:
    - "Название" — Полис ДМС
    - "ФИО ребенка" — Фамилия, Имя, Отчество ребенка.
    - "ДР ребенка" — дата рождения ребенка в формате DD/MM/YYYY.
    - "Номер полиса" — Уникальный номер полиса.
    - "Начало действия страхования" — Дата, с которой начинается действие страхования в формате DD/MM/YYYY.
    - "Окончание действия страхования" — Дата, до которой действителен ДМС в формате DD/MM/YYYY.
        НЕМНОГО ИСПОЛЬЗУЙ ЛОГИКУ, В СЛУЧАЕ ЕСЛИ ФАМИЛИИ ОТЛИЧАЮТСЯ НА ОДНУ БУКВУ ВАЛИДИРУЙ КАК ТЫ БУДЕШЬ ЧТО БЫЛО И ТД
    Убедись, что данные корректны. Игнорируй информацию о месте рождения, национальности, гражданстве и других дополнительных данных. Пример результата:
    {
      "Название": "Полис ДМС",
      "ФИО ребенка": "Иванов Иван Иванович",
      "ДР ребенка": "15/05/2010",
      "Номер полиса": "4400 2888 9654 3821",
      "Начало действия страхования": "25/01/2020",
      "Окончание действия страхования": "25/01/2030"
    }

    В ответ дай только JSON который я запрашиваю
    """
    
    # Шаг 1: Извлечение текста с изображения
    extract_text_payload = json.dumps({
        "model": "GigaChat-Max",
        "messages": [
            {
                "role": "user",
                "content": """Выведи информацию со снимка текстом всю, сделай это качественно /
                Стандартный полис ДМС содержит шапку с названием фирмы Страховщика, далее идёт блок с информацией страховщика (Адрес, Реквизиты, Контактные данные), блок с информацией страхователя (ФИО, адрес, паспорт, телефон, реквизиты, гражданство), блок с информацией застрахованного (ФИО, адрес, паспорт, телефон, гражданство), варианты страхования, срок действия полиса, подпись и печать. Документ содержит декоративные элементы разных цветов, печать синего цвета.""",
                "attachments": [img_id]
            }
        ],
        "stream": False,
        "update_interval": 0
    })

    extract_response = requests.post(base_url, headers=headers, data=extract_text_payload, verify=False)
    if extract_response.status_code != 200:
        delete_img(access_token, img_id)
        return {"error": f"Ошибка извлечения текста: {extract_response.status_code}", "details": extract_response.text}

    extracted_text = extract_response.json()['choices'][0]['message']['content']
    # print("Извлечённый текст:")
    # print(extracted_text)

    # Шаг 2: Преобразование текста в JSON
    process_payload = json.dumps({
        "model": "GigaChat-Max",
        "messages": [
            {
                "role": "user",
                "content": f"{prompt}\n\nТекст документа:\n{extracted_text}"
            }
        ],
        "stream": False,
        "update_interval": 0
    })

    process_response = requests.post(base_url, headers=headers, data=process_payload, verify=False)
    delete_img(access_token, img_id)  # Удаляем изображение после обработки
    if process_response.status_code == 200:
        try:
            raw_content = process_response.json()['choices'][0]['message']['content']
            json_start = raw_content.find("{")
            json_end = raw_content.rfind("}") + 1
            if json_start != -1 and json_end != -1:
                cleaned_json = raw_content[json_start:json_end]
                return json.loads(cleaned_json)
            else:
                return {"error": "JSON не найден в ответе", "response": raw_content}
        except Exception as e:
            return {"error": f"Ошибка обработки JSON: {str(e)}", "response": process_response.json()}
    else:
        return {"error": f"Ошибка запроса на преобразование: {process_response.status_code}", "details": process_response.text}
