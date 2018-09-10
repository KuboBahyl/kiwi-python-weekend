import psycopg2
from psycopg2.extras import RealDictCursor


def insert_to_pg(pg_conn, values: dict):
    sql_insert = """
                INSERT INTO jakub_connections (src_id, dst_id, dep, arr, price, type)
                VALUES (%(src_id)s,
                        %(dst_id)s,
                        %(dep)s,
                        %(arr)s,
                        %(price)s,
                        %(type)s);
            """

    with pg_conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute(sql_insert, values)
            pg_conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            pg_conn.rollback()
            print(error)
        # finally:
        #     if pg_conn is not None:
        #         pg_conn.close()

def load_from_pg(pg_conn):
    sql_select = "SELECT * FROM jakub_connections WHERE price < 100"

    with pg_conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute(sql_select)
            results_dict = cursor.fetchall()
            return results_dict

        except (Exception, psycopg2.DatabaseError) as error:
            pg_conn.rollback()
            print(error)