import pandas
import sqlite3

def get_console(conn):
    return pandas.read_sql(
    '''
    SELECT * FROM CONSOLE
    ''', conn)

def get_console_search(conn, name = "", only_available = False):
    if name==None:
        name=''
    command = '''
    SELECT ConsoleID as ID, Console.Name as Название,
    COMPANY.Name as Производитель, 
    IIF(IsRented==1,'Недоступна','Доступна') as "Доступность"
    from CONSOLE
    join COMPANY USING (CompanyID)'''
    if name!='' or only_available:
        command+=" WHERE "
        if name!='' and only_available:
            command+= 'Console.NAME like "' + name +'%"' + "and IsRented==0"
        elif name!='':
            command += 'Console.NAME like "' + name +'%"'
        elif only_available:
            command += " IsRented==0"
    return pandas.read_sql(command, conn)
    
def get_company(conn):
    return pandas.read_sql(
    '''
    SELECT * FROM COMPANY
    ''', conn)

def create_console(conn, name, company_id):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO CONSOLE (Name,CompanyID,IsRented)
        VALUES (:n, :ci,false)
    """, {"ci": company_id, "n" : name})
    conn.commit()
    return cur.lastrowid