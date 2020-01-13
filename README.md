# dbgrate
Python cli tool for simple database migration tracking

## Usage

```
# install
pip install https://github.com/roemhildtg/dbgrate/archive/master.zip

# help
dbgrate --help
dbgrate db --help
dbgrate generate --help

# generate a migration
dbgrate generate migration_name

# run all migrations
dbgrate db upgrade

# run one migration
dbgrate db upgrade 1234_migration_name

# downgrade all migrations (in reverse order)
dbgrate db downgrade

# downgrade one migration
dbgrate db downgrade 1234_migration_name
```
