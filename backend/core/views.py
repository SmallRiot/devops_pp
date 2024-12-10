import json
import os
import uuid
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from core.models import Document
from core.serializers import DocumentSerializer
from core.converters import FileConverter
from core.doc_services import DataInspector,remove_dir,check_is_file_exist_and_delete,delete_garbage_file
from backend.transcriber import *


def index(request):
    if not request.session.session_key:
        request.session.create()
    return HttpResponse("Добро пожаловать")

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = (MultiPartParser,)

    def create(self, request, *args, **kwargs):

        if not request.session.session_key:
            request.session.create()

        session_id = request.session.session_key
        request.session['session_id'] = session_id

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name, ext = os.path.splitext(request.FILES.get('path').name)

        self.perform_create(serializer,name, session_id)
        auth_token = ''

        # Первое заявление
        statement1 = '''
        {
          "Название": "Заявление",
          "Дата": "2023-10-01",
          "Наличие подписи": true,
          "Дата подписи": "2024-11-03",
          "ФИО заявителя": "Цветков Андрей Георгиевич",
          "ФИО ребенка": "Цветков Денис Андреевич",
          "ДР ребенка": "2011-12-03"
        }
        '''
        # Второе заявление
        statement2 = '''
        {
          "Название": "Заявление",
          "Дата": "2024-08-20",
          "Наличие подписи": false,
          "Дата подписи": "2024-11-03",
          "ФИО заявителя": "Петров Сергей Александрович",
          "ФИО ребенка": "Петрова Анна Сергеевна",
          "ДР ребенка": "2024-08-20"
        }
        '''
        # Первое св. о браке
        marriage_certificate1 = '''
        {
          "Название": "СВИДЕТЕЛЬСТВО О ЗАКЛЮЧЕНИИ БРАКА",
          "ФИО мужа": "Цветков Андрей Георгиевич",
          "ФИО жены": "Цветкова Виктория Александровна"
        }
        '''
        # Первое св. о рождении
        birth_certificate1 = '''
        {
          "Название": "СВИДЕТЕЛЬСТВО О РОЖДЕНИИ",
          "ФИО ребенка": "Цветков Денис Андреевич",
          "ДР ребенка": "03/12/2011",
          "ФИО отца": "Цветков Андрей Георгиевич",
          "ФИО матери": "Цветкова Виктория Александровна"
        }
        '''
        # Второе св. о браке
        marriage_certificate2 = '''
        {
          "Название документа": "СВИДЕТЕЛЬСТВО О ЗАКЛЮЧЕНИИ БРАКАa",
          "ФИО мужа": "Белов Сергей Юрьевич",
          "ФИО жены": "Белова Александра Андреевна"
        }
        '''
        # второе св. о рождении
        birth_certificate2 = '''
        {
          "Название документа": "СВИДЕТЕЛЬСТВО О РОЖДЕНИИa",
          "ФИО ребенка": "Белова Марина Сергеевна",
          "ДР ребенка": "30/07/2015",
          "ФИО отца": "Белов Сергей Юрьевич",
          "ФИО матери": "Белова Александра Андреевна"
        }
        '''
        # чек
        cheque1 ='''
        {
          "Название": "Чек",
          "Способ оплаты": "Безналично",
          "ФИО плательщика": "Цветков Андрей Георгиевич",
          "Дата оплаты": "30/07/2024",
          "Сумма": "16000.00",
          "Место оплаты": "Больница 1",
          "Подпись": true,
          "Печать": true
        }
        '''
        cheque2 ='''
        {
          "Название": "Чек",
          "Способ оплаты": "Наличными",
          "ФИО плательщика": "Цветков Андрей",
          "Дата оплаты": "30/07/2024",
          "Сумма": "16000.00",
          "Место оплаты": "Больница 1",
          "Подпись": true,
          "Печать": false
        }
        '''
        bank_reference1 ='''
        {
          "Название": "Выписка",
          "ФИО плательщика": "Цветков Андрей Георгиевич",
          "Дата оплаты": "30/07/2024",
          "Сумма": "16000.00",
          "Место оплаты": "Больница 1"
        }
        '''
        bank_reference2 ='''
        {
          "Название": "Выписка",
          "ФИО плательщика": "Цветков Иван Георгиевич",
          "Дата оплаты": "30/05/2024",
          "Сумма": "122000.00",
          "Место оплаты": "Больница 2"
        }
        '''
        cert_of_payment_med_services1 ='''
        {
          "Название": "Справка об оплате медицинских услуг",
          "ФИО налогоплательщика": "Цветков Андрей Георгиевич",
          "ДР налогоплательщика": "1988-12-03",
          "Название организации": "Организация",
          "Место оплаты": "Больница 1",
          "ИНН": "111111111111",
          "Паспортные данные": "1111 222222",
          "Сумма расходов": "16000.00",
          "ФИО выдавшего справку": "Иванов Иван Иванович",
          "ФИО ребенка": "Цветков Денис Андреевич",
          "ДР ребенка": "03/12/2011",
          "Подпись": true,
          "Печать": true
        }
        '''
        insurance_policy_VMI1 ='''
        {
          "Название": "Полис ДМС",
          "ФИО ребенка": "Цветков Денис Андреевич",
          "ДР ребенка": "03/12/2011",
          "Номер полиса": "4400 2888 9654 3821",
          "Начало действия страхования": "25/01/2020",
          "Окончание действия страхования": "25/01/2030"
        }
        '''
        insurance_policy_VMI2 ='''
        {
          "Название": "Полис ДМС",
          "ФИО ребенка": "Иванов Иван Иванович",
          "ДР ребенка": "15/05/2010",
          "Номер полиса": "1111 2888 9654 3821",
          "Начало действия страхования": "25/01/2020",
          "Окончание действия страхования": "25/01/2030"
        }
        '''
        cert_about_paid_franchise_VMI1 ='''
        {
          "Название": "Справка от страховой компании",
          "ФИО плательщика": "Цветков Андрей Георгиевич",
          "ФИО ребенка": "Цветков Денис Андреевич",
          "ДР ребенка": "03/12/2011",
          "Номер полиса ДМС": "4400 2888 9654 3821",
          "Дата начала страхования": "25/01/2020",
          "Дата окончания страхования": "25/01/2030"
        }
        '''
        cert_about_paid_franchise_VMI2 ='''
        {
          "Название": "Справка от страховой компании",
          "ФИО плательщика": "Егоров Андрей Георгиевич",
          "ФИО ребенка": "Иванов Иван Иванович",
          "ДР ребенка": "15/05/2010",
          "Номер полиса ДМС": "4400 2888 9654 3821",
          "Дата начала страхования": "25/01/2020",
          "Дата окончания страхования": "25/01/2023"
        }
        '''


        saved_instance = serializer.instance

        rquid = str(uuid.uuid4())

        access_token = get_access_token(rquid, auth_token)

        img_path = saved_instance.path.name
        if(ext == '.pdf'):
            sourse_id = load_pdf(access_token, img_path)
            if ("statement" in saved_instance.name):
                info = get_statement_info(access_token, sourse_id)
            elif ("cert_about_paid_franchise_VMI" in saved_instance.name):
                info = get_reference_six_info(access_token, sourse_id)
            else:
                info = get_info(access_token, sourse_id)
        else:
            sourse_id = load_img(access_token, img_path)

        if ("marriage_certificate" in saved_instance.name):
            if (ext == '.pdf'):
                res = marriage_response(info, auth_token)
            else:
                res = process_marriage_certificate(access_token, sourse_id)

            inspector = DataInspector(json.dumps(res))
            response = inspector.check_marriage_certificate(session_id)
            if (response.status_code == 400):
                delete_garbage_file(saved_instance.id)
                return response
        elif ("statement" in saved_instance.name and ext == '.pdf'):
            if (ext == '.pdf'):
                res = statement_response(info, auth_token)
                inspector = DataInspector(json.dumps(res))
                response = inspector.check_statement(session_id)
            else:
                response = JsonResponse({'message': "Неверный формат файла, ожидается: PDF"}, status=400)


            if (response.status_code == 400):
                delete_garbage_file(saved_instance.id)
                return response
        if ("birth_certificate" in saved_instance.name):
            if (ext == '.pdf'):
                res = birth_response(info, auth_token)
            else:
                res = process_birth_certificate(access_token, sourse_id)
            inspector = DataInspector(json.dumps(res))
            response = inspector.check_birth_certificate(session_id)
            if (response.status_code == 400):
                delete_garbage_file(saved_instance.id)
                return response
        elif ("cert_of_payment_med_services" in saved_instance.name):
            if(ext == '.pdf'):
                res = double_page_response(info, auth_token)
                inspector = DataInspector(json.dumps(res))
                response = inspector.check_payment_reference(session_id)
            else:
                response = JsonResponse({'message': "Неверный формат файла, ожидается: PDF"}, status=400)


            if (response.status_code == 400):
                delete_garbage_file(saved_instance.id)
                return response
        elif ("insurance_policy_VMI" in saved_instance.name):
            if (ext == '.pdf'):
                res = insurance_response(info, auth_token)
            else:
                res = process_insurance(access_token, sourse_id)

            inspector = DataInspector(json.dumps(res))
            response = inspector.check_policy(session_id)
            if (response.status_code == 400):
                delete_garbage_file(saved_instance.id)
                return response
        elif ("cert_about_paid_franchise_VMI" in saved_instance.name):
            if(ext == '.pdf'):
                res = reference_six_response(info, auth_token)
                inspector = DataInspector(json.dumps(res))
                response = inspector.check_policy_reference(session_id)
            else:
                response = JsonResponse({'message': "Неверный формат файла, ожидается: PDF"}, status=400)
            if (response.status_code == 400):
                delete_garbage_file(saved_instance.id)
                return response
        elif ("cheque" in saved_instance.name):
            if (ext == '.pdf'):
                res = receipt_response(info, auth_token)
            else:
                res = process_reciept(access_token, sourse_id)

            inspector = DataInspector(json.dumps(res))
            response = inspector.check_cheque(session_id)
            if (response.status_code == 400):
                delete_garbage_file(saved_instance.id)
                return response
        elif ("bank_reference" in saved_instance.name):
            if (ext == '.pdf'):
                res = reference_response(info, auth_token)
            else:
                res = process_reference(access_token, sourse_id)

            inspector = DataInspector(json.dumps(res))
            response = inspector.check_cheque_reference(session_id)
            if (response.status_code == 400):
                delete_garbage_file(saved_instance.id)
                return response
        # if ("marriage_certificate" in saved_instance.name):
        #     # if (ext == '.pdf'):
        #     #     res = marriage_response(info, auth_token)
        #     # else:
        #     #     res = process_marriage_certificate(access_token, sourse_id)
        #     inspector = DataInspector(marriage_certificate1)
        #     response = inspector.check_marriage_certificate(session_id)
        #     if (response.status_code == 400):
        #         delete_garbage_file(saved_instance.id)
        #         return response
        # elif ("statement" in saved_instance.name):
        #     # res = statement_response(info, auth_token)
        #
        #     inspector = DataInspector(statement1)
        #     response = inspector.check_statement(session_id)
        #     if (response.status_code == 400):
        #         delete_garbage_file(saved_instance.id)
        #         return response
        # if ("birth_certificate" in saved_instance.name):
        #     # if (ext == '.pdf'):
        #     #     res = birth_response(info, auth_token)
        #     # else:
        #     #     res = process_birth_certificate(access_token, sourse_id)
        #
        #     inspector = DataInspector(birth_certificate1)
        #     response = inspector.check_birth_certificate(session_id)
        #     if (response.status_code == 400):
        #         delete_garbage_file(saved_instance.id)
        #         return response
        # elif ("cert_of_payment_med_services" in saved_instance.name):
        #     #res = double_page_response(access_token, sourse_id)
        #
        #     inspector = DataInspector(cert_of_payment_med_services1)
        #     response = inspector.check_payment_reference(session_id)
        #     if (response.status_code == 400):
        #         delete_garbage_file(saved_instance.id)
        #         return response
        # elif ("insurance_policy_VMI" in saved_instance.name):
        #     # if (ext == '.pdf'):
        #     #     res = insurance_response(info, auth_token)
        #     # else:
        #     #     res = process_insurance(access_token, sourse_id)
        #
        #     # res_max = sup_response(res, auth_token)
        #
        #     inspector = DataInspector(insurance_policy_VMI1)
        #     response = inspector.check_policy(session_id)
        #     if (response.status_code == 400):
        #         delete_garbage_file(saved_instance.id)
        #         return response
        # elif ("cert_about_paid_franchise_VMI" in saved_instance.name):
        #     # res = reference_six_response(access_token, sourse_id)
        #
        #     inspector = DataInspector(cert_about_paid_franchise_VMI1)
        #     response = inspector.check_policy_reference(session_id)
        #     if (response.status_code == 400):
        #         delete_garbage_file(saved_instance.id)
        #         return response
        # elif ("cheque" in saved_instance.name):
        #     # if (ext == '.pdf'):
        #     #     res = receipt_response(info, auth_token)
        #     # else:
        #     #     res = process_reciept(access_token, sourse_id)
        #
        #     inspector = DataInspector(cheque1)
        #     response = inspector.check_cheque(session_id)
        #     if (response.status_code == 400):
        #         delete_garbage_file(saved_instance.id)
        #         return response
        # elif ("bank_reference" in saved_instance.name):
        #     # if (ext == '.pdf'):
        #     #     res = reference_response(info, auth_token)
        #     # else:
        #     #     res = process_reference(access_token, sourse_id)
        #
        #     inspector = DataInspector(bank_reference1)
        #     response = inspector.check_cheque_reference(session_id)
        #     if (response.status_code == 400):
        #         delete_garbage_file(saved_instance.id)
        #         return response

        headers = self.get_success_headers(serializer.data)

        # if("marriage_certificate" in saved_instance.name):
        #     inspector = DataInspector(marriage_certificate1)
        #     response= inspector.check_marriage_certificate(session_id)
        #     if (response.status_code == 400):
        #         delete_garbage_file(saved_instance.id)
        #         return response
        # elif ("statement" in saved_instance.name):
        #     inspector = DataInspector(statement1)
        #     response= inspector.check_statement(session_id)
        #     if(response.status_code == 400):
        #         delete_garbage_file(saved_instance.id)
        #         return response
        # elif ("birth_certificate" in saved_instance.name):
        #     inspector = DataInspector(birth_certificate1)
        #     response= inspector.check_birth_certificate(session_id)
        #     if (response.status_code == 400):
        #         delete_garbage_file(saved_instance.id)
        #         return response

        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer,file_name, session_id):
        check_is_file_exist_and_delete(file_name,session_id)
        serializer.save(session_id=session_id)



class CombineImagesToPDFView(APIView):
    def get(self, request):
        try:
            converter = FileConverter()
            output_pdf_path = converter.convert_images_to_pdf(request.session.session_key)
            if not os.path.exists(output_pdf_path):
                return JsonResponse({'error': 'PDF file could not be created.'},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            with open(output_pdf_path, 'rb') as pdf_file:
                response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{request.session.session_key}_combined.pdf"'
                return response
        except Document.DoesNotExist:
            return JsonResponse({'error': 'Session ID not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserDataView(APIView):

    def delete(self, request):
        try:
            session_id=request.session.session_key
            base_folder = os.path.join(settings.MEDIA_ROOT, 'backend/documents', session_id)

            response = remove_dir(session_id, base_folder)
            if response:
                return response
            return JsonResponse({'message': 'Success'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
