<p align="center">
  <img src='https://github.com/ruha02/forpost/blob/main/apps/web/src/assets/readme_logo.png?raw=true' height="auto" width="100px" style="border-radius:50%">
</p>


## Описание
ФОРПОСТ - сервис, который позволяет программисту, менеджеру проекта или инженеру по ИБ провести проверку на уязвимости своего сервиса и его кода.

## Запуск
Для локальной установки вам необходимо использовать Docker версии не ниже 20. Инструкцию по установке можете найти [здесь](https://docs.docker.com/engine/install/)
Далее необходимо выполнить следующие команды:
```
git clone https://github.com/ruha02/forpost.git
cd forpost
```
Далее вам следует заполнить файл переменных окружений. Например, следующим образом (пример есть в файле .example.env):
***.env***
```
PGSQL_URL=postgresql://admin:password@pgsql/database
API_SECRET_KEY=BIGsecretkey$
API_ALGORITHM=HS256
PROJECT_NAME=forpost
API_MEDIA_URL=http://localhost:80/files/
API_MEDIA_PATH=media
API_BASE_URL=http://localhost:9000/
API_ACCESS_TOKEN_EXPIRE_MINUTES=6000
API_REFRESH_TOKEN_EXPIRE_MINUTES=36000
PGSQL_USERNAME=admin 
PGSQL_PASSWORD=password
PGSQL_DATA=/data/
PGSQL_DATABASE=database
API_BASE_URL_FRONT=http://api:9000
```
Теперь можно переходить к сборке проекта. Для этого выполните следующие команды:
```
docker compose up -d --build
```
Для заполнения базы данных демо данными необходимо выполнить следующие команды:
- для windows:
```
migrate.cmd
```
- для linux:
```
chmod +x migrate.sh
./migrate.sh
```