# ШАГИ ПО УСТАНОВКЕ
1. Клонируйте репозиторий
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
6. Миграции. После создания модели необходимо создать миграцию (для Windows и Мак соответственно)
$ python manage.py makemigrations
$ python manage.py migrate
7. Запустите сервер (для Windows и Мак соответственно)
$ python manage.py runserver
$ python3 manage.py runserver
8. Создать суперадмина (для Windows и Мак соответственно)
$  python manage.py createsuperuser
$  python3 manage.py createsuperuser

# СТРАНИЦЫ
Внешний вид календаря
![image](https://github.com/user-attachments/assets/8798ccf5-daf0-448c-a4ff-b293fcc93ea7)
Главная страница
![image](https://github.com/user-attachments/assets/36097a15-a4be-451b-882c-1405e688ab4e)
Главная страница, вид для мобильных устройств
![image](https://github.com/user-attachments/assets/8636d471-ca82-4960-8a1b-c4b1321ed628)
Вид расширенного блока информации о постановке
![image](https://github.com/user-attachments/assets/5d877359-2fe4-4997-9409-78b2acddc45f)
