**Доска обновлений**

**Технологии проекта**

Django = 4.2.21
django-bootstrap5 = 25.1
django-extensions = 4.1
djangorestframework = 3.16.0



**Установка**

1) Создать виртуальное окружение
```bash
py -m venv venv
```
2) Активировать виртуальное окружение
```bash
.\venv\Scripts\activate
```
2.1) Опционально: обновить pip
```bash
py -m pip install --upgrade pip  
```
3) Установить зависимости
```bash
pip install -r .\requirements.txt
```
4) Сделать миграции
```bash
py manage.py migrate
```
5) Задать данные администратора
```bash
py manage.py createsuperuser
```
6) по данным администратора зайти и заполнить данные Категорий и возможных статусов

6.1) Запустить сервер
```bash
py manage.py runserver
```
6.2) Зайти в админ панель
```bash
http://127.0.0.1:8000/admin
```

**Доступные страницы**
Страница логина
http://127.0.0.1:8000/announcement/login/
Страница регистрации
http://127.0.0.1:8000/announcement/register/
Страница с объявлениями
http://127.0.0.1:8000/announcement/list/
Детальная информация об объявлении
http://127.0.0.1:8000/announcement/4/detail/
Страница с поступившими ит отправленными заявками
http://127.0.0.1:8000/announcement/proposal/
Создание нового объявления
http://127.0.0.1:8000/announcement/create/