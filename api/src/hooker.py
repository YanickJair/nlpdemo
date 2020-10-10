import psycopg2

""" 
Description:
    create a new connection to a DB
"""
def connection(host, username, db_name, password, port="5432", db_type="PSQL",):
    try:
        conn = psycopg2.connect(
            host=host,
            database=db_name,
            user=username,
            password=password
        )
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        raise error

""" 
Description:
    Return the configured field from database to be analyzed
"""
def query_fields():
    pass