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