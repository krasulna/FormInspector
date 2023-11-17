# Form Inspector

Form Inspector - это простой сервис, который принимает данные формы и определяет соответствующий шаблон формы. Кроме того, если совпадения не найдены, сервис возвращает типы полей формы.

## Установка и запуск

### Зависимости

Прежде чем начать, убедитесь, что у вас установлены следующие зависимости:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python](https://www.python.org/downloads/) (для запуска и тестирования без Docker)

### Установка

1. Склонируйте репозиторий:

   ```bash
   git clone https://github.com/krasulna/FormInspector.git
2. Перейдите в каталог проекта:
    ```bash
   cd FormInspector
3. Внесите в файл `db/test_data.json` ваши тестовые данные шаблонов.
4. Запустите Docker Compose:
    ```bash
   docker-compose up -d
    ```
5. Откройте браузер и перейдите по адресу http://localhost:5000/docs для интерактивной документации API.

## Использование API
Вы можете отправить POST-запрос на /get_form, передав данные формы в формате JSON. Например:
```json
{
  "data": {
    "f_name1": "john.doe@example.com",
    "f_name2": "+79123456789"
  }
}
```
API вернет соответствующий шаблон, если он найден, или типы полей, если совпадения не найдены.

## Разработка и тестирование
Если вы хотите запустить проект локально без Docker, убедитесь, что у вас установлен Python, создайте виртуальное окружение, установите зависимости из requirements.txt и запустите приложение.
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate  # для Windows
pip install -r requirements.txt
python app.py
```
