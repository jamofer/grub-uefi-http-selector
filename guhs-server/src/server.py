from typing import List

import pydantic.typing

import fastapi
from pydantic import BaseModel

import boot_script
import storage


app = fastapi.FastAPI()


@app.get('/boot_source')
def boot_source():
    return boot_script.generate(
        storage.get('boot_selection_timeout'),
        storage.get('default_target')
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
    storage.save('targets', request.targets)
    storage.save('boot_selection_timeout', request.boot_selection_timeout)
    storage.save('default_target', request.default_target)
