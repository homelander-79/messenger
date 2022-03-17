from sys import flags
import create_tables
import datetime 

def sign_in(name,password,conn):
    c=conn.cursor()
    c.execute("""select user_name, password from USERS
    where user_name==? and password== ?""",(name,password,))
    rows=c.fetchall()
    if rows == []:
        return False
    else:
        return True

def sign_up(name,password,conn):
    c=conn.cursor()
    c.execute("""select user_name from USERS
    where user_name==?""",(name,))
    rows=c.fetchall()
    if rows !=[]:
        return False
    else :
        tuple_1=(name,password)
        c=conn.cursor()
        c.execute("""insert into USERS (user_name,password) values (?,?)""",tuple_1)
        conn.commit()
        return True

def check_name(name,conn):
    c=conn.cursor()
    c.execute("""select user_name from USERS 
    where user_name==?""",(name,))
    rows=c.fetchall()
    if rows == []:
        return False
    else:
        return True

def show_groups(name,conn):
    c=conn.cursor()
    c.execute("""select group_name ,user_name from GROUPS
    where user_name ==? """,(name,))
    rows=c.fetchall()
    if rows==[]:
        return [-2]
    return rows

def check_group_name(group_name,conn):
    c=conn.cursor()
    c.execute("""select group_name from GROUPS""")
    row=c.fetchall()
    for i in row:
        if  group_name==i[0]:
            return False  
    return True

def new_group(group_name,contacts,conn):
    c=conn.cursor()
    for i in contacts:
        c.execute("""select user_name from USERS 
        where user_name==?""",(i,))
        row=c.fetchall()
        if row==[]:
          return False
    for i in contacts:
        c.execute('insert into GROUPS (user_name,group_name) values(?,?)',(i,group_name))
        conn.commit()
    return True

def save_message(name,group,message,conn,recv_name,status):
    if group==None:
        c=conn.cursor()
        c.execute("""select number from message
        where sender== ? and resever==? or sender== ? and resever==? """,(name,recv_name,recv_name,name))
        rows=c.fetchall()
        number=0
        if rows==[]:
            rows+=[(0,)]
        for j in range(len(rows)):
            for i in rows[j]:
                if number<=i:
                    number=i+1
        now=datetime.datetime.now()
        info=(name,recv_name,number,message,status,now)
        c.execute("""insert into message (sender , resever, number,message,status ,time) values (?,?,?,?,?,?)""", info)
        conn.commit()
        return True

def show_message(name,conn):
    c=conn.cursor()
    c.execute('''select * from message where sender==?
    or resever==?''',(name,name,))
    rows=c.fetchall()
    if rows==[]:
        rows=[-3]
    c.execute('''update message set status=?''',(1,))
    conn.commit()
    return rows

def delete_message(conn,id,sender,resever):
    c=conn.cursor()
    c.execute('''delete from message where number==? 
    and sender==? and resever==?''',(id,sender,resever))
    conn.commit()

def group_members(conn,group_name,sender):
    c=conn.cursor()
    c.execute("""select user_name from groups 
    where group_name =? and user_name!=?""",(group_name,sender))
    rows=c.fetchall()
    return rows

def all_members(sender,conn):
    c=conn.cursor()
    c.execute("""select user_name from users where user_name!=?""",(sender,))
    rows=c.fetchall()
    return rows 

def unsend_message(name,conn):
    c=conn.cursor()
    c.execute("""select * from message where resever=? and status=?""",(name,'0'))
    row=c.fetchall()
    c.execute('''update message set status=?
    where resever=?''',(1,name))
    conn.commit()
    return row 

if __name__=="__main__":
    conn=create_tables.create_connection(r"C:\Users\mostafa\Desktop\messenger\database\sqlite.db")
    #print(conn.cursor().execute('''select * from users''').fetchall())