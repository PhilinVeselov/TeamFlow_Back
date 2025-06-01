FROM python:3.11-slim

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Копируем скрипт старта
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Указываем PYTHONPATH
ENV PYTHONPATH=/app

# Запуск через start.sh
ENTRYPOINT ["bash", "/start.sh"]
