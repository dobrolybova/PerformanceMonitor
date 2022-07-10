import psycopg2

sql_commands = (
        """
        CREATE TABLE users (
            "user_name" character varying NOT NULL,
            user_passwd character varying NOT NULL,
            user_id bigserial,
            PRIMARY KEY ("user_name")
        )
        """,
        """
        CREATE TABLE sessions (
            user_id integer NOT NULL,
            user_session uuid,
            user_cpu double precision,
            user_timestamp double precision
        )
        """,
)


def create_db():
    conn = psycopg2.connect(database="postgres",
                            user='postgres',
                            password='example',
                            host='127.0.0.1',
                            port='5432')
    conn.autocommit = True
    cursor = conn.cursor()
    sql = '''CREATE database performancemonitor'''
    cursor.execute(sql)
    conn.close()


def create_tables(commands: tuple[str, str]):
    conn = psycopg2.connect(database="performancemonitor",
                            user='postgres',
                            password='example',
                            host='127.0.0.1',
                            port='5432')
    cursor = conn.cursor()
    for command in commands:
        cursor.execute(command)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_db()
    create_tables(sql_commands)
