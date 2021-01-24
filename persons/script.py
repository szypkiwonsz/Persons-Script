import click

from data_loader import JsonLoader
from database import DatabaseHandler
from query_handler import GenderHandler, CommonCitiesHandler, CommonPasswordsHandler, DateHandler, \
    PasswordHandler


@click.group()
def cli():
    pass


@cli.command(help='Loads n persons data from api to database.')
@click.argument('n', nargs=1, type=int)
def load_from_api(n):
    temp_json_loader = JsonLoader()
    temp_json_loader.load_data_from_api(n)
    temp_json_loader.modify_data()
    temp_database_handler = DatabaseHandler()
    temp_database_handler.insert_data_into_person(temp_json_loader.data['results'])
    click.echo('The data from the API has been correctly loaded.')


@cli.command(help='Loads persons data from file to database.')
@click.argument('filename', nargs=1, type=str)
def load_from_file(filename):
    temp_json_loader = JsonLoader()
    temp_json_loader.load_data_from_file(filename)
    temp_json_loader.modify_data()
    temp_database_handler = DatabaseHandler()
    temp_database_handler.insert_data_into_person(temp_json_loader.data['results'])
    click.echo('The data from the file has been correctly loaded.')


@cli.command(help='Shows percentage of women and men in database.')
def people_percentage():
    temp_gender_handler = GenderHandler()
    click.echo(f'Percentage of women: {temp_gender_handler.get_gender_percentage("male")}%, '
               f'men: {temp_gender_handler.get_gender_percentage("female")}%')


@cli.command(help='Options: "male", "female", "all".')
@click.argument('gender', nargs=1, type=str)
def average_age(gender):
    temp_gender_handler = GenderHandler()
    click.echo(f'Average age of {gender}(s) is {temp_gender_handler.get_average_gender_age(gender)}')


@cli.command(help='Shows N common cities.')
@click.argument('n', nargs=1, type=int)
def most_common_cities(n):
    temp_cities_handler = CommonCitiesHandler()
    click.echo(temp_cities_handler.get_n_common_cities(n))


@cli.command(help='Shows N common passwords.')
@click.argument('n', nargs=1, type=int)
def most_common_passwords(n):
    temp_passwords_handler = CommonPasswordsHandler()
    click.echo(temp_passwords_handler.get_n_common_passwords(n))


@cli.command(help='Shows persons born between two dates.')
@click.argument('dates', nargs=2, type=str)
def range_dob(dates):
    temp_date_handler = DateHandler(dates[0], dates[1])
    click.echo(f'{temp_date_handler.get_persons_born_between_dates()}')


@cli.command(help='Shows safest passwords selected by password rater.')
def safest_password():
    temp_password_handler = PasswordHandler()
    click.echo(f'{temp_password_handler.get_safest_password()}')


if __name__ == '__main__':
    cli()
