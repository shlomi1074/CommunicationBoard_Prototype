import sqlite3
from Database.DBMgmt import db_name
import Util.Utilities


def get_profile_names():
    con = None
    try:
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        profile_names = []
        for row in cur.execute('SELECT * FROM profiles'):
            profile_names.append(row[0])
        con.commit()
        con.close()
        return profile_names
    except Exception as e:
        if con:
            con.close()
        print("[get_profile_names] " + str(e))
        return None


def add_profile(profile_name, profile_image=r".\Resources\UI Icons\profile-icon.png"):
    if profile_name is None or profile_name == "" or profile_name == '':
        return False

    con = None
    try:
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        sql = ''' INSERT INTO profiles(profileName, profileImagePath)
                  VALUES(?, ?) '''
        profile_image_blob = Util.Utilities.convert_to_binary_data(profile_image)

        cur.execute(sql, (profile_name, profile_image_blob,))
        con.commit()
        con.close()
        return True
    except Exception as e:
        if con:
            con.close()
        print("[add_profile] " + str(e))
        return False


def add_record(profile_name, record_name, record_text, record_icon_name, category):
    if profile_name is None or profile_name == "" or profile_name == '':
        return False

    con = None
    try:
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        sql = ''' INSERT INTO profile_data(profileName, iconName, recordingName, recordingText, category)
                  VALUES(?, ?, ?, ?, ?) '''
        cur.execute(sql, (profile_name, record_icon_name, record_name, record_text, category,))
        con.commit()
        con.close()
        return True
    except Exception as e:
        if con:
            con.close()
        print("[add_profile] " + str(e))
        return False


def add_category(profile_name, category_name, icon_path):
    if profile_name is None or profile_name == "" or profile_name == '':
        return False

    con = None
    try:
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        sql = ''' INSERT INTO categories(profileName, category, icon)
                  VALUES(?, ?, ?) '''
        cur.execute(sql, (profile_name, category_name, icon_path,))
        con.commit()
        con.close()
        return True
    except Exception as e:
        if con:
            con.close()
        print("[add_category] " + str(e))
        return False


def get_user_records(profile_name):
    con = None
    try:
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        records = []
        for row in cur.execute('SELECT * FROM profile_data WHERE profileName=?', (profile_name,)):
            records.append(row)
        con.commit()
        con.close()
        return records
    except Exception as e:
        if con:
            con.close()
        print("[get_profile_names] " + str(e))
        return None


def get_user_categories(profile_name):
    con = None
    try:
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        records = []
        for row in cur.execute('SELECT * FROM categories WHERE profileName=?', (profile_name,)):
            records.append(row)
        con.commit()
        con.close()
        return records
    except Exception as e:
        if con:
            con.close()
        print("[get_user_categories] " + str(e))
        return None


def get_user_category_records(profile_name, category):
    con = None
    try:
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        records = []
        for row in cur.execute('SELECT * FROM profile_data WHERE profileName=? AND category=?',
                               (profile_name, category,)):
            records.append(row)
        con.commit()
        con.close()
        return records
    except Exception as e:
        if con:
            con.close()
        print("[get_user_category_records] " + str(e))
        return None


def get_user_profile_picture(profile_name):
    con = None
    try:
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        pic = cur.execute('SELECT profileImagePath FROM profiles WHERE profileName=?', (profile_name,))
        for p in pic:
            con.commit()
            con.close()
            return p[0]
    except Exception as e:
        if con:
            con.close()
        print("[get_user_profile_picture] " + str(e))
        return None


def delete_profile(profile_name):
    if profile_name is None or profile_name == "" or profile_name == '':
        return False

    con = None
    try:
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        sql = 'DELETE FROM profiles WHERE profileName=?'
        cur.execute(sql, (profile_name,))
        sql = 'DELETE FROM categories WHERE profileName=?'
        cur.execute(sql, (profile_name,))
        sql = 'DELETE FROM profile_data WHERE profileName=?'
        cur.execute(sql, (profile_name,))
        con.commit()
        con.close()
        return True
    except Exception as e:
        if con:
            con.close()
        print("[delete_profile] " + str(e))
        return False


def delete_category(profile_name, category):
    if profile_name is None or profile_name == "" or profile_name == '':
        return False

    con = None
    try:
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        sql = 'DELETE FROM categories WHERE profileName=? AND category=?'
        cur.execute(sql, (profile_name, category,))
        con.commit()
        con.close()
        return True
    except Exception as e:
        if con:
            con.close()
        print("[delete_profile] " + str(e))
        return False


def delete_user_category(profile_name, category_name):
    if profile_name is None or profile_name == "" or profile_name == '':
        return False

    con = None
    try:
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        sql = 'DELETE FROM profile_data WHERE profileName=? AND category=?'
        cur.execute(sql, (profile_name, category_name,))
        con.commit()
        con.close()
        return True
    except Exception as e:
        if con:
            con.close()
        print("[delete_user_category] " + str(e))
        return False


def delete_user_record(profile_name, record_name):
    if profile_name is None or profile_name == "" or profile_name == '':
        return False

    con = None
    try:
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        sql = 'DELETE FROM profile_data WHERE profileName=? AND recordingName=?'
        cur.execute(sql, (profile_name, record_name,))
        con.commit()
        con.close()
        return True
    except Exception as e:
        if con:
            con.close()
        print("[delete_user_record] " + str(e))
        return False


def delete_user_category_record(profile_name, record_name, category):
    if profile_name is None or profile_name == "" or profile_name == '':
        return False

    con = None
    try:
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        sql = 'DELETE FROM profile_data WHERE profileName=? AND recordingName=? AND category=?'
        cur.execute(sql, (profile_name, record_name, category))
        con.commit()
        con.close()
        return True
    except Exception as e:
        if con:
            con.close()
        print("[delete_user_category_record] " + str(e))
        return False


def update_user_profile_picture(profile_name, profile_picture_path):
    con = None
    try:
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        pic_blob = Util.Utilities.convert_to_binary_data(profile_picture_path)
        cur.execute('UPDATE profiles set profileImagePath = ? WHERE profileName=?', (pic_blob, profile_name, ))
        con.commit()
        con.close()
    except Exception as e:
        if con:
            con.close()
        print("[get_user_profile_picture] " + str(e))
        return None

