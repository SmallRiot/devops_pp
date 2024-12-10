# Базовый образ для Node.js
FROM node:18

# Устанавливаем рабочую директорию
WORKDIR /frontend

# Копируем package.json и package-lock.json
COPY package*.json /frontend/

# Устанавливаем зависимости
RUN npm install

# Копируем весь проект
COPY . /frontend/

# Открываем порт
EXPOSE 3000

# Команда запуска для разработки
CMD ["npm", "start"]
