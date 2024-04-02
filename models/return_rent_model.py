import pandas
import sqlite3

def db_return_rent(conn, rent_id,penalty = 0):
    cur = conn.cursor()

    cur.execute(
    '''
    SELECT ConsoleID, UserID
    from RENT
    where RentID = :ri
    ''', {"ri" : rent_id}
    )
    
    fetch = cur.fetchone()
    console_id = fetch[0]
    user_id = fetch[1]

    cur.execute("""
        UPDATE USERS 
        SET HasRented = False
        WHERE UserID = :ui
    """, {"ui": user_id})
    
    cur.execute("""
        UPDATE USERS 
        SET Penalty = :pen
        WHERE UserID = :ui               
         """,{"ui":user_id, 'pen' : penalty})

    cur.execute("""
        UPDATE CONSOLE
        SET IsRented = false
        WHERE ConsoleID = :ci
    """, {"ci": console_id})

    cur.execute(
          '''
    UPDATE RENT
    SET ReturnDate = DATE("now")
    where RentID = :ri
    ''', {"ri" : rent_id}
    )
    
    conn.commit()

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
