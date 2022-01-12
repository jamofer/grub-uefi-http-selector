import re
from typing import List

import pydantic.typing

import fastapi
from pydantic import BaseModel
from starlette.responses import PlainTextResponse

import boot_script
import storage


app = fastapi.FastAPI()


def default_target():
    target = storage.get('default_target')
    if re.match(r'\d+', target) is not None:
        return str(int(target) - 1)


@app.get('/boot_source.cfg')
def boot_source():
    return PlainTextResponse(
        boot_script.generate(
            default_target(),
            storage.get('boot_selection_timeout')
        )
    )


@app.get('/api/get/{parameter}')
def get_parameter(parameter):
    return {'value': storage.get(parameter)}


class Parameter(BaseModel):
    parameter: str
    value: pydantic.typing.Any


@app.post('/api/set')
def set_parameter(parameter: Parameter):
    storage.save(parameter.parameter, parameter.value)


@app.get('/api/configuration')
def configuration():
    return {
        'targets': storage.get('targets'),
        'boot_selection_timeout': storage.get('boot_selection_timeout'),
        'default_target': storage.get('default_target')
    }


class Target(BaseModel):
    order_id: int
    name: str


class GuhsConfiguration(BaseModel):
    targets: List[Target]
    boot_selection_timeout: int
    default_target: str


@app.post('/api/configuration')
def configure(request: GuhsConfiguration):
    request_json = request.dict()
    storage.save('targets', request_json['targets'])
    storage.save('boot_selection_timeout', request_json['boot_selection_timeout'])
    storage.save('default_target', request_json['default_target'])
