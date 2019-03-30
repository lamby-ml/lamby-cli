import click
import requests
import os
import sys
import json
from src.utils import post_request


@click.command('auth', short_help='authorizes user')
@click.option('--email', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def auth(email, password):
    payload = {'email': email, 'password': password}

    res = post_request(payload, '/api/auth/token')

    res_json = res.json()
    if res_json['message'] == 'Invalid credentials!':
        click.echo(res_json['message'])
        sys.exit(1)
    api_key = res_json['api_key']

    with open(os.path.dirname(os.path.abspath(__file__)) +
              '/.config', 'w+') as global_config:
        global_config.write(json.dumps({'api_key': api_key}))
    sys.exit(0)
