# agora-hack
#### Данный репозиторий является решением "Кейс №1: Микросервис автоматического сопоставления товаров" от команды "ML Princess [Napoleon IT]"

### Содержание
- [user guide](#user-guide):
    * [Структура репозитория](#структура-репозитория)
    * [Инструкция по использованию репозитория в docker](#docker-run)


# User guide
### Структура репозитория
- [app](./app/) - папка содержащая реализацию бэка, всю логику работы моделей, инициализацию моделей
- [backend.py](backend.py) - вспомогательный файл для запуска сервиса
- [docker-compose.yml](docker-compose.yml) - конфиг докера для сборки и поднятия сервиса
- [Dockerfile](Dockerfile) - докер файл сервиса, отвечающий за окружение и установку нужных пакетов
- [requirements.txt](requirements.txt) - файл со всеми необходимыми библиотеками для работы сервиса
- [install_models.sh](install_models.sh) - скрипт для выгрузки моделей с облака
- [start_service.sh](start_service.sh) - bash скрипт с выгрузкой моделей с диска и запуском сервиса сопоставления (запускается внутри `docker-compose.yml`)
- [product_matches_path.json](product_matches_path.json) - json с сопоставленными классами к `reference_id`
### Docker run
Для того чтобы поднять сервис на локальной/удаленной машине нужно:
- убедиться, что указанные порты в ```docker-compose.yml``` доступны на вашей машине
- У вас должен быть `.env`:
```
MODEL_PATH=./models/arcface_bert/model.pt
BASE_FILE=./models/source/base_file.csv
PRODUCTS_MATCHES_PATH=./models/source/product_matches_path.json
```
- запустить скрипт сборки docker контейнеров:
```
docker-compose build
```
- запустить скрипт поднятия сервиса:
```
docker-compose up -d
```
- Поздравляем, сервис поднят