from sqlite3 import connect
con = connect("data/users_info.db")
def create_all_data():
    c = con.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            tg_id INT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            username TEXT,
            frendID INT NULL
        )
    """)
    con.commit()
    c.close()
    con.close()

def add_user(tg_id: int, first_name: str, last_name: str, username: str,frendID='friend_id') -> None:
    con = connect("data/users_info.db")
    c = con.cursor()
    if not check_user(tg_id):
        c.execute("INSERT INTO users (tg_id, first_name, last_name, username, frendID) VALUES (?, ?, ?, ?, ?)", (tg_id, first_name, last_name, username, frendID))
    con.commit()
    c.close()
    con.close()

def check_user(tg_id: int) -> bool:
    con = connect("data/users_info.db")
    c = con.cursor()
    c.execute("SELECT tg_id FROM users WHERE tg_id=?", (tg_id,))
    rows = c.fetchall()
    con.close()  # Ma'lumotlar bazasini yopamiz
    if len(rows) > 0:
        return True
    return False

create_all_data()

def update_fdriend_id(user_id, friend_id):
    con = connect('data/users_info.db')
    c = con.cursor()
    c.execute(f"UPDATE users SET frendID = {friend_id} WHERE tg_id = {user_id}")
    con.commit()
    c.close()
    con.close()

def get_all_datas():
    con = connect('data/users_info.db')
    c = con.cursor()
    users = c.execute(f"SELECT * FROM users")
    f=users.fetchall()
    con.commit()
    c.close()
    con.close()
    return f

def get_name(idd):
    con = connect('data/users_info.db')
    c = con.cursor()
    users = c.execute(f"SELECT first_name FROM users WHERE tg_id = {idd}")
    f=users.fetchall()
    con.commit()
    c.close()
    con.close()
    return f

def get_friend_id(idd):
    con = connect('data/users_info.db')
    c = con.cursor()
    users = c.execute(f"SELECT frendID FROM users WHERE tg_id = {idd}")
    f=users.fetchall()
    con.commit()
    c.close()
    con.close()
    return f

def update_fdriend_id_to_friend_id(user_id):
    con = connect('data/users_info.db')
    c = con.cursor()
    c.execute(f"UPDATE users SET frendID = ? WHERE tg_id = ?", ('friend_id', user_id))
    con.commit()
    c.close()
    con.close()