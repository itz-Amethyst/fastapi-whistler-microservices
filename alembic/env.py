from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from common.config import settings
from common.models.pictureMixIn import PictureMixin
from common.db.session import DBSessionManager, MetaData 
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
#! Custom
config.set_main_option("sqlalchemy.url", settings.FULL_DATABASE_PG_URL)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
#? Custom
target_metadata = MetaData

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

#? Custom

def run_setup_on_migration(context):
    with DBSessionManager().session_sync() as session:
        PictureMixin().setup(session)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        #! Todo: be here or not ?
        # process_revision_directives=run_setup_on_migration 
    )

    with context.begin_transaction():
        context.run_migrations()
        # custom
        run_setup_on_migration()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata 
            #! Todo: be here or not ?
            # process_revision_directives=run_setup_on_migration 
        )

        with context.begin_transaction():
            context.run_migrations()
            # Custom
            run_setup_on_migration()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
