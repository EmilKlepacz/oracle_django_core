from django.db import connection


def next_sequence_value(sequence_name):
    with connection.cursor() as cursor:
        cursor.execute(f"select {sequence_name}.nextval from dual")
        return cursor.fetchone()[0]
