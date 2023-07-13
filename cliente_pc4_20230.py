import socket
import time
import random
import pickle
SOCK_BUFFER = 999999
equipos = ['ATL','BOS','BRK','CHA','DAL','DEN','DET','GSW','LAC','LAL','MEM','MIA','NOP','NYK','OKC','ORL','POR','SAC','SAS','SEA','WAS','CHI','CLE','UTA','HOU','IND','MIL','MIN','PHI','PHX','TOR','BOL'] #CONTIENE EL NOMBRE DE CADA EQUIPO QUE PARTICIPARA EN LA FASE DE GRUPOS

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("192.168.1.6", 5000)

    print(f"Conectando a {server_address[0]}:{server_address[1]}")

    sock.connect(server_address)
    client_id = random.randint(0, 1000)
    print("Dime tu nombre")
    nombre = input()
    sock.sendall(nombre.encode("utf-8"))
    confirmacion = sock.recv(SOCK_BUFFER)
    print(confirmacion) 
    print(f"Bienvenido al simulador de mundial de clubes fake, {nombre}")
    while True:
        print("Ingresa una de las siguientes frases claves :")
        print("equipos - fase de grupos asincronico - fase de grupos sincronico - eliminatorias asincronico - eliminatorias sincronico - reporte - quit")
        msg = input()
        msg_copy = msg
        msg = msg.encode("utf-8")
        sock.sendall(msg)
        if msg == "quit".encode("utf-8"):
            break
        rpta = sock.recv(SOCK_BUFFER)
        if msg_copy != 'reporte':#En el reporte no se hace eso porque lo que se recepciona no requiere aplicarle esa funcion
            rpta = pickle.loads(rpta)
                  
        if msg_copy == "equipos":
            for i in range(len(rpta)):
                print("Lista TOP 5 jugadores del",equipos[i],":",rpta[i]) # para que no se vea tan feo, le doy algo de forma
        else:
            print(rpta) # Solo retorna la lista
        time.sleep(3)
    print("Gracias por usar este simulador :)")
    sock.close()