# api_yamdb
Групповой проект, работала с https://github.com/myPyL/ (тимлид, работала над отзывами, комментариями и рейтингом) и https://github.com/SergeyMalischev13 (работал над моделями, Views и эндпойнтами). Я осуществляла работу с пользователями. Моей задачей было реализовать регистрацию по электронной почте, куда потом должен приходить код подтверждения. После этого пользователь должен передавать код подтверждения и имя пользователя в POST-запросе, после чего формируется и выдается токен. 

# Технологии
Django
uuid
REST API

# Как подключить:
Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone https://github.com/AnastasyaTerekhova/api_yamdb.git
cd api_yamdb
```

В локальной папке проекта создать и активировать виртуальное окружение:
```bash
# Команды для Windows:
python -m venv env
source env/Scripts/activate

# Команды для Linux и macOS:
python3 -m venv env
source env/bin/activate
```

Обновить пакетный менеджер:
```bash
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:
```bash
pip install -r requirements.txt
```