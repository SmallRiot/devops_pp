import os
from django.db import models
import pillow_heif

from core.converters import FileConverter

pillow_heif.register_heif_opener()

class Parent(models.Model):
    FATHER = 'father'
    MOTHER = 'mother'
    ROLE_CHOICES = [
        (FATHER, 'Father'),
        (MOTHER, 'Mother'),
    ]

    name = models.CharField(max_length=255, verbose_name="ФИО родителя")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, verbose_name="Роль")
    is_payer = models.BooleanField(default=False, verbose_name="Плательщик")
    is_applicant = models.BooleanField(default=False, verbose_name="Заявитель")

    def __str__(self):
        return self.name

class MedicalInsurance(models.Model):
    session_id = models.CharField(max_length=100, blank=True, null=True)  # Поле для сессии
    father =models.ForeignKey(Parent, related_name='father_insurances', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Отец")
    mother = models.ForeignKey(Parent, related_name='mother_insurances', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Мать")
    child_name = models.CharField(max_length=255, verbose_name="ФИО ребенка",null=True)
    child_birth_date = models.DateField(verbose_name="Дата рождения ребенка",null=True)
    contract_period_start = models.DateField(verbose_name="Начало периода страховой справки",null=True)
    contract_period_end = models.DateField(verbose_name="Конец периода страховой справки",null=True)
    cheque_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cумма чека",null=True)
    policy_number = models.CharField(max_length=50, verbose_name="Номер полиса ДМС",null=True)
    medical_organization_data = models.TextField(verbose_name="Данные медорганизации",null=True)
    is_extract_cheque_uploaded = models.BooleanField(default=False, verbose_name="Выписка загружена")  # Новое поле
    is_policy_case  = models.BooleanField(default=False, verbose_name="Сценарий с полисом")  # Новое поле

class Document(models.Model):
    name = models.CharField(max_length=100)
    session_id = models.CharField(max_length=100, blank=True, null=True)  # Поле для сессии
    path = models.FileField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            name, ext = os.path.splitext(self.path.name)
            self.name = name

        final_path = f'backend/documents/{self.session_id or "default_session"}/'


        if self.path:
            if self.path.name.endswith('.png'):
                final_filename = f"{self.name}.png"
                self.path.name = os.path.join(final_path, final_filename)
            elif self.path.name.endswith('.pdf'):
                self.path.name = os.path.join(final_path, self.path.name)
            else:
                converter = FileConverter(self.path, self.name)
                converted_files = converter.process_file()

                self.path.delete(save=False)

                for file_content, filename in converted_files:
                    file_path = os.path.join(final_path, filename)
                    self.path.save(file_path, file_content, save=False)


        super().save(*args, **kwargs)
