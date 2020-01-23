from inspect import getargspec
from os.path import dirname,  isfile, join, exists, isdir, basename 
from os import makedirs, errno, getcwd
from glob import glob
from mako.template import Template
from sys import path
from sys import stdout
from importlib import import_module
import logging

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from .Migration import Migration, Base
from .constants import PACKAGE_DIR


class MigrationRunner(object):
    def __init__(self, env, db_uri, workspace):

        logging.debug('Using db connection: {}'.format(db_uri))
        self.engine = create_engine(db_uri)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()

        self.env = env 

        # update the path so we can import migrations
        logging.debug('Using workspace: {}'.format(workspace))
        self.workspace = workspace
        

        
    def upgrade(self, name):
        """
        Run the upgrade action of one or all migrations. Specify `NAME` for upgrading one migration. 
        """
        return self.run_migrations('upgrade', migrate_to=name)

    def downgrade(self, name):
        return self.run_migrations('downgrade', 'Downgrading migration', 'REMOVED', migrate_to=name, reverse=True)
    

    def get_migrations(self):
        """
        return a list of the migrations that can be run 
        """
        modules = glob(join(self.workspace, "migrations", "*.py"))
        migrations = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

        return migrations

    def get_migration_args(self, fn):
        """
        evaluates a migration function for arguments and returns a dict
        with valid arguments. 
        """
        spec = getargspec(fn)
        args = {}
        for arg in spec.args:
            logging.debug('Adding argument: {}.'.format(arg))
            args[arg] = getattr(self, arg)
            
        return args

    def run_migrations(self, action, message='Applying migration', status='APPLIED', migrate_to=None, reverse=False):
        result = {
            'error': [],
            'success': [],
        }
        migrations = self.get_migrations()

        # handle downgrades
        if reverse:
            migrations.reverse()

        # handle individual migrations
        if migrate_to and migrate_to not in migrations:
            logging.warning('Error: The migration {} was not found in the list of migrations. No actions were completed'.format(migrate_to))
            logging.warning('Available migrations are: {}'.format(' ,'.join(migrations)))
            return
        logging.info('Found migrations:\n\t{}'.format('\n\t'.join(migrations)))
        if migrate_to:
            logging.info('Migration name was passed, migration will stop after completing {}'.format(migrate_to))

        for m in migrations:
            # get or create a migration orm object
            current_migration = self.session.query(Migration).filter_by(name=m).first()
            if not current_migration:
                current_migration = Migration(name=m)

            # skip if it the status is already upgraded
            if current_migration.status == status:
                logging.info('Skipped migration {}. Already been set to {}'.format(m, status))
                continue
            
            logging.info('{} {}...'.format(message, m))
            
            # import it and run it
            try:
                i = import_module('.'.join(['migrations', m]))
                fn = getattr(i, action)
                if fn:
                    args = self.get_migration_args(fn)
                    fn(**args)
            except Exception:
                result['error'].append('{} - {}'.format(action, m))
                logging.traceback.print_exc(file=stdout)
                logging.error('Error while executing migration {}!'.format(m))

                fn = getattr(i, 'downgrade')
                if fn:
                    logging.info('Rolling back migration {}...'.format(m))
                    args = self.get_migration_args(fn)
                    try:
                        fn(**args)
                    except Exception:
                        result['error'].append('Downgrade - {}'.format(m))
                        logging.traceback.print_exc(file=stdout)
                        logging.error('Error while executing downgrade migration {}!'.format(m))
                    
                break

            # update database of migrations
            current_migration.status = status;
            self.session.add(current_migration)
            self.session.commit()
            result['success'].append(m)
            logging.info('Migration was successful.')

            if migrate_to and current_migration.name == migrate_to:
                logging.info('Migration has finished to {}. Migration process will now complete.'.format(migrate_to))
                break

        logging.info('Committing migration updates...')
        self.session.commit()
        logging.info('Migration complete')

        return result