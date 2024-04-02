import pandas
import sqlite3

def get_user(conn):
    return pandas.read_sql(
    '''
    SELECT * FROM USERS
    ''', conn)

def get_user_search(conn, name = "", has_rented = False):
    if name==None:
        name=''
    command = '''
    SELECT UserID as ID, Name as Имя,
    PhoneNumber as "Номер телефона",
    Penalty as Штраф,
    IIF(HasRented==1,'Да','Нет') as "Есть невозвращённая приставка"
    from USERS'''
    if name!='' or has_rented:
        command+=" WHERE "
        if name!='' and has_rented:
            command+= 'USERS.NAME like "' + name +'%"' + "and HasRented==1"
        elif name!='':
            command += 'USERS.NAME like "' + name +'%"'
        elif has_rented:
            command += " HasRented==1"
    return pandas.read_sql(command, conn)

def create_user(conn: sqlite3.Connection, user_name: str, user_phone_number : str):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO USERS (PhoneNumber,Name,Penalty,HasRented)
        VALUES (:uph, :un,0,false)
    """, {"uph": user_phone_number, "un" : user_name})
    conn.commit()
    return cur.lastrowid