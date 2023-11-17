import datetime
from typing import Dict

from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
from tinydb import TinyDB, Query
import json
import uvicorn

app = FastAPI()
db = TinyDB('db/db.json')


class FormData(BaseModel):
    data: Dict[str, str]


def initialize_database():
    with open('db/test_data.json') as file:
        data = json.load(file)
        db.insert_multiple(data)


def find_matching_template(data):
    templates = db.all()
    for template in templates:
        template_name = template.get('name')
        template_values = {k: v for k, v in template.items() if k != 'name'}
        data_values = {k: determine_field_type(v) for k, v in data.items()}

        # Проверяем, что все значения ключей ШАБЛОНА подходят под значения валидации ЗАПРОСА
        if all(data_values[data_key] == template_values[template_key] for template_key, data_key in
               zip(template_values.keys(), data_values.keys())):
            return template_name

    return None


def determine_field_type(value):
    if isinstance(value, str):
        if "@" in value and "." in value:
            return "email"
        elif value.startswith("+7") and value[1:].replace(" ", "").isdigit() and len(value) == 12:
            return "phone"
        elif "." in value or "-" in value:
            try:
                datetime.datetime.strptime(value, "%Y-%m-%d")
                return "date"
            except ValueError:
                try:
                    datetime.datetime.strptime(value, "%d.%m.%Y")
                    return "date"
                except ValueError:
                    return "text"
        else:
            return "text"
    return "text"


@app.post("/get_form")
async def get_form(data: FormData):
    matching_template = find_matching_template(data.data)
    if matching_template:
        return {"template_name": matching_template}
    else:
        field_types = {field_name: determine_field_type(value) for field_name, value in data.data.items()}
        return field_types

if __name__ == '__main__':
    initialize_database()
    uvicorn.run(app, host='0.0.0.0', port=5000, log_level='info')
