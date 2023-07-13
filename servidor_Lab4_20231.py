
import socket 
import time
import matplotlib.pyplot as plt

def leer_datos(contenido):
    lineas  = contenido.split("\n")
    first_name = []
    last_name = []
    age = []
    email = []
    gender = []
    salary = []

    idx = 0
    for linea in lineas:
        if idx ==0:
            idx = idx + 1
            continue
        if linea == "":
            continue
        datos = linea.split(",")
    
    first_name.append(datos[0])
    last_name.append(datos[1])
    age.append(datos[2])
    email.append(datos[3])
    gender.append(datos[4])
    salary.append(datos[5])

    return first_name, last_name, age, email, gender, salary


def obtener_mayores_salarios(lista, numero):
    max = lista[0]
    for x in lista:
        lista_max = []
        if x > max:
            max = x 
    lista_max.append(max)        
    
    return lista_max
            


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

    server_address =("0.0.0.0", 4000)

    sock.bind(server_address)
    sock.listen()

    while True:
        conn, addr = sock.accept()
        print(f"Conectado a {addr}")
        with conn:
            inicio_recepcion = time.perf_counter()
            msg_recib = conn.recv(1024)
            num_empleados = msg_recib.decode()
            fin_recepcion = time.perf_counter()
            print(f"Tiempo de recepcion: {fin_recepcion - inicio_recepcion}")
            
            inicio_lectura = time.perf_counter()
            with open("empleados.csv", "r") as file:
                contenido = file.read()
            fin_lectura = time.perf_counter()
            print(f"Tiempo de lectura: {fin_lectura - inicio_lectura}")

            inicio_proceso = time.perf_counter()
            first_name, last_name,age, email, gender,salary = leer_datos(contenido)
            gender.sort()
            mayores_salarios = obtener_mayores_salarios(salary, num_empleados)
            print(f" los mayores son {mayores_salarios} ")
            msg_enviar = ",".join(mayores_salarios)
            msg_enviar = msg_enviar.encode()
            conn.sendall(msg_enviar)
            fin_proceso = time.perf_counter()
            print(f"Tiempo de proceso: {fin_proceso - inicio_proceso}")
        
        read_times = []
        sort_times = []
        send_times = []
        lista_N = [i for i in range(100,5001,100)]
        
        
        
        conn.close()
        
        
    
    
     



    