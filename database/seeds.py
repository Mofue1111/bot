import sqlite3

conn =  sqlite3.connect("bot/database/app.db")
cursor = conn.cursor()


def create_table_users():
    sql_table_users = """
CREATE TABLE IF NOT EXISTS users (
Id integer Primary key autoincrement,
fullname text,
phone text,
role text DEFAULT user
)
"""
    cursor.execute(sql_table_users)

def create_table_history():
    pass 
def create_orders_tables():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        count INTEGER,
        total_price INTEGER,
        date TEXT,
        user_name TEXT,
        status TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders_dishes (
        id_order INTEGER,
        id_dish INTEGER,
        count INTEGER
    )
    """)

    conn.commit()
    conn.close()

def create_table_dishes():
#       название, описание, калории, цена, фото, теги 
# (веган, без сахара и т.п.) 
      sql_table_dishes = ("CREATE TABLE IF NOT EXISTS dishes("
                         "id integer Primary key autoincrement,"
                         "name text,"
                         "price int," 
                         "photo BLOB,"
                         "tags text,"
                         "description text,"
                         "properties text NULL,"
                         "ans_neurlink text NULL)"
                        )
      cursor.execute(sql_table_dishes)

def seed():
    create_table_users()
    create_table_history()
    create_table_dishes()
    create_orders_tables()
    conn.commit()

seed()