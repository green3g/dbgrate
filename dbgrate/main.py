import click
import logging
from importlib import import_module
from os.path import join
from sys import path
from os import getcwd, environ

from .lib.MigrationRunner import MigrationRunner
from .lib.generator import init_migrations, generate_migration

# modify the local path so we can import our env.py
WORKING_DIR = getcwd()
path.append(WORKING_DIR)

DEFAULT_MIGRATIONS_DB = join('sqlite:///migrations', 'migrations.sqlite')


@click.group()
@click.option('--log', default='INFO', help='Set the log level. DEBUG, INFO, WARNING, ERROR.')
def cli(log):
    level = getattr(logging, log.upper())
    logging.basicConfig(level=level)


@cli.group('db')
def db():
    """
    Run database commands: upgrade, downgrade.
    """
    pass

def get_runner():
    logging.info('Importing database env...')
    env = import_module('env')
    db = getattr(env, 'DB_CONNECTION_URL', DEFAULT_MIGRATIONS_DB)

    logging.info('Database env imported')

    # set the migrations context variable for the next command 
    return MigrationRunner(env, db, WORKING_DIR)


@db.command()
@click.option('--name', default=None, help='Upgrade to specific migration version')
def upgrade(name):
    """
    Run the upgrade action of one or all migrations. Specify `NAME` for upgrading one migration. 
    """
    migrations = get_runner()
    result = migrations.upgrade(name)
    exit(len(result['error']))


@db.command()
@click.option('--name', default=None, help='Downgrade to specific migration version')
def downgrade(name):
    """
    Run the downgrade action of one or all migrations. Specify `NAME` for downgrading one migration. 
    """
    migrations = get_runner()
    result = migrations.downgrade(name)
    exit(len(result['error']))



@cli.command()
@click.option('--name', default=None, help='Migration name')
@click.option('--comment', default=None, help='Comment text for migration.')
def generate(name=None, comment=None):
    """
    Generate a new database migration file
    """
    name = name or click.prompt('Migration name')
    comment = comment or click.prompt('Comment')
    author = environ.get('USER') or environ.get('USERNAME')
    generate_migration(WORKING_DIR, name, {
        'comment': comment,
        'author': author,
    })

if __name__ == '__main__':
    logging.info('dbgrate: Current working directory is {}'.format(WORKING_DIR))
    init_migrations(WORKING_DIR)

    # create cli with context
    cli()
