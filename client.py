import socket
import pickle
import threading
import datetime

ex=0
flag=None

def messenger(client):                 
    try: 
        t1=threading.Thread(target= new_message,args=(client,))
        t1.start()
        print('-------------------------------------------------------')
        x=int(input('welcome to messenger \n1.sign in\n2.sign up\n3.exit\n'))
        if x==1:
            name=input('enter yousername:')
            password=input('enter password:')
            send(client,[1,1,name,password])
            data=test(1,1)
            if data[0]==1 and data[1]==1 :
                print('-------------------------------------------------------')
                print('you have new messages!')
                print('-------------------------------------------------------')
                for i in data[2]:
                    print('from:',i[0])
                    print('message:',i[4])
                    print('time',i[5])
                    print('-------------------------------------------------------')
                page(client,name)
            elif data[0]==1 and data[1]==0:
                print('-------------------------------------------------------') 
                print('no new message!')
                page(client,name)
            else:
                print('no record find or maybe incorrect password):') 
                messenger(client)  
        if x==2:
            name=input('enter yousername:')
            password=input('enter password:')
            send(client,[1,2,name,password])
            data=test(1,1)
            if data[0]==0:
                print(data[1])
                messenger(client)
            elif data[0]==1:
                print(data[1])
                page(client,name)
        if x==3:
            send(client,[1,3])
            global ex
            ex=1
            print('tanks for choosing us')
            client.close()
            exit()
        else:
            print('wrong input!')
            messenger(client)
        print('-------------------------------------------------------')
    except ValueError:
        print('wrong input!')
        messenger(client)

def page(client,name):
    try:
        print('-------------------------------------------------------')
        x=int(input('1.pv message\n2.group message\n3.broadcast message \n4.new group\n5.all message\n6.log out\n'))
        if x == 1:
            recv_name=input('please inter resever name exist in network:')
            send(client,[2,1,name,recv_name])
            data=test(1,1)
            if data[0]=='ok':
                message=input('enter your message to {0}:'.format(recv_name))
                send(client,[message,name,recv_name])
                page(client,name)
            else :
                print('user not exist!')
                page(client,name)
        if x == 2:
            send(client,[2,2,name])
            data=test(1,1)
            if data[0]==-2:
                print('''-------------------------------------------------------\n
                you are not in any group!\n''')
                page(client,name)
            else:
                print('your gourps is:')
                for i in data:
                    print(i[0])
                group=input('enter group name:')
                message=input('enter your message to group {0}:'.format(group))
                send(client,[name,group,message])
                data=test(1,1)
                if data[0]==1:
                    print('all done!')
                else:
                    print('some thig bad happend!')
                page(client,name)
        if x == 3:
            message=input('enter your message :\b')
            send(client,[2,3,name,message])
            print('done!')
            print('1')
            page(client,name)
        if x == 4:
            group_name=input('enter group name(must be unique):')
            send(client,[2,4,name,group_name])
            data=test(1,1)
            if data[0]==0:
                print('group name is token')
                page(client,name)
            else :
                print('enter member names when done enter space')
                contacts=list()
                while True:
                    contact=input('enter username: ')
                    if contact== ' ':
                        break
                    contacts.append(contact)
                send(client,[group_name,contacts])
                data=test(1,1)
                if data[0]==1:
                    print('group created!')
                    page(client,name)
                else:
                    print('some thing bad happend!')
                    page(client,name)
        if x == 5:
            send(client,[2,5,name])
            data=test(1,1)
            if data[0]!=-3:
                for i in data:
                    print('-------------------------------------------------------')
                    print('id ',i[2],'  from ',i[0],' to ',i[1],':')
                    print('message=',i[3])
                    print('time',i[5])
                    print('-------------------------------------------------------')
                try:    
                    m=int(input('1.back to page\n2.delete message\n'))
                    if m==1:
                        send(client,[-1])
                        page(client,name)
                    elif m==2:
                        resever=input('to how(you can delete only your message)?')
                        id=int(input('select id message:'))
                        send(client,[id,name,resever])
                        print('done!')
                        page(client,name)
                    else:
                       send(client,[-4])
                except ValueError:
                    send(client,[-4])
            else:
                print('no message yet!')
        if x == 6:
            send(client,[2,6,name])
            data=test(1,1)
            print(data[0])
            messenger(client)    
        else:
            print('wrong input')
            page(client,name)
    except ValueError:
        print('wrong input')
        page(client,name)

def new_message(client):
    while True:
        global ex
        if ex==1:
            exit(0)
        try:
            data=pickle.loads(client.recv(100000))
            if data[0]==8:
                print('-------------------------------------------------------')
                print('you have new messages!')
                print('-------------------------------------------------------')
                if data[4]!=None:
                    print('from group',data[4])
                print('from:',data[1])
                print('message:',data[3])
                print('time' ,datetime.datetime.now())
                print('-------------------------------------------------------')                            
            else:
                test(0,data)
        except:
            pass

def socket_c():
    host = '127.0.0.1'
    port = 2025
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client.connect((host,port))
        messenger(client)
    except:
        print('server is not ready! or you are exit (: ')

def send(con,data):
    data=pickle.dumps(data)
    con.send(data)

def test(n,data):
    global flag
    if n == 0:
        flag=data
    elif n==1:
        while True:
            if flag != None:
                l=flag
                flag=None
                return l

if __name__ == '__main__':
    socket_c()    