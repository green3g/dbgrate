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
