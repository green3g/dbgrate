# dbgrate
Python cli tool for simple database migration tracking

## Usage

First, create a `env.py` file in the directory you want to store your migrations. 
Inside the `env.py` you can run any python code you want, but to customize the 
migrations database, simply define a variable, like:

```python
# env.py

DB_CONNECTION_URL = 'sqlite:///migrations/custom-migrations.sqlite'

```

You can use any connection url that sqlalchemy supports, since
migrations are stored using sqlalchemy. By default, migrations
will be stored in the directory `migrations/migrations.sqlite`.

Tip: Use git to version these files.


### CLI
```
# install
pip install https://github.com/roemhildtg/dbgrate/archive/master.zip

# help
dbgrate --help
dbgrate db --help
dbgrate generate --help

# generate a migration (no spaces in name)
dbgrate generate migration_name

# run all migrations
dbgrate db upgrade

# upgrade to a specific migration
dbgrate db upgrade --name 1234_migration_name

# downgrade all migrations (in reverse order)
dbgrate db downgrade

# downgrade to a specific migration
dbgrate db downgrade --name 1234_migration_name
```

### Migration files

Each migration file has an upgrade and downgrade method. You can 
run any python you want inside of these functions. You can also
access the sqlalchemy engine if you so choose to. Simply define
the parameter you want, and it will be passed to your function.

Parameters: 

 - `engine` - The sqlalchemy [engine](https://docs.sqlalchemy.org/en/13/core/engines.html?highlight=create_engine#sqlalchemy.create_engine)
 - `sesssion` - Sqalchemy [session](https://docs.sqlalchemy.org/en/13/orm/session_basics.html#what-does-the-session-do)
 - `env` - The env module YOU defined. You can put any data in here you want to be accessible to your migrations.


Example: 

```python


from sqlalchemy import Table, Column, Integer, String, MetaData

meta = MetaData()

account = Table(
    'account', meta,
    Column('id', Integer, primary_key=True),
    Column('login', String(40)),
    Column('passwd', String(40)),
)

# engine gets passed to the method
def upgrade(engine):
    meta.bind = engine
    account.create()


def downgrade(engine):
    meta.bind = engine
    account.drop()

```

## Why?

Why another migration tool? 

1. The learning experience. Building a migration tool has allowed me to learn about file generators, database communication, version management, etc. 
2. I didn't see a easy to use tool that would be flexible enough. I wanted a migrations tool that didn't force me to use an ORM model or even sql. This tool is generic enough to use even with non sql databases. That being said, it doesn't do anything for you other than assist with the migration generation and the actual migration steps. 