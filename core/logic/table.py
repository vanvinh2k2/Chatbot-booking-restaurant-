from django.db import connection

def get_table_all(query):
    tables = []
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        for row in rows:
            data_col = dict(zip(columns, row))
            tables.append(data_col)
    return tables