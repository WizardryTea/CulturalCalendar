# Используем официальный python-образ
FROM python:3.9
ENV PYTHONUNBUFFERED 1

# Создаем и устанавливаем рабочую директорию
RUN mkdir /CulturalCalendar
WORKDIR /CulturalCalendar

# Копируем нужные файлы в контейнер
COPY requirements.txt /CulturalCalendar/

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем наше приложение в контейнер
COPY . .

# port where the Django app runs  
EXPOSE 8001 
#EXPOSE 3306

# Указываем команду для выполнения Django-приложения 
CMD python server/manage.py runserver 127.0.0.1:8001
#CMD ["python","server/manage.py","runserver","127.0.0.1:8000"]