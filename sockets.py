from sqlite3.dbapi2 import connect
import menu
import socket
import threading
from _thread import *
import querys
from create_tables import *
print_lock= threading.Lock()
def threaded(con,addr):
    con.send(menu.menu())
    while True:
        x=con.recv(2048)
        conn=create_connection(r"D:\program\network\database\sqllite.db")
        if x==1:
            con.send('username:')
            name=con.recv(2048)
            con.send('password:')
            password=con.recv(2048)
            sing_in=querys.sign_in(name,password,conn)
            if sing_in== 'not find':
                con.send('no record find or maybe incorrect password):')
                start_new_thread(threaded,(con,addr))
            if sing_in=='welcome':
                con.send('welcome')
                start_new_thread(page ,(name,con,addr))
        if x==2:
            con.send('username:')
            name=con.recv(2048)
            con.send('password:')
            password=con.recv(2048)
            sign_up=querys.sign_up(name,password,conn)
            if sign_up=='not found':
                con.recv('some one with this username exsist ):')
                start_new_thread(threaded,(con,addr))
            else:
                con.recv('welcome to messanger!')
                start_new_thread(page ,(name,con,addr))
        if x == 3:
            con.close()
def page(name,con,addr):
    con.send(menu.page())
    while True:
        x=con.recv(2048)
        conn=create_connection(r"D:\program\network\database\sqllite.db")
        if x==1 :
            recv_name=con.send(input('please inter resever name exist in network:'))
            querys.check_name(recv_name,conn)
            message=con.send(input('enter your message to {0}:'.format(name)))
            querys.save_message(name,None,message,conn,recv_name)
            anycast(name,message)
            start_new_thread(page ,(name,con,addr))
        if x==2:
            querys.show_groups(name,conn)
            group=input('enter group name:')
            message=con.send(input('enter your message to group {0}:'.format(group)))
            querys.save_message(name,group,message,conn,None)
            multicast(name,message)
            page (name,con,addr)
        if x ==3:
            message=con.send(input('enter your message :\b'))
            broadcast(name,message)
            page (name,con,addr)
        if x==4:
            group_name=con.send(input('enter group name(must be unique):'))
            if querys.check_group_name(group_name,conn)==True:
                con.send('try with another name')
                page(name,con ,addr)
            con.send(('enter member names'))
            '''contact=None
            contacts=list()
            while contact != '':
                contact=input('enter username: ')
                contacts+=contact 
                print('group created\n all done!\n')'''
            contacts=con.recv('2024')
            querys.new_group(group_name,contacts,conn)
            page(name,con,addr)
        if x==5:
            m=querys.inbox(name,conn,con)
            if m=='empty':
                con.send('no message find ')
                page(name,con,addr)
            if m=='page':
                page(name,con,addr)
        if x==6:
            querys.log_in_out(name,conn,0)
            threaded(con,addr)
def get_socket():
    return '2020'
def main():
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ip_address='168.192.1.0'
    port='20255'
    server.bind(ip_address,port)
    server.listen(20)
    while True:
        con,addr =server.accept()
        print_lock.acquire()
        start_new_thread(threaded,(con,addr))
def anycast(name,message):
    pass
def multicast(name,message):
    pass
def broadcast(name,message):
    pass