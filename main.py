import psycopg2

def create_database(conn):
    with conn.cursor() as cursor:
        cursor.execute("CREATE TABLE IF NOT EXISTS Client (id SERIAL PRIMARY KEY, name TEXT NOT NULL, surname TEXT NOT NULL, email TEXT NOT NULL, phone TEXT[])")
        cursor.execute("CREATE TABLE IF NOT EXISTS ClientPhone (client_id INTEGER, phone TEXT)")
        conn.commit()

def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cursor:
        client_id = cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM Client").fetchone()[0]
        cursor.execute("INSERT INTO Client (id, name, surname, email, phone) VALUES (%, %, %, %, %s)", (client_id, first_name, last_name, email, phones or []))
        conn.commit()
        return client_id

def add_phone(conn, client_id, phone):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO ClientPhone (client_id, phone) VALUES (%, %s)", (client_id, phone))
        conn.commit()

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    with conn.cursor() as cursor:
        if first_name is not None:
            cursor.execute("UPDATE Client SET name=? WHERE id=?", (first_name, client_id))
        if last_name is not None:
            cursor.execute("UPDATE Client SET surname=? WHERE id=?", (last_name, client_id))
        if email is not None:
            cursor.execute("UPDATE Client SET email=? WHERE id=?", (email, client_id))
        if phones is not None:
            cursor.execute("UPDATE Client SET phone=? WHERE id=?", (phones or [], client_id))
        conn.commit()

def delete_phone(conn, client_id, phone):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM ClientPhone WHERE client_id=? AND phone=?", (client_id, phone))
        conn.commit()

def delete_client(conn, client_id):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM Client WHERE id=?", (client_id,))
        conn.commit()

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cursor:
        if first_name and last_name:
            cursor.execute("SELECT id, name, surname, email, phone FROM Client WHERE name=? AND surname=?", (first_name, last_name))
        elif email:
            cursor.execute("SELECT id, name, surname, email, phone FROM Client WHERE email=?", (email,))
        elif phone:
            cursor.execute("SELECT id, name, surname, email, phone FROM Client WHERE phone=?", (phone,))
        else:
            cursor.execute("SELECT id, name, surname, email, phone FROM Client")
        return cursor.fetchall()
    with psycopg2.connect(database="homework_db", user="postgres", password="postgres") as conn:
        create_database(conn)

        client_id = add_client(conn, "Natalia", "Bulysheva", "natalia.bu@mail.com", ["+123456789", "+79278971374"])

        add_phone(conn, client_id, "+123456789")

        change_client(conn, client_id, first_name="Anastasiia", last_name="Narbekova", email="anastasiia.nar@mail.com", phones=["+79278908316", "+123456789"])

        clients = find_client(conn, first_name)
    conn.close()

