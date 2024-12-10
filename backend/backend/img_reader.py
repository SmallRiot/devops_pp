import pytesseract
import cv2
import os
import numpy as np
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # resized = cv2.resize(gray, (1000, 1418))

    sharpened = cv2.filter2D(gray, -1, kernel=(1, 1))

    binary = cv2.threshold(sharpened, 127, 255, cv2.THRESH_BINARY)[1]

    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    
    return closing

def preprocess_roi_image(image):
    # Apply adaptive thresholding for better text extraction
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return binary

def extract_date_from_text(text):
    date_patterns = [
        r'\b(\d{2}\.\d{2}\.\d{4})\b',  # DD.MM.YYYY
        r'\b(\d{2}/\d{2}/\d{4})\b',   # DD/MM/YYYY
        r'\b(\d{4}-\d{2}-\d{2})\b',   # YYYY-MM-DD
        r'\b(\d{2}\.\d{2}\.\d{2})\b',  # DD.MM.YY
        r'\b(\d{2}/\d{2}/\d{2})\b'    # DD/MM/YY
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    
    return None

def extract_company_name(lines):
    company_prefixes = ['ООО', 'ЗАО', 'ИП', 'ТОО', 'АО', 'ОАО']
    
    for line in lines[:3]:
        for prefix in company_prefixes:
            modified_line = line.replace('0', 'О')
            if prefix in modified_line:
                company_name = modified_line.split(prefix)[-1].strip()
                return f"{prefix} {company_name}".strip()
    
    return None

def extract_text_from_receipt(image_path):
    try:
        image = cv2.imread(image_path)
        if image is None:
            return f"Ошибка: Не удалось прочитать изображение из {image_path}"
        preprocessed_image = preprocess_image(image)
        text = pytesseract.image_to_string(preprocessed_image, lang='rus')

        lines = text.splitlines()

        company_name = None
        amount = None
        payment_method = None
        date = None
        
        company_name = extract_company_name(lines)
        for i, line in enumerate(lines):
            if "ИТОГ" in line:
                amount = re.search(r'\d+[\.,]?\d*', line)
                if amount:
                    amount = amount.group(0)
                if i + 2 < len(lines):
                    payment_method = lines[i + 2].strip()
                    payment_method = re.split(r'[\W_]', payment_method)[0].strip()

        date = extract_date_from_text(text)

        extracted_info = {
            'company_name': company_name,
            'amount': amount,
            'payment_method': payment_method,
            'date': date
        }

        extracted_info = {k: v for k, v in extracted_info.items() if v is not None}
        
        return extracted_info
    except Exception as e:
        return f"Ошибка в извлечении файла: {e}"
    
def resize_image(image, target_width=1000, target_height=1418):
    return cv2.resize(image, (target_width, target_height))

def extract_text_from_roi(image_path, roi, original_size=(1000, 1418)):
    image = cv2.imread(image_path)
    if image is None:
        return f"Ошибка: Не удалось прочитать изображение из {image_path}"

    resized_image = resize_image(image)

    scale_x = resized_image.shape[0] / original_size[1]
    scale_y = resized_image.shape[1] / original_size[0]

    x, y, w, h = roi
    x = int(x * scale_x)
    y = int(y * scale_y)
    w = int(w * scale_x)
    h = int(h * scale_y)

    roi_image = resized_image[y:y+h, x:x+w]
    print(roi_image.shape)

    try:
        preprocessed_image = preprocess_image(roi_image)
        text = pytesseract.image_to_string(preprocessed_image, lang='rus')
        cleaned_text = re.sub(r'[^\w\s\d]', '', text)
        cleaned_text = cleaned_text.replace('_','')
        cleaned_text = cleaned_text.lstrip()
        return cleaned_text
    except Exception as e:
        return f"Ошибка в извлечении файла: {e}"

def write_text_to_file(text_dict, output_file):
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as file:
            for field, text in text_dict.items():
                file.write(f"{field}:\n{text}\n")
        print(f"Текст записан в {output_file}")
    except Exception as e:
        print(f"Ошибка записи файла: {e}")

def prompt_user_for_file_type():
    while True:
        choice = input("Вы хотите загрузить чек (C) или другой файл (F)? ").strip().lower()
        if choice in ['c', 'f']:
            return choice
        else:
            print("Неверный выбор. Пожалуйста, введите 'C' для чека или 'F' для другого файла.")

def main():
    file_path = input("Введите путь к файлу: ")

    if not os.path.exists(file_path):
        print("Файл не найден.")
        return

    file_type = prompt_user_for_file_type()

    if file_type == 'c':
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
            extracted_text = extract_text_from_receipt(file_path)
            print("Извлечённый текст:")
            print(extracted_text)

            output_file = r'C:\Users\USER\Desktop\extracted_receipt_text.txt'
            write_text_to_file({'receipt_text': extracted_text}, output_file)
        else:
            print("Неподходящий формат файла.")
            return
    else:
        rois = {
            'title': (330, 180, 400, 90),
            'surname': (90, 340, 810, 30),
            'fullname': (90, 380, 810, 40),
            'father_surname': (145, 695, 810, 39),
            'father_fullname': (90, 738, 810, 30),
            'mother_surname': (145, 845, 810, 40),
            'mother_fullname': (90, 885, 810, 39)
        } 

        marriage_rois = {
            'title' : (330, 180, 400, 90),
            'father_surname': (145, 695, 810, 39),
            'father_fullname': (90, 738, 810, 30),
            'mother_surname': (145, 845, 810, 40),
            'mother_fullname': (90, 885, 810, 39)
        }

        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
            extracted_text = {}
            for field, roi in rois.items():
                text = extract_text_from_roi(file_path, roi)
                if 'surname' in field:
                    words = text.split()
                    if words:
                        largest_word = max(words, key=len)
                        text = largest_word
                extracted_text[field] = text
        else:
            print("Неподходящий формат файла.")
            return

        print("Извлечённый текст:")
        print(extracted_text)

        output_file = r'C:\Users\USER\Desktop\extracted_text.txt'
        write_text_to_file(extracted_text, output_file)

if __name__ == "__main__":
    main()