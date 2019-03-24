import click
import requests
import os
import sys
import json


@click.command('auth', short_help='authorizes user')
def auth():
    email = click.prompt('Enter your email: ')
    password = click.prompt('Enter your password ')

    payload = {'email': email, 'password': password}
    res = requests.post(os.getenv('LAMBY_WEB_URI') +
                        '/api/auth/token', json=payload)
    res_json = res.json()
    if res_json['message'] == 'Invalid credentials!':
        click.echo(res_json['message'])
        sys.exit(1)
    api_key = res_json['api_key']

    with open(os.path.dirname(os.path.abspath(__file__)) +
              '/.config', 'w+') as global_config:
        global_config.write(json.dumps({'api_key': api_key}))
