import datetime

from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
from tinydb import TinyDB, Query
import json
import uvicorn

app = FastAPI()
db = TinyDB('db.json')

class FormData(BaseModel):
    f_name1: str
    f_name2: str

def initialize_database():
    with open('test_data.json') as file:
        data = json.load(file)
        db.insert_multiple(data)

def find_matching_template(data):
    templates = db.all()
    for template in templates:
        template_values = set(template.values())
        template_name = template.get('name')
        data_values = set(determine_field_type(value) for value in data.values())
        if template_name and template_values == data_values:
            return template_name
    return None







def determine_field_type(value):
    if isinstance(value, str):
        if "@" in value and "." in value:
            return "email"
        elif value.startswith("+7") and value[1:].replace(" ", "").isdigit() and len(value) == 12:
            return "phone"
        elif "." in value and "-" in value:
            try:
                datetime.datetime.strptime(value, "%Y-%m-%d")
                return "date"
            except ValueError:
                pass
        else:
            return "text"
    return "text"

@app.post("/get_form")
async def get_form(data: FormData):
    matching_template = find_matching_template(data.model_dump())
    if matching_template:
        return {"template_name": matching_template}
    else:
        field_types = {field_name: determine_field_type(value) for field_name, value in data.model_dump().items()}
        return field_types

if __name__ == '__main__':
    initialize_database()
    uvicorn.run(app, host='0.0.0.0', port=5000, log_level='info')
