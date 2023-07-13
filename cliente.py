import socket
import time


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost',4000)
    print(f"Conectando a {server_address[0]} en el puerto {server_address[1]}")
    
    s.connect(server_address)
    
    msg = input("Ingrese cualquiera de las opciones (hora, combustible, marca, kilometros o cerrar sesion): ")
    msg = msg.encode("utf-8")
    inicio_time = time.perf_counter()
    s.sendall(msg)
    fin_time = time.perf_counter()
    print(f"Tiempo de transmisión: {fin_time - inicio_time} segundos")
    
    amnt_recvd = 0
    amnt_expected =len(msg)
    total_data = b""
    
    inicio_io = time.perf_counter()
    while amnt_recvd < amnt_expected:
        data = s.recv(1024)
        total_data += data
        amnt_recvd += len(data)
        print(f"Recibido parcial: {data}")
    fin_io = time.perf_counter()
    
    print(f"Tiempo de recepción: {fin_io - inicio_io} segundos")
    
    total_data = total_data.decode()
    print(f"{total_data}")
    
    s.close()
    
        