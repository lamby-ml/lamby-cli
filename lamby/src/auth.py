import click
import requests
import os
import sys
import json


@click.command('auth', short_help='authorizes user')
@click.option('--email', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def auth(email, password):
    payload = {'email': email, 'password': password}

    try:
        res = requests.post(os.getenv('LAMBY_WEB_URI') +
                            '/api/auth/token', json=payload)
    except requests.exceptions.ConnectionError:
        click.echo('Could not reach lamby web. Aborting authorization.')
        sys.exit(1)
    except requests.exceptions.Timeout:
        click.echo('Connection timed out. Aborting authorization.')
        sys.exit(1)
    except requests.exceptions.TooManyRedirects:
        click.echo(
            'Too many redirects to reach lamby web. Aborting authorization.')
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        click.echo(e)
        sys.exit(1)

    res_json = res.json()
    if res_json['message'] == 'Invalid credentials!':
        click.echo(res_json['message'])
        sys.exit(1)
    api_key = res_json['api_key']

    with open(os.path.dirname(os.path.abspath(__file__)) +
              '/.config', 'w+') as global_config:
        global_config.write(json.dumps({'api_key': api_key}))
    sys.exit(0)
