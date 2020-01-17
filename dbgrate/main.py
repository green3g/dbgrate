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

CONTEXT={
    'obj': {
        'MIGRATIONS': None,
    },
}

@click.group(context_settings=CONTEXT)
@click.option('--log', default='ERROR', help='Set the log level. DEBUG, INFO, WARNING, ERROR.')
def cli(log):
    level = getattr(logging, log.upper())
    logging.basicConfig(level=level)


@cli.group('db', context_settings=CONTEXT)
@click.pass_context
def db(ctx):
    """
    Run database commands: upgrade, downgrade.
    """
    logging.info('Importing database env...')
    env = import_module('env')
    db = getattr(env, 'DB_CONNECTION_URL', DEFAULT_MIGRATIONS_DB)

    # set the migrations context variable for the next command 
    ctx.obj['MIGRATIONS'] = MigrationRunner(env, db, WORKING_DIR)
    logging.info('Database env imported')


@db.command()
@click.option('--name', default=None, help='Migration ID to run')
@click.pass_context
def upgrade(ctx, name):
    """
    Run the upgrade action of one or all migrations. Specify `NAME` for upgrading one migration. 
    """
    migrations = ctx.obj['MIGRATIONS']
    result = migrations.upgrade(name)
    exit(len(result['error']))


@db.command()
@click.option('--name', default=None, help='Migration ID to run')
@click.pass_context
def downgrade(ctx, name):
    """
    Run the downgrade action of one or all migrations. Specify `NAME` for downgrading one migration. 
    """
    migrations = ctx.obj['MIGRATIONS']
    result = migrations.downgrade(name)
    exit(len(result['error']))



@cli.command()
@click.argument('name')
@click.pass_context
def generate(ctx, name):
    """
    Generate a new database migration item in the local ./migrations folder. 
    """
    comment = click.prompt('Comment')
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
