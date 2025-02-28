import socket 
import threading
import sys

class Servidor():

    def __init__(self, host="localhost", port=7000):
        #arreglo para guardar los clientes conectados
        self.clientes = []

        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        self.sock.bind((str(host), int(port)))
        self.sock.listen(10)
        self.sock.setblocking(False)

        #hilos para aceptar y procesar las conexiones
        aceptar = threading.Thread(target=self.aceptarCon)
        procesar = threading.Thread(target=self.procesarCon)

        aceptar.daemon =True 
        aceptar.start()

        procesar.daemon = True 
        procesar.start()
        try:
            while True:
                msg = input('-> ')
                if msg == 'salir':
                    break
                self.sock.close()
                sys.exit()
        except:
            self.sock.close()
            sys.exit()
            
    def msg_to_all(self, msg, cliente):
        for c in self.clientes:
            try:
                if c != cliente:
                    c.send(msg)

            except:
                self.clientes.remove(c)


    def aceptarCon(self):
        print("aceptarCon iniciado")
        while True:
            try:
                conn, addr = self.sock.accept()
                conn.setblocking(False)
                self.clientes.append(conn)
            except:
                pass
            
    def procesarCon(self):
        print("ProcesarCon iniciado")
        while True:
            if len(self.clientes) > 0:
                for c in self.clientes:
                    try:
                        data = c.recv(1024)
                        if data:
                            self.msg_to_all(data,c)
                    except:
                        pass

server = Servidor()
server()