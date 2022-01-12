import requests


def get(fqdn, path):
    return requests.get(f'http://{fqdn}{path}')


def post(fqdn, path, request_body=None):
    return requests.post(f'http://{fqdn}{path}', json=request_body)
