# Используем официальный образ Python из Docker Hub
FROM python:3.10

# Устанавливаем рабочую директорию в контейнере
WORKDIR /backend

# Копируем файлы requirements.txt и entrypoint.sh в контейнер
COPY requirements.txt /backend/
COPY entrypoint.sh /backend/

RUN pip install --upgrade pip


# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта в контейнер
COPY . /backend/

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1

# Открываем порт, на котором будет работать приложение
EXPOSE 8000

# Команда для запуска контейнера
ENTRYPOINT ["sh", "entrypoint.sh"]