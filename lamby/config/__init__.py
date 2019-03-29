import os

from dotenv import load_dotenv


def init_env(env='development'):
    config_path = os.path.realpath(os.path.join(__file__, '..'))
    load_dotenv(dotenv_path=os.path.join(config_path, '%s.env' % env))
