from logging.config import fileConfig
from time import sleep

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from common.config import settings
from common.config.settings import Settings
from common.models.pictureMixIn import PictureMixin
from common.db.session import DBSessionManager, metadata 
from common.db.session import Base

#? Custom models
from product_service import models
from user_service import models
from order_service import models

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
#! Custom
settings = Settings()
# local_connection = settings.FULL_DATABASE_PG_URL.replace("db", "localhost", 1)
sync_database_url = settings.FULL_DATABASE_PG_URL.replace("postgresql+asyncpg", "postgresql")
print(sync_database_url)
config.set_main_option("sqlalchemy.url", sync_database_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
#? Custom
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

#? Custom
def run_setup_on_migration(ctx, **args):
    with ctx.begin_transaction():
        ctx.run_migrations()
    sleep(1)
    with DBSessionManager().session_sync() as session:
        for class_ in PictureMixin.__subclasses__():
            print(f"Running setup for {class_.__name__}")
            class_.setup(session)

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
    )

    with context.begin_transaction():
        context.run_migrations()


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
            connection=connection,
            #? Custom
            target_metadata=target_metadata ,
            on_version_apply=run_setup_on_migration
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
