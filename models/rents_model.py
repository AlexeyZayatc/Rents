import sqlite3
import pandas

def get_rent(conn):
        return pandas.read_sql(
    '''
    SELECT * FROM RENT
    ''', conn)

def get_rent_search(conn, name = '', id = None, only_returned = False):
    if name==None:
        name=''
    if id=='':
        id=None
    command = '''
    SELECT RentID as RentID, 
    USERS.Name as Имя, ConsoleID as ConsoleID,
    RentDate as "Начало аренды",
    ReturnDate as 'Конец аренды'
    from RENT
    join USERS USING(UserID)
    ''' 
    # WHERE Name LIKE  + name + "%"
    if name!='' or id!=None or only_returned:
        command+=" WHERE "
        commands = []
        if name!='':
            commands.append('USERS.Name like "' + name +'%"')
        if only_returned:
            commands.append('ReturnDate is not NULL')
        if id!=None:
            commands.append("ConsoleID==" + str(id))
        command+=' and '.join(commands)
    return pandas.read_sql(command, conn)

def get_user(conn,user_id):
    uid_limit = (pandas.read_sql(
    '''
    select count(*) as Количество from USERS
    ''',conn
    ))['Количество'][0]
    if user_id!='' and user_id!=None:
        if int(user_id)<0 or int(user_id)>=uid_limit:
            return None
    return pandas.read_sql('''
    select name, PhoneNumber
    from USERS
    where UserID=='''+str(user_id),conn)

def get_console(conn,console_id):
    cid_limit = (pandas.read_sql(
    '''
    select count(*) as Количество from CONSOLE
    ''',conn
    ))['Количество'][0]
    if console_id!='' and console_id!=None:
        if int(console_id)<0 or int(console_id)>=cid_limit:
            return None
    return pandas.read_sql('''
    select Console.Name as CN, Company.name as CMN
    from Console
    join Company using (CompanyID)
    where ConsoleID=='''+str(console_id),conn)

def approve(conn : sqlite3.Connection, user_id, console_id):
    cur = conn.cursor()

    uid_limit = (pandas.read_sql(
    '''
    select count(*) as Количество from RENT
    ''',conn
    ))['Количество'][0]
    if int(uid_limit)==0:
        cur.execute("""
            INSERT INTO RENT
            VALUES (0,:ci, :ui,DATE("now"),NULL)
        """, {"ui": user_id, "ci" : console_id})
    else:
        cur.execute("""
            INSERT INTO RENT
            VALUES (:i,:ci, :ui,DATE("now"),NULL)
        """, {"ui": user_id, "ci" : console_id, 'i':int(uid_limit)})
    cur.execute("""
        UPDATE USERS 
        SET HasRented = true
        WHERE UserID = :ui
    """, {"ui": user_id})
    cur.execute("""
        UPDATE CONSOLE
        SET IsRented = true
        WHERE ConsoleID = :ci
    """, {"ci": console_id})

    conn.commit()
    return cur.lastrowid