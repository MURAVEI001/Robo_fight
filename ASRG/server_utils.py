import socket
import struct

def getIp():
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.connect(('8.8.8.8',80))
        
    print(s.getsockname()[0])
    return s.getsockname()[0]

def initServer(HOST, PORT):
    print("TCP Server is running...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Socket created")
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        s.bind((HOST, PORT)) #привязка сокета к адресу и порту
        print("Socket bind complete")
        s.listen() #прослушивание входящих подключений
        print("Socket is listening")
        conn, addr = s.accept() #принятие входящего подключения
        return conn
    
def sendData(conn, *data):
    message = struct.pack(f'{len(data)}f', *data)  #упаковка данных в байты
    conn.send(message) #отправка данных клиенту