import json
import os

from django.contrib.messages import SUCCESS
from django.core.exceptions import ValidationError
from django.http import JsonResponse

from .models import MedicalInsurance, Parent, Document
from datetime import datetime


def remove_dir(session_id,
              base_folder):
    from core.models import Document, MedicalInsurance
    import shutil

    if os.path.exists(base_folder):
        for item in os.listdir(base_folder):
            item_path = os.path.join(base_folder, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)

    try:
        shutil.rmtree(base_folder)
        print(f"Directory '{base_folder}' and its contents deleted successfully.")
    except OSError as e:
        print(f"Error: {e.strerror}")

    Document.objects.filter(session_id=session_id).delete()

    try:
        medicalInsurance = MedicalInsurance.objects.get(session_id=session_id)
        medicalInsurance.father.delete()
        medicalInsurance.mother.delete()
        medicalInsurance.delete()
    except MedicalInsurance.DoesNotExist:
        return JsonResponse({'message': 'Файлы пользователя уже удалены.'}, status=200)

def parse_date(date_str, date_name):
    formats = ['%d/%m/%Y', '%m/%d/%Y','%Y/%m/%d',
               '%Y-%m-%d', '%d-%m-%Y', '%m-%d-%Y',
               '%Y.%m.%d', '%d.%m.%Y']
    for fmt in formats:
        try:
            parsed_date = datetime.strptime(date_str, fmt)
            return parsed_date.date()
        except ValueError:
            continue
    # Если ни один формат не подошел, возвращаем JsonResponse с сообщением об ошибке
    return JsonResponse({'message': f"Не удалось распознать поле '{date_name}'"}, status=400)

# def parse_date(date_str, date_name):
#     try:
#         return datetime.strptime(date_str, '%Y-%m-%d').date()
#     except ValueError:
#         return JsonResponse({'message': f"Не удалось распознать поле \'{date_name}\'"}, status=400)

def clear_exist_medical_insurance(_session_id):
    existing_insurances = MedicalInsurance.objects.filter(session_id=_session_id)
    if existing_insurances.exists():
        # Удаление связанных объектов Parent
        for insurance in existing_insurances:
            if insurance.father:
                insurance.father.delete()
            if insurance.mother:
                insurance.mother.delete()
        # Удаление объектов MedicalInsurance
        existing_insurances.delete()

def delete_garbage_file(id):
    doc = Document.objects.get(id=id)
    if doc.path:
        file_path = doc.path.path
        if os.path.exists(file_path):
            os.remove(file_path)

    doc.delete()

def check_is_file_exist_and_delete(_file_name,_session_id):
    doc = Document.objects.filter(name=_file_name, session_id=_session_id).first()
    if doc:
        delete_garbage_file(doc.id)

class DataInspector:
    def __init__(self, json_data):
        self.json_data = json_data

    def check_marriage_certificate(self, _session_id):
        """
       Функция для обработки св-ва о браке
       """
        try:
            data = json.loads(self.json_data)

            if data:
                file_name = data.get('Название')
                father_name = data.get('ФИО мужа')
                mother_name = data.get('ФИО жены')

            if(file_name != "СВИДЕТЕЛЬСТВО О ЗАКЛЮЧЕНИИ БРАКА" and file_name != "СВИДЕТЕЛЬСТВО О БРАКЕ"):
                return JsonResponse({'message': "Загружен неверный файл"}, status=400)

            try:
                medical_insurance = MedicalInsurance.objects.get(session_id=_session_id)
            except Exception:
                return JsonResponse(
                    {'message': "Документ 'Свидетельство о рождении' не найден. Пожалуйста, следуйте инструкции"}, status=400)

            father = medical_insurance.father
            mother =medical_insurance.mother

            if(father_name != father.name):
                return JsonResponse({'message': "Неверно указаны ФИО отца"}, status=400)
            elif(mother_name != mother.name):
                return JsonResponse({'message': "Неверно указаны ФИО матери"}, status=400)

            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except json.JSONDecodeError:
            raise ValueError("Не удалось распознать данные, возможно загружен неверный файл")
        except ValidationError as e:
            raise ValueError(f"Validation error: {e}")

    def check_statement(self, _session_id):
        """
          Функция для обработки заявления
       """
        try:
            data = json.loads(self.json_data)

            if data:
                file_name = data.get('Название')
                applicant_name = data.get('ФИО заявителя')
                kid_name = data.get('ФИО ребенка')
                signature = data.get('Наличие подписи')
                _signature_date = data.get('Дата подписи')
                _kid_birth = data.get('ДР ребенка')


            # Извлечение данных из JSON
            if not ( "заявление" in file_name.lower()):
                return JsonResponse({'message': "Загружен неверный файл"}, status=400)

            signature_date = parse_date(_signature_date, 'Дата подписи')
            if isinstance(signature_date, JsonResponse): return signature_date
            kid_birth = parse_date(_kid_birth, 'ДР ребенка')
            if isinstance(kid_birth, JsonResponse): return kid_birth

            try:
                medical_insurance = MedicalInsurance.objects.get(session_id=_session_id)
            except Exception:
                return JsonResponse(
                    {'message': "Документ 'Свидетельство о рождении' не найден. Пожалуйста, следуйте инструкции"},status=400)

            if(not signature):
                return JsonResponse({'message': 'Подпись не распознана'}, status=400)
            if (signature_date.year != datetime.now().year):
                return JsonResponse(
                    {'message': f"Дата подписи не от этого года"}, status=400)
            elif(kid_name != medical_insurance.child_name):
                return JsonResponse({'message': 'Неверно указаны ФИО ребенка'}, status=400)
            elif (kid_birth != medical_insurance.child_birth_date):
                return JsonResponse({'message': 'Неверно указана дата рождения ребенка'}, status=400)
            elif (applicant_name == medical_insurance.father.name):
                medical_insurance.father.is_applicant = True
                medical_insurance.father.save()
                return JsonResponse({'message': 'SUCCESS'}, status=200)
            elif (applicant_name == medical_insurance.mother.name):
                medical_insurance.mother.is_applicant = True
                medical_insurance.mother.save()
                return JsonResponse({'message': 'SUCCESS'}, status=200)
            else:
                return JsonResponse({'message': 'Неверно указаны ФИО заявителя'}, status=400)

        except json.JSONDecodeError:
            raise ValueError("Не удалось распознать данные, возможно загружен неверный файл")
        except ValidationError as e:
            raise ValueError(f"Validation error: {e}")

    def check_birth_certificate(self, _session_id):
        """
      Функция для обработки св-ва о рождении
      """
        try:
            data = json.loads(self.json_data)
            # Извлечение данных из JSON
            if data:
                file_name = data.get('Название')
                father_name = data.get('ФИО отца')
                mother_name = data.get('ФИО матери')
                child_name = data.get('ФИО ребенка')
                _child_birth_date = data.get('ДР ребенка')

            if(file_name != "СВИДЕТЕЛЬСТВО О РОЖДЕНИИ"):
                return JsonResponse({'message': "Загружен неверный файл"}, status=400)

            child_birth_date = parse_date(_child_birth_date, 'ДР ребенка')
            if isinstance(child_birth_date, JsonResponse): return child_birth_date

            clear_exist_medical_insurance(_session_id)

            father = Parent(
                name = father_name,
                role =Parent.FATHER,
                is_payer = False,
                is_applicant = False
            )
            mother = Parent(
                name= mother_name,
                role=Parent.MOTHER,
                is_payer=False,
                is_applicant=False
            )

            # Создание экземпляра модели
            medical_insurance = MedicalInsurance(
                session_id = _session_id,
                father=father,
                mother=mother,
                child_name=child_name,
                child_birth_date=child_birth_date,
                # Другие поля могут быть заполнены по умолчанию или оставлены пустыми
                contract_period_start=None,
                contract_period_end=None,
                cheque_amount=None,
                policy_number=None,
                medical_organization_data=None,
                is_extract_cheque_uploaded = False,
                is_policy_case = False,
            )

            # Валидация и сохранение модели
            #medical_insurance.full_clean()
            father.save()
            mother.save()

            medical_insurance.save()
            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except json.JSONDecodeError or TypeError :
            raise ValueError("Не удалось распознать данные, возможно загружен неверный файл")
        except ValidationError as e:
            raise ValueError(f"Validation error: {e}")

    def check_cheque_reference(self, _session_id):
        """
      Функция для обработки выписки
      """
        try:
            data = json.loads(self.json_data)
            if data:
                file_name = data.get('Название')
                payer_name = data.get('ФИО плательщика')
                amount = data.get('Сумма')
                date = data.get('Дата оплаты')
                place = data.get('Место оплаты')


            if not ("выписка" in file_name.lower()):
                return JsonResponse({'message': "Загружен неверный файл"}, status=400)

            try:
                medical_insurance = MedicalInsurance.objects.get(session_id=_session_id)
            except Exception:
                return JsonResponse(
                    {'message': "Документ 'Свидетельство о рождении' не найден. Пожалуйста, следуйте инструкции"}, status=400)

            father = medical_insurance.father
            mother =medical_insurance.mother

            if(payer_name != father.name and payer_name != mother.name):
                return JsonResponse({'message': f"Указан другой плательщик. Ожидается: {father.name} или {mother.name}"}, status=400)

            if not amount:
                return JsonResponse({'message': f"Не удалось распознать сумму"}, status=400)

            medical_insurance.cheque_amount = amount
            medical_insurance.is_extract_cheque_uploaded = True
            medical_insurance.save()
            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except json.JSONDecodeError:
            raise ValueError("Не удалось распознать данные, возможно загружен неверный файл")
        except ValidationError as e:
            raise ValueError(f"Validation error: {e}")

    def check_cheque(self, _session_id):
        """
      Функция для обработки чеков
      """
        try:
            data = json.loads(self.json_data)
            if data:
                file_name = data.get('Название')
                payment_method = data.get('Способ оплаты')
                payer_name = data.get('ФИО плательщика')
                _payment_date = data.get('Дата оплаты')
                amount = data.get('Сумма')
                medical_institutions = data.get('Место оплаты')
                is_signature = data.get('Подпись')
                is_print = data.get('Печать')

            if not ("чек" in file_name.lower()):
                return JsonResponse({'message': "Загружен неверный файл"}, status=400)

            payment_date = parse_date(_payment_date, 'Дата оплаты')
            if isinstance(payment_date, JsonResponse): return payment_date

            try:
                medical_insurance = MedicalInsurance.objects.get(session_id=_session_id)
            except Exception:
                return JsonResponse(
                    {'message': "Документ 'Свидетельство о рождении' не найден. Пожалуйста, следуйте инструкции"}, status=400)

            father = medical_insurance.father
            mother =medical_insurance.mother

            if(payment_method == f"Безналично" and medical_insurance.is_extract_cheque_uploaded == False):
                return JsonResponse({'message': "При безналичном расчете требуется банковская выписка"}, status=400)
            if (payer_name != father.name and payer_name != mother.name):
                return JsonResponse(
                    {'message': f"Указан другой плательщик. Ожидается: {father.name} или {mother.name}"}, status=400)
            if (payment_date.year != datetime.now().year):
                return JsonResponse(
                    {'message': f"Год оплаты не равен текущему году"}, status=400)
            if medical_insurance.is_policy_case:
                 if not (medical_insurance.contract_period_start <= payment_date  and
                        payment_date <= medical_insurance.contract_period_end):
                    return JsonResponse(
                    {'message': f"Чек не входит в период действия страховой справки"}, status=400)
            if (amount != medical_insurance.cheque_amount):
                return JsonResponse(
                    {'message': f"Сумма в чеке и сумма в выписке не совпадают"}, status=400)
            if (medical_institutions != medical_insurance.medical_organization_data):
                return JsonResponse(
                    {'message': f"Данные мед. организации не совпадают. Ожидается: {medical_insurance.medical_organization_data}"}, status=400)
            if not is_signature:
                return JsonResponse({'message': f"Отсутствует подпись"},status=400)
            if not is_print:
                return JsonResponse({'message': f"Отсутствует печать"},status=400)

            medical_insurance.cheque_amount = 0
            medical_insurance.is_extract_cheque_uploaded = False
            medical_insurance.save()


        except json.JSONDecodeError:
            raise ValueError("Не удалось распознать данные, возможно загружен неверный файл")
        except ValidationError as e:
            raise ValueError(f"Validation error: {e}")

    def check_payment_reference(self, _session_id):
        """
        Функция для обработки справки об оплате мед услуг
      """
        try:
            data = json.loads(self.json_data)
            if data:
                file_name = data.get('Название')
                payer_name = data.get('ФИО налогоплательщика')
                kid_name = data.get('ФИО ребенка')
                _kid_birth = data.get('ДР ребенка')
                medical_institutions = data.get('Название организации')
                # INN = data.get('ИНН')
                # payer_birth = data.get('ДР налогоплательщика')
                # org_name = data.get('Название организации')
                # summ = data.get('Сумма расходов')
                # some_name = data.get('ФИО выдавшего справку')
                # signature = data.get('Подпись')
                # print = data.get('Печать')




            if not ("справк" in file_name.lower() and "оплат" in file_name.lower()):
                return JsonResponse({'message': "Загружен неверный файл"}, status=400)

            kid_birth = parse_date(_kid_birth, 'ДР ребенка')
            if isinstance(kid_birth, JsonResponse): return kid_birth

            try:
                medical_insurance = MedicalInsurance.objects.get(session_id=_session_id)
            except Exception:
                return JsonResponse(
                    {'message': "Документ 'Свидетельство о рождении' не найден. Пожалуйста, следуйте инструкции"},
                    status=400)

            father = medical_insurance.father
            mother = medical_insurance.mother

            if (payer_name != father.name and payer_name != mother.name):
                return JsonResponse(
                    {'message': f"Указан другой плательщик. Ожидается: {father.name} или {mother.name}"}, status=400)
            elif(kid_name != medical_insurance.child_name):
                return JsonResponse({'message': 'Неверно указаны ФИО ребенка'}, status=400)
            elif (kid_birth != medical_insurance.child_birth_date):
                return JsonResponse({'message': 'Неверно указана дата рождения ребенка'}, status=400)

            medical_insurance.medical_organization_data = medical_institutions
            medical_insurance.save()

            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except json.JSONDecodeError as e:
            raise ValueError(f"Validation error: {e}")
            raise ValueError("Не удалось распознать данные, возможно загружен неверный файл")
        except ValidationError as e:
            raise ValueError(f"Validation error: {e}")

    # Данные ДМС

    def check_policy(self, _session_id):
        """
      Функция для обработки полиса
      """
        try:
            data = json.loads(self.json_data)
            if data:
                file_name = data.get('Название')
                kid_name = data.get('ФИО ребенка')
                _kid_birth =data.get('ДР ребенка')
                _policy_number = data.get('Номер полиса')

                _validity_date1 = data.get('Начало действия страхования')
                _validity_date2 = data.get('Окончание действия страхования')


            if not ("полис" in file_name.lower()):
                return JsonResponse({'message': "Загружен неверный файл"}, status=400)

            kid_birth = parse_date(_kid_birth, 'ДР ребенка')
            if isinstance(kid_birth, JsonResponse): return kid_birth
            validity_date1 = parse_date(_validity_date1, 'Начало действия страхования')
            if isinstance(validity_date1, JsonResponse): return validity_date1
            validity_date2 = parse_date(_validity_date2, 'Окончание действия страхования')
            if isinstance(validity_date2, JsonResponse): return validity_date2

            try:
                medical_insurance = MedicalInsurance.objects.get(session_id=_session_id)
            except Exception:
                return JsonResponse(
                    {'message': "Документ 'Свидетельство о рождении' не найден. Пожалуйста, следуйте инструкции"}, status=400)

            if (kid_name != medical_insurance.child_name):
                return JsonResponse({'message': 'Неверно указаны ФИО ребенка'}, status=400)
            if (kid_birth != medical_insurance.child_birth_date):
                return JsonResponse({'message': 'Неверно указана дата рождения ребенка'}, status=400)
            if (validity_date2 < datetime.now()):
                return JsonResponse(
                    {'message': f"Срок полиса истек"}, status=400)

            medical_insurance.policy_number = _policy_number
            medical_insurance.is_policy_case = True
            medical_insurance.save()

            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except json.JSONDecodeError:
            raise ValueError("Invalid JSON data")
        except ValidationError as e:
            raise ValueError(f"Validation error: {e}")

    def check_policy_reference(self, _session_id):
        """
      Функция для обработки справки от страховой компании
      """
        try:
            data = json.loads(self.json_data)
            if data:
                file_name = data.get('Название')
                payer_name = data.get('ФИО плательщика')
                kid_name = data.get('ФИО ребенка')
                _kid_birth =data.get('ДР ребенка')
                policy_number = data.get('Номер полиса ДМС')
                _validity_date1 = data.get('Дата начала страхования')
                _validity_date2 = data.get('Дата окончания страхования')

            if not ("справк" in file_name.lower() and "страхов" in file_name.lower()):
                return JsonResponse({'message': "Загружен неверный файл"}, status=400)

            kid_birth = parse_date(_kid_birth, 'ДР ребенка')
            if isinstance(kid_birth, JsonResponse): return kid_birth
            validity_date1 = parse_date(_validity_date1, 'Дата начала страхования')
            if isinstance(validity_date1, JsonResponse): return validity_date1
            validity_date2 = parse_date(_validity_date2, 'Дата окончания страхования')
            if isinstance(validity_date2, JsonResponse): return validity_date2

            try:
                medical_insurance = MedicalInsurance.objects.get(session_id=_session_id)
            except Exception:
                return JsonResponse(
                    {'message': "Документ 'Свидетельство о рождении' не найден. Пожалуйста, следуйте инструкции"}, status=400)

            father = medical_insurance.father
            mother =medical_insurance.mother

            if (payer_name != father.name or payer_name != mother.name):
                return JsonResponse(
                    {'message': f"Указан другой плательщик. Ожидается: {father.name} или {mother.name}"}, status=400)
            if (kid_name != medical_insurance.child_name):
                return JsonResponse({'message': 'Неверно указаны ФИО ребенка'}, status=400)
            if (kid_birth != medical_insurance.child_birth_date):
                return JsonResponse({'message': 'Неверно указана дата рождения ребенка'}, status=400)
            if (policy_number != medical_insurance.policy_number):
                return JsonResponse({'message': 'Неверный полис'}, status=400)

            medical_insurance.contract_period_start = validity_date1
            medical_insurance.contract_period_end = validity_date2

            medical_insurance.save()

            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except json.JSONDecodeError:
            raise ValueError("Не удалось распознать данные, возможно загружен неверный файл")
        except ValidationError as e:
            raise ValueError(f"Validation error: {e}")
