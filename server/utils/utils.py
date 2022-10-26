import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
  from Constants import USERNAME, PASSWORD
except ImportError:
  from sys import exit
  exit("Please, ensure you have a Constants.py file with the USERNAME and PASSWORD constants")


def CreateLocalDB(db_name, host='localhost', port='5432'):

    dialect = 'postgresql'

    username = USERNAME
    password = PASSWORD

    if port:
        port = ':' + port
    if password:
        password = ':' + password

    db_url_name = f"{dialect}://{username}{password}@{host}{port}/{db_name}"

    from sqlalchemy import create_engine
    engine = create_engine(db_url_name)

    from sqlalchemy_utils import database_exists
    if not database_exists(engine.url):

        from sqlalchemy_utils import create_database
        create_database(engine.url, encoding='utf8')


CreateLocalDB("development")
#CreateLocalDB("production")
