import socket 
import time

SOCKET_BUFFER = 1024


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("192.168.1.11", 4000)
    
    print(f"Iniciando servidor en {server_address[0]} en el puerto {server_address[1]}")
    
    sock.bind(server_address)
    sock.listen()
    
    while True:
        print(f"Esperando conexión")
        try:
            conn, client_address = sock.accept()
            print(f"Conectado desde {client_address[0]} en puerto {client_address[1]}")
            with conn:
                while True:
                    lista = []
                    data= conn.recv(SOCKET_BUFFER).decode()
                    print(f"Recibi data")
                    lista.append(data)
                    if lista:
                        dato = lista.pop(0)
                        with open("archivo_recibo_datos.txt", "a") as f:
                            f.write(dato)
        except KeyboardInterrupt:
            print("El usuario ha terminado el programa")  
            break;              
                        