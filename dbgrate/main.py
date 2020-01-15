import click
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
        'workspace': None,
    },
}

@click.group(context_settings=CONTEXT)
def main():
    pass


@main.group('db', context_settings=CONTEXT)
@click.pass_context
def db(ctx):
    """
    Run database commands: upgrade, downgrade.
    """
    print('Importing database env...')
    env = import_module('env')
    db = getattr(env, 'DB_CONNECTION_URL', DEFAULT_MIGRATIONS_DB)

    # set the migrations context variable for the next command 
    ctx.obj['MIGRATIONS'] = MigrationRunner(env, db, WORKING_DIR)
    print('Database env imported')


@db.command()
@click.option('--name', default=None, help='Migration ID to run')
@click.pass_context
def upgrade(ctx, name):
    """
    Run the upgrade action of one or all migrations. Specify `NAME` for upgrading one migration. 
    """
    migrations = ctx.obj['MIGRATIONS']
    migrations.upgrade(name)


@db.command()
@click.option('--name', default=None, help='Migration ID to run')
@click.pass_context
def downgrade(ctx, name):
    """
    Run the downgrade action of one or all migrations. Specify `NAME` for downgrading one migration. 
    """
    migrations = ctx.obj['MIGRATIONS']
    migrations.downgrade(name)



@main.command()
@click.argument('name')
@click.pass_context
def generate(ctx, name):
    comment = click.prompt('Comment')
    author = environ.get('USER') or environ.get('USERNAME')
    generate_migration(ctx.obj['workspace'], name, {
        'comment': comment,
        'author': author,
    })

cli = click.CommandCollection(sources=[main])
if __name__ == '__main__':
    print('dbgrate: Current working directory is {}'.format(WORKING_DIR))
    init_migrations(WORKING_DIR)

    # create cli with context
    cli()
