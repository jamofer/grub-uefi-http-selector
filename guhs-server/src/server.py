import io
import re

import flask
from flask import send_file, request

import boot_script
import storage


app = flask.Flask(__name__)


@app.get('/boot_source.cfg')
def boot_source():
    content = boot_script.generate(_default_target(), storage.get('boot_selection_timeout'))
    media_type = 'application/octet-stream'
    return send_file(io.BytesIO(content), mimetype=media_type)


@app.get('/api/get/{parameter}')
def get_parameter(parameter):
    return {'value': storage.get(parameter)}


@app.post('/api/set')
def set_parameter():
    parameter = request.get_json()
    storage.save(parameter['parameter'], parameter['value'])

    return '', 200


@app.get('/api/configuration')
def configuration():
    return {
        'targets': storage.get('targets'),
        'boot_selection_timeout': storage.get('boot_selection_timeout'),
        'default_target': storage.get('default_target')
    }


@app.post('/api/configuration')
def configure():
    configuration_json = request.get_json()
    storage.save('targets', configuration_json['targets'])
    storage.save('boot_selection_timeout', configuration_json['boot_selection_timeout'])
    storage.save('default_target', configuration_json['default_target'])

    return '', 200


def _default_target():
    target = storage.get('default_target')
    if re.match(r'\d+', target) is not None:
        return str(int(target) - 1)
