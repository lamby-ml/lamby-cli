import os

from dotenv import load_dotenv


def init_env(env='development'):
    config_path = os.path.realpath(os.path.join('.', 'lamby/config'))
    print(config_path)
    load_dotenv(dotenv_path=os.path.join(config_path, '%s.env' % env))
