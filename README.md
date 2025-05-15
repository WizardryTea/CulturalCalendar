# CulturalCalendar

## Установка

### Шаги по установке

1. Клонируйте репозиторий:
$ git clone https://github.com/WizardryTea/CulturalCalendar

2. Создайте виртуальное окружение (для Windows и Мак соответственно)
$  python -m venv venv
$  python3 -m venv venv

3. Активируйте виртуальное окружение (для Windows и Мак соответственно)
$  source venv/scripts/activate
$  source venv/bin/activate

4. Перейдите в директорию проекта
cd foodie

5. Установите зависимости
$  pip install -r requirements.txt

6. Создайте миграции. После создания модели необходимо создать миграцию (для Windows и Мак соответственно)
$ python manage.py makemigrations
$ python manage.py migrate

7. Запустите сервер (для Windows и Мак соответственно)
$ python manage.py runserver
$ python3 manage.py runserver

8. Создайте суперадмина (для Windows и Мак соответственно)
$  python manage.py createsuperuser
$  python3 manage.py createsuperuser

### Запуск

Для запуска сервера необходимо:
1. Перейти в папку server,
2. Ввести команду
$ python manage.py runserver

Теперь сервер доступен по адресу http://127.0.0.1:8000/ в браузере.

3. При желании для удобного тестирования и ознакомления с функционалом можно воспользоваться готовыми тестовыми данными. Доступные команды:

1. Очистка данных
$ python manage.py reset_data
Сообщение: "Данные очищены!"

2. Загрузка тестовых данных
$ python manage.py load_test_data
Сообщение: "Тестовые данные успешно загружены!"


### Внешний вид

Главная страница
![image](https://github.com/user-attachments/assets/f3df9a06-6019-4e0d-8dbe-0b9ed129b06b)

Страница "Календарь событий"
![image](https://github.com/user-attachments/assets/4f29e614-3eb4-4807-950d-f9be36acfe0d)

Сраница постановки
![image](https://github.com/user-attachments/assets/ab3997e3-d1a6-4db9-a379-a8fd48ac3f9d)

Страница добавления представения
![image](https://github.com/user-attachments/assets/9846d275-6a95-4bc4-8999-86c9796d831e)

Шапка сайта
![image](https://github.com/user-attachments/assets/2b37b298-3146-4af3-bba0-d62fdc4170c4)

Адаптация меню
![image](https://github.com/user-attachments/assets/6dacb81b-7ef8-47d9-9b8a-ebea51fb4726)

Футер сайта (политика конфиденциальности и условия использования доступны для загрузки)
![image](https://github.com/user-attachments/assets/0d905a4e-0436-45c5-920a-c54dde97a083)

Администрирование Django
![image](https://github.com/user-attachments/assets/1c741047-8315-4c3a-b4c7-3509d9fbefaa)
