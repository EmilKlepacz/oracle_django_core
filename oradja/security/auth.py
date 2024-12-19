from django.db import connection, DatabaseError


def set_authenticated_user(apiusr):
    try:
        with connection.cursor() as cursor:
            cursor.callproc("apisec.set_authenticated_user", [apiusr])
        print(f"User {apiusr} authenticated successfully.")
    except DatabaseError as e:
        print(f"Database error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
