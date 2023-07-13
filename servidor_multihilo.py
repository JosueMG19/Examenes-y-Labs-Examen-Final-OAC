import socket
import time
from threading import Thread

SOCK_BUFFER = 1024

def recibir_Datos(lista):
    inicio_recibo = time.perf_counter()
    data = conn.recv(SOCK_BUFFER).decode()
    fin_recibo = time.perf_counter()
    print(f"Recibi data")
    print(f"El tiempo de ejecución del recibo de datos es: {fin_recibo-inicio_recibo} seg")
    lista.append(data)
    

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("192.168.1.11", 4000)


    print(f"Iniciando servidor en {server_address[0]} en el puerto {server_address[1]}")

    sock.bind(server_address)
    sock.listen()

    while True:
        print(f"Esperando conexión ...")
        try:
            conn, client_address = sock.accept()
            print(f"Conexion desde {client_address[0]} en puerto {client_address[1]}")
            with conn:
                while True:
                    lista = []
                    recibir_Datos_thread = Thread(target=recibir_Datos, args=(lista,))
                    recibir_Datos_thread.start()
                    recibir_Datos_thread.join()
                    inicio_escritura = time.perf_counter()
                    if lista:
                        data = lista.pop(0)
                        with open("archivo_recibo_datos.txt", "a") as f:
                            f.write(data)
                    fin_escritura = time.perf_counter()
                    print(f"El tiempo de escritura es {fin_escritura-inicio_escritura} seg")
                    
        except KeyboardInterrupt:
            print("El usuario ha terminado el programa")
            break