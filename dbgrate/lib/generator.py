
from os import makedirs
from os.path import dirname, join, exists, isdir, realpath
from mako.template import Template
from datetime import datetime
import logging

from .constants import PACKAGE_DIR

def init_migrations(workspace):
    """
    Initialize working directory with python package and migrations folder
    """
    if not isdir(join(workspace, 'migrations')):
        logging.info('Initializing migrations directory...')
        try:
            makedirs(join(workspace, 'migrations'))
        except Exception as e:
            logging.info('Error initializing migrations:')
            logging.info(e)

    # create init.py
    if not exists(join(workspace, 'migrations', '__init__.py')):
        logging.info('Initializing __init__.py migrations package...')
        template_path = join(PACKAGE_DIR, 'templates', '__init__.py.mako')
        with open(template_path, 'r') as f:
            template = f.read()
            with open(join('migrations', '__init__.py'), 'w') as f:
                content = Template(template).render()
                f.write(content)


def generate_migration(workspace, name, data={}):
    """
    Generate a new migrations file. Migrations will be prefixed with a timestamp.
    """


    timestamp = str(datetime.now().timestamp()).replace('.', '_')
    file_name = '{}_{}.py'.format(timestamp, name.replace('.', '_').replace(' ', '_').lower())
    logging.info('generating migration migrations/{}'.format(file_name))

    # get the template content
    template_path = join(dirname(realpath(__file__)), 'templates', 'migration.py.mako')
    with open(template_path, 'r') as f:
        template = f.read()

    data['create_date'] = datetime.now().ctime()

    # write it to a migration file
    with open(join('migrations', file_name), 'w') as f:
        content = Template(template).render(**data)
        f.write(content)

    logging.info('Created new migration file migrations/{}'.format(file_name))
    return file_name