import mysql.connector
from mysql.connector import Error

from recflows.vars import HOST, PORT, USER, PASSWORD, DATABASE



def run_query(query, values=None, commit=False):
    try:
        conexion = mysql.connector.connect(
            host=HOST,
            port=PORT,
            database=DATABASE,
            user=USER,
            password=PASSWORD,
        )

        # Crear un cursor
        cursor = conexion.cursor()

        # Ejecutar una consulta SQL
        if values:
            cursor.execute(query, values)
            conexion.commit()
        elif commit:
            cursor.execute(query)
            conexion.commit()
        else:
            cursor.execute(query)

        # Obtener y mostrar los resultados
        registros = cursor.fetchall()

        # Cerrar el cursor y la conexión
        cursor.close()
        conexion.close()

        return registros
    except Error as e:
        print(f"Error al conectar a la base de datos: {repr(e)}")


def read_table(table_name):
    registros = run_query(f"SELECT * FROM {table_name};")
    return registros


def read_resource_by_id(table_name, id):
    registros = run_query(f"SELECT * FROM {table_name} WHERE id = '{id}';")
    return registros


def insert_resouce(table_name, record):
    query = f"""
    INSERT INTO {table_name} ({', '.join(record.keys())})
    VALUES({', '.join(["%s" for _ in record.keys()])})
    """
    values = tuple(record.values())
    run_query(query, values)


def update_resouce(table_name, record):
    id = record["id"]
    record = {k: v for k, v in record.items() if k != "id"}
    values = tuple(record.values())
    query = f"""
    UPDATE {table_name}
    SET {', '.join([f"{k} = %s" for k in record.keys()])}
    WHERE id = '{id}'
    """

    run_query(query, values)


def delete_resouce_by_id(table_name, id):
    query = f"DELETE FROM {table_name} WHERE id = '{id}'"

    run_query(query, commit=True)
