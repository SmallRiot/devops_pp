import io
import os
from PIL import Image
from django.core.files.base import ContentFile
from pdf2image import convert_from_bytes
from django.conf import settings
from PyPDF2 import PdfReader, PdfWriter

import re

# Определите порядок элементов
order = {
    "birth_certificate": 1,
    "statement": 2,
    "marriage_certificate": 3,
    "consent_to_pers_data_bank_employee": 4,
    "consent_to_pers_data_minor": 5,
    "cheque": 6,
    "bank_reference": 7,
    "cert_of_payment_med_services": 100
}

order_with_polis = {
    "birth_certificate": 1,
    "statement": 2,
    "marriage_certificate": 3,
    "consent_to_pers_data_bank_employee": 4,
    "consent_to_pers_data_minor": 5,
    "insurance_policy_VMI": 6,
    "cert_about_paid_franchise_VMI": 7,
    "cheque": 8,
    "bank_reference": 9
}

def get_order_list(item, order):
    for key in order:
        if key in item:
            suffix = re.findall(r'\d+', item)
            suffix_value = int(suffix[-1]) if suffix else 0
            # Корректируем порядок, если есть числовой суффикс
            return (order[key] + suffix_value - 1, suffix_value)
    return (float('inf'), 0)

class FileConverter:
    """Класс для конвертации файлов в нужный формат."""
    def __init__(self, file=None, name=None):
        self.file = file
        self.name = name
        if self.file:
            self.file_ext = os.path.splitext(self.file.name)[1].lower()
        else:
            self.file_ext = None

    def process_file(self):
        """Обрабатывает файл в зависимости от типа и возвращает список файлов для сохранения."""
        if self.file_ext == '.png':
            # Если уже PNG, возвращаем исходный файл
            return [(self.file, self.file.name)]
        else:
            return self._process_image()

    def _process_image(self):
        """Обработка других изображений (не PNG). Конвертирует изображение в PNG."""
        img = Image.open(self.file)
        img = img.convert("RGB")
        temp_img = io.BytesIO()
        img.save(temp_img, format="PNG")
        temp_img.seek(0)
        filename = f"{self.name}.png"
        return [(ContentFile(temp_img.read()), filename)]

    def convert_images_to_pdf(self, session_id):
        from core.models import MedicalInsurance, Document

        base_folder = os.path.join(settings.MEDIA_ROOT, 'backend/documents', session_id)
        output_pdf_path = os.path.join(base_folder, f'{session_id}_combined.pdf')

        if os.path.exists(output_pdf_path):
            return output_pdf_path  # Возвращаем существующий путь, если файл уже создан

        _all_files = []
        for root, dirs, files in os.walk(base_folder):
            for file in files:
                if file.endswith(".png") or file.endswith(".pdf"):
                    _all_files.append(os.path.join(root, file))

        try:
            medical_insurance = MedicalInsurance.objects.get(session_id=session_id)
        except Exception as e:
            medical_insurance = None


        if medical_insurance and medical_insurance.is_policy_case :
            all_files = sorted(_all_files, key=lambda x: get_order_list(x, order_with_polis))
        else:
            all_files = sorted(_all_files, key=lambda x: get_order_list(x, order))

        pdf_writer = PdfWriter()

        for file in all_files:
            if file.endswith(".png"):
                image = Image.open(file).convert('RGB')
                image_pdf = io.BytesIO()
                image.save(image_pdf, format='PDF')
                image_pdf.seek(0)
                image_pdf_reader = PdfReader(image_pdf)
                for page_num in range(len(image_pdf_reader.pages)):
                    pdf_writer.add_page(image_pdf_reader.pages[page_num])
            else:
                with open(file, 'rb') as pdf:
                    pdf_reader = PdfReader(pdf)
                    pdf_writer.append_pages_from_reader(pdf_reader)

        with open(output_pdf_path, 'wb') as output_pdf_file:
            pdf_writer.write(output_pdf_file)

        # if images:
        #     from core.models import Document
        #     images[0].save(output_pdf_path, save_all=True, append_images=images[1:])


        Document.objects.create(
            name =f'{session_id}_combined.pdf',
            session_id=session_id,
            path=output_pdf_path.replace(settings.MEDIA_ROOT, '')  # Относительный путь для хранения
        )

        return output_pdf_path

