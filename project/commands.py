import click
from db import create_data_base, create_user_table, create_blacklist_token_table


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    create_data_base()
    create_user_table()
    create_blacklist_token_table()
    click.echo('Initialized the database.')
