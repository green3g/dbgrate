import click
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import importlib
from os.path import basename, isfile, join
import glob
from datetime import datetime
from mako.template import Template
from os.path import dirname, realpath
from os import makedirs, errno, getcwd

# modify the local path so we can import our env.py
from sys import path
WORKING_DIR = getcwd()
path.append(WORKING_DIR)

engine = None
session = None

Base = declarative_base()


class Migration(Base):
    __tablename__ = 'migrations'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    status = Column(String)


def init_migrations():

    try:
        makedirs('migrations')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def get_migrations():
    modules = glob.glob(join(WORKING_DIR, "migrations", "*.py"))
    __all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

    return __all__


def run_migrations(action, message='Applying migration', status='APPLIED', migration=None, reverse=False):
    migrations = get_migrations()

    # handle downgrades
    if reverse:
        migrations = migrations.reverse()

    # handle individual migrations
    if migration:
        print('Filtering list to include only {}'.format(migration))
        migrations = [m for m in migrations if m == migration]
    print('Found migrations: ', migrations)

    for migration in migrations:
        print('{} {}...'.format(message, migration))

        # get or create a migration orm object
        current_migration = session.query(Migration).filter_by(name=migration).first()
        if not current_migration:
            current_migration = Migration(name=migration)

        # skip if it the status is already upgraded
        if current_migration.status == status:
            print('Migration has already been set to {}, skipping'.format(status))
            continue
        
        # import it and run it
        i = importlib.import_module('.'.join(['migrations', migration]))
        action(i)

        # update database of migrations
        current_migration.status = status;
        session.add(current_migration)
        print('Migration was successful.')
    session.commit()


@click.group()
def main():
    pass


@main.group('db')
def db():
    global engine, session
    print('Importing database env...')
    importlib.import_module('env')
    init_migrations()
    engine = create_engine(join('sqlite:///migrations', 'migrations.sqlite'))
    Base.metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    print('Database env imported')


@db.command()
@click.option('--name', default=None, help='Migration ID to run')
def upgrade(name):
    def action(migration):
        migration.upgrade()

    run_migrations(action, migration=name)


@db.command()
@click.option('--name', default=None, help='Migration ID to run')
def downgrade(name):
    def action(migration):
        migration.downgrade()

    run_migrations(action, 'Downgrading migration', 'REMOVED', migration=name, reverse=True)


@main.command()
@click.argument('name')
def generate(name):

    init_migrations()

    timestamp = str(datetime.now().timestamp()).replace('.', '_')
    comment = click.prompt('Comment')
    file_name = '{}_{}.py'.format(timestamp, name.replace('.', '_'))
    print('generating migration migrations/{}'.format(file_name))

    # get the template content
    template_path = '{}/templates/migration.py.mako'.format(dirname(realpath(__file__)))
    with open(template_path, 'r') as f:
        template = f.read()

    # write it to a migration file
    with open('migrations/{}'.format(file_name), 'w') as f:
        content = Template(template).render(
            create_date=datetime.now().ctime(),
            comment=comment,
        )
        f.write(content)


cli = click.CommandCollection(sources=[main])
if __name__ == '__main__':
    cli()
