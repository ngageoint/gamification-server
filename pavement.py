# -*- coding: utf-8 -*-

import os
import sys

from paver.easy import *
from paver.setuputils import setup

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

setup(
    name="gamification",
    packages=['gamification'],
    version='0.0.0.1',
    url="",
    author="Site Admin",
    author_email="admin@localhost"
)


@task
def install_dependencies():
    """ Installs dependencies."""
    sh('pip install --upgrade -r gamification/requirements.txt')


@cmdopts([
    ('fixture=', 'f', 'Fixture to install"'),
])
@task
def install_fixture(options):
    """ Loads the supplied fixture """
    fixture = options.get('fixture')
    sh("python manage.py loaddata {fixture}".format(fixture=fixture))


@task
def install_dev_fixtures():
    """ Installs development fixtures in the correct order """
    fixtures = [
        'gamification/core/fixtures/initial_data.json',  # Core
        'gamification/badges/fixtures/initial_data.json',  # Badges
        'gamification/events/fixtures/initial_data.json', # Events
        ]

    for fixture in fixtures:
        sh("python manage.py loaddata {fixture}".format(fixture=fixture))

@task
def sync_initial():
    sh("python manage.py syncdb; python manage.py migrate --all 2> /dev/null")
    sh("python manage.py syncdb; python manage.py migrate --all 2> /dev/null")
    sh("python manage.py syncdb; python manage.py migrate core")
    sh("python manage.py syncdb; python manage.py migrate --all")

@task
def sync():
    """ Runs the syncdb process with migrations """
    sh("python manage.py migrate core")
    sh("python manage.py syncdb --noinput")
    sh("python manage.py migrate --all")


@cmdopts([
    ('bind=', 'b', 'Bind server to provided IP address and port number.'),
])
@task
def start_django(options):
    """ Starts the Django application. """
    bind = options.get('bind', '')
    sh('python manage.py runserver %s &' % bind)


@needs(['sync',
        'start_django'])
def start():
    """ Syncs the database and then starts the development server. """
    info("Gamification is now available.")


@cmdopts([
    ('template=', 'T', 'Database template to use when creating new database, defaults to "template_postgis"'),
])
@task
def createdb(options):
    """ Creates the database in postgres. """
    from gamification import settings
    template = options.get('template', 'template_postgis')
    database = settings.DATABASES.get('default').get('NAME')
    sh('createdb {database}'.format(database=database, template=template))


@task
def create_db_user():
    """ Creates the database in postgres. """
    from gamification import settings
    database = settings.DATABASES.get('default').get('NAME')
    user = settings.DATABASES.get('default').get('USER')
    password = settings.DATABASES.get('default').get('PASSWORD')

    sh('psql -d {database} -c {sql}'.format(database=database,
                                            sql='"CREATE USER {user} WITH PASSWORD \'{password}\';"'.format(user=user,
                                                                                                            password=password)))
