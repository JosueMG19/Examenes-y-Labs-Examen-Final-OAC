import socket
import time 
   
if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("192.168.1.11", 4000)

    print(f"Conectando a {server_address[0]} en el puerto {server_address[1]}")

    sock.connect(server_address)

    try:
        tiempo_lectura_inicio = time.perf_counter()
        with open("big_file.txt","r") as f:
            contenido = f.read()
        tiempo_lectura_fin = time.perf_counter()
        print(f"Tiempo de lectura: {tiempo_lectura_fin - tiempo_lectura_inicio}")
        
        inicio_envio = time.perf_counter()
        sock.sendall(contenido.encode())
        fin_envio = time.perf_counter()
        print(f"Tiempo de envio: {fin_envio - inicio_envio}")
    finally:
        print("Cerrando la conexión")
        sock.close()