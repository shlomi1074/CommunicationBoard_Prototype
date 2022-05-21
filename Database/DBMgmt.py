import sqlite3

db_name = 'database.db'


def create_database():
    con = None
    try:
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        # Create table
        cur.execute('''CREATE TABLE IF NOT EXISTS profile_data
                       (profileName text, iconName text, recordingName text, recordingText text, category text)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS profiles
                       (profileName text PRIMARY KEY)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS categories
                       (profileName text, category text, icon text)''')

        # Save (commit) the changes
        con.commit()
        con.close()
    except Exception as e:
        if con:
            con.close()
        print("[create_database] " + str(e))
        return False


def delete_tables():
    con = None
    try:
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cur.execute("DROP TABLE profile_data")
        cur.execute("DROP TABLE profiles")
        cur.execute("DROP TABLE categories")
        con.commit()
        con.close()
        return True
    except Exception as e:
        if con in None:
            con.close()
        print("[delete_table] " + str(e))
        return False


def get_table_list():
    conn = sqlite3.connect(db_name)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [
        v[0] for v in cursor.fetchall()
        if v[0] != "sqlite_sequence"
    ]
    print(tables)
    cursor.close()
    return tables


