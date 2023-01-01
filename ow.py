import pickle
import socket
from . import cry

__accept_info__ = {"version": "0.1.0.3"}

class Client:
    def __init__(self,ip:str,port:int):
        self.__ip = ip
        self.__port = port
        self.__socket = socket.socket()
    def Connect(self):
        self.__socket.connect((self.__ip,self.__port))
        self.Send(__accept_info__)
    def Recv(self,buffer_size:int):
        serv_pubk = pickle.loads(self.__socket.recv(147))
        skey = cry.GenerateSimetricKey()
        cpskey = pickle.dumps(cry.AsimetricEncrypt(skey,serv_pubk))
        self.__socket.send(cpskey)
        data = pickle.loads(cry.SimetricDecrypt(self.__socket.recv(buffer_size),skey))
        return data
    def Send(self,data):
        pubk, privk = cry.GenerateAsimetricKeys()
        ppubk = pickle.dumps(pubk)
        self.__socket.send(ppubk)
        skey = cry.AsimetricDecrypt(pickle.loads(self.__socket.recv(112)),privk)
        pdata = pickle.dumps(data)
        cpdata = cry.SimetricEncrypt(pdata,skey)
        self.__socket.send(cpdata)
    def Close(self):
        self.__socket.close()   
class Server:
    def __init__(self,ip:str, port:int):
        self.__ip = ip
        self.__port = port
        self.__socket = socket.socket()
    def Bind(self):
        try:
            self.__socket.bind((self.__ip,self.__port))
            self.__socket.listen()
            return None
        except Exception as e: 
            return e
    def Shutdown(self):
        self.__socket.close()
    def Recv(self,conn,buffer_size:int,timeout: int | None = None):
        conn.settimeout(timeout)
        try:
            conn_pubk = pickle.loads(conn.recv(147))
        except:
            return conn
        skey = cry.GenerateSimetricKey()
        try:
            cpskey = pickle.dumps(cry.AsimetricEncrypt(skey,conn_pubk))
        except:
            return conn
        conn.send(cpskey)
        try:
            data = pickle.loads(cry.SimetricDecrypt(conn.recv(buffer_size),skey))
        except:
            return conn
        conn.settimeout(None)
        return data
    def Send(self,conn,data,timeout: int | None = None):
        conn.settimeout(timeout)
        pubk, privk = cry.GenerateAsimetricKeys()
        ppubk = pickle.dumps(pubk)
        conn.send(ppubk)
        try:
            skey = cry.AsimetricDecrypt(pickle.loads(conn.recv(112)),privk)
        except:
            return False
        pdata = pickle.dumps(data)
        try:
            cpdata = cry.SimetricEncrypt(pdata,skey)
        except:
            return False
        conn.send(cpdata)
        conn.settimeout(None)
        return True
    
    def AcceptDecorator(self,func,timeout = 2):
        def inner():
            conn,address = self.__socket.accept()
            if __accept_info__ != self.Recv(conn,1024,timeout):
                conn.close()
                return
            is_accepted = func(conn,address)
            if not is_accepted:
                conn.close()
                return
            return (conn,address)
        return inner
    def Accept(self,timeout = 2):
        conn, address = self.__socket.accept()
        if __accept_info__ != self.Recv(conn,1024,timeout):
            conn.close()
            return
        return (conn,address)