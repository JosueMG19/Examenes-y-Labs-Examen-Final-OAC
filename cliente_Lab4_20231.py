

import socket 
import time 


try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("0.0.0.0", 4000)

    sock.connect(server_address)

    inicio_envio = time.perf_counter()
    num_empleados_msg = int(input("Ingresar el número de empleados mejor pagados que quiera solicitar: "))
    sock.sendall(num_empleados_msg.encode())
    fin_envio = time.perf_counter()
    print(f"Tiempo de envío: {fin_envio - inicio_envio}")

    inicio_recepcion = time.perf_counter()
    msg = sock.recv(1024)
    print(msg.decode())
    fin_recepcion = time.perf_counter()
    print(f"Tiempo de recepción: {fin_recepcion - inicio_recepcion}")


except ConnectionRefusedError:
    print("Conexión cerrada ")

finally:
    sock.close()


