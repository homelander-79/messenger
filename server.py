from os import name
import socket
import querys
import pickle
import create_tables 
import threading

lock = threading.Lock()

def unicast(group,sender,online,message):
    if group!=None:
        send(online[1],[8,sender,online[0],message,None])
    else:
        send(online[1],[8,sender,online[0],message,group])

def threaded(con,online_member):
    while True:
            conn=create_tables.create_connection(r"D:\program\network\database\sqllite.db")
            x=reseve(con)
            if x[0]==1:
                if x[1]==1:
                    y=querys.sign_in(x[2],x[3],conn)
                    if y==True:
                        online_member.append((x[2],con))
                        print(x[2],'is connected')
                        unsend=querys.unsend_message(x[2],conn)
                        if unsend == []:
                            send(con,[1,0])
                        else:
                            send(con,[1,1,unsend])
                    else :
                        send(con,[0,1])
                if x[1]==2:
                    y=querys.sign_up(x[2],x[3],conn)
                    if y== True:
                        online_member.append((x[2],con))
                        print(x[2],'is connected')
                        data=[1,'welcom to messanger!',x[2]]
                        send (con,data)
                    if y==False:
                        data=[0,'username token!',x[2]]
                        send(con,data)
                if x[1]==3:
                    con.close()
                    exit(0)
                else:
                    continue
            if x[0]==2:
                if x[1]==1:
                    m=querys.check_name(x[2],conn)
                    if m==True:
                        send(con,['ok'])
                        data=reseve(con)
                        j=0
                        for i in range(len(online_member)):
                            if data[2]==online_member[i][0]:
                                print(data[2],online_member[i][0])
                                lock.acquire()
                                querys.save_message(data[1],None,data[0],conn,data[2],1)
                                unicast(None,data[1],online_member[i],data[0])
                                lock.release()
                                j=1
                                continue
                        if j==0:
                            lock.acquire()
                            querys.save_message(data[1],None,data[0],conn,data[2],0)
                            lock.release
                    if m==False:
                        send(con,['no'])
                if x[1]==2:
                    m=querys.show_groups(x[2],conn)
                    send(con,m)
                    if m[0]==-2:
                        threaded(con,online_member)
                    data=reseve(con)
                    if data:
                        m=querys.save_message(data[0],data[1],data[2],conn,None,0)
                        print(m,'nnnnn')
                        if m==False:
                            send(con,[0])
                        else :
                            send(con,[1])
                            members=querys.group_members(conn,data[1],data[0])
                            for i in members:
                                flag=0
                                for j in range(len(online_member)):
                                    if i[0]==online_member[j][0]:
                                        lock.acquire()
                                        querys.save_message(data[0],None,data[2],conn,i[0],1)
                                        unicast(data[1],data[0],online_member[j],data[2])
                                        lock.release()
                                        flag=1
                                        break
                                if flag==0:
                                    lock.acquire()
                                    querys.save_message(data[0],None,data[2],conn,i[0],0)          
                                    lock.release()            
                if x[1]==3:
                    members=querys.all_members(x[2],conn)
                    for i in members:
                        flags=0
                        for j in online_member:
                            if j[0]==i[0]:
                                lock.acquire()
                                querys.save_message(x[2],None,x[3],conn,i[0],1)
                                lock.release()
                                flags=1
                                unicast(None,x[2],j,x[3])
                        if flags==0:
                            lock.acquire()
                            querys.save_message(x[2],None,x[3],conn,i[0],0)
                            lock.release()
                print('2')
                if x[1]==4:
                    m=querys.check_group_name(x[3],conn)
                    if m==True:
                        send(con,[1])
                        data=reseve(con)
                        n=querys.new_group(data[0],data[1],conn)
                        if n==True:
                            send(con,[1])
                        else:
                            send(con,[0])
                    elif m== False:
                        send(con,[0])
                if x[1]==5:
                    m=querys.show_message(x[2],conn)
                    print
                    send(con,m)
                    if m[0]==-3:
                        threaded(con,online_member)
                    data=reseve(con)
                    if data[0]==-1 or data[0]==-4:
                        pass
                    else:
                        querys.delete_message(conn,data[0],data[1],data[2])
                if x[1]==6:
                    for i in range(len(online_member)):
                        if online_member[i][0]==x[2]:
                            del online_member[i]
                            print(x[2],'is disconnect')
                            break
                    send(con,['goodby {0}'.format(x[2])])
            else :
                continue

def send(con,data):
    data=pickle.dumps(data)
    con.send(data)
        
def reseve(con):
        data=con.recv(10000)
        data=pickle.loads(data)
        return data

def main():
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ip_address=''
    port=2025
    server.bind((ip_address,port))
    server.listen(20)
    online_member=list()
    while True:
        con,addr =server.accept()
        t=threading.Thread(target=threaded,args=(con,online_member))
        t.start()

if __name__ =='__main__':
    main()