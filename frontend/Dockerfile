# Базовый образ для Node.js (этап сборки)
FROM node:18 as build

# Устанавливаем рабочую директорию
WORKDIR /frontend

# Копируем package.json и package-lock.json
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем весь проект
COPY . /frontend/

# Сборка проекта
RUN npm run build

# Используем базовый образ Nginx для обслуживания статических файлов
FROM nginx:alpine

# Копируем собранные файлы в директорию Nginx
COPY --from=build /frontend/build /usr/share/nginx/html

# Открываем порт 80
EXPOSE 80

# Запускаем Nginx
CMD ["nginx", "-g", "daemon off;"]