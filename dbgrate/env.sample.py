from os.path import join

from environs import Env 
env = Env()
env.read_env()

db_connection = env.str('DB_CONNECTION', default='gisdata___inspect_sde.sde')
username = env.str('DB_USERNAME', default='dbo')
password = env.str('DB_PASSWORD', default='secret')
db = env.str('DB_NAME', default='inspect_sde')
host = env.str('DB_HOST', default='gisdata.com')
schema = env.str('DB_SCHEMA', default='dbo')

DB_CONNECTION_URL = 'postgresql://{username}:{password}@{host}:5432/{db}'.format(
    db=db,
    password=password,
    username=username,
    host=host,
)