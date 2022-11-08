import psycopg2
from config import host, user, password, db_name


def reg_user(message):
    try:
        # connect to exist database
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        # the cursor for performing database operations
        with connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE if not exists users(
                     id_users serial PRIMARY KEY,
                     user_name varchar(50) NOT NULL,
                     chat_id varchar(50) NOT NULL);"""
            )

        with connection.cursor() as cursor:
            cursor.execute(
                f"""select chat_id from users where chat_id = '{message.from_user.id}';"""
            )
            data = cursor.fetchone()

            if data is None:
                cursor.execute(
                    f"""INSERT INTO users (user_name, chat_id)
                        VALUES ('{message.from_user.username}', '{message.from_user.id}');"""
                )
                return None
            else:
                return "User was exists!"

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        pass


def get_users():
    try:
        # connect to exist database
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                f"""select chat_id from users;"""
            )
            data = cursor.fetchall()

            return data

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)

def del_user(message):
    try:
        # connect to exist database
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                f"""delete from users where chat_id = '{message.from_user.id}';"""
            )
        return get_users()


    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)




# get data from a table
# with connection.cursor() as cursor:
#     cursor.execute(
#         """SELECT * FROM users;"""
#     )
#
#     print(*cursor.fetchone())
# connection = psycopg2.connect(
#             host=host,
#             user=user,
#             password=password,
#             database=db_name
#         )
# connection.autocommit = True
#
# with connection.cursor() as cursor:
#      cursor.execute(
#          """DROP table users;"""
#     )
#
#
# with connection.cursor() as cursor:
#     cursor.execute(
#         """CREATE TABLE if not exists users(
#              id_users serial PRIMARY KEY,
#              user_name varchar(50) NOT NULL,
#              chat_id varchar(50) NOT NULL);"""
#     )

# with connection.cursor() as cursor:
#     name = 'alek'
#     ident = '1235'
#     cursor.execute(
#          f"""INSERT INTO users (user_name, chat_id)
#              VALUES ('{name}', '{ident}');"""
#         )


# with connection.cursor() as cursor:
#     cursor.execute(
#             f"""delete from users where user_name = 'Alecsandr';"""
#         )
