
import math 
import os 
import time

def calcular_velocidad_escritura(nombre_directorio):
    contenido = "The quick brown bull jumps over the dog."
    iteracion = int(pow(10,6) / 40)
    print(iteracion)
    archivo_nombre = nombre_directorio + "/" + "texto.txt"
    print(archivo_nombre)
    inicio_io = time.perf_counter()
    with open(archivo_nombre, "w") as file:
        for i in range(iteracion):
            file.write(contenido)
    fin_io = time.perf_counter()
    total_time = fin_io - inicio_io   
    return 1/ total_time 

if __name__ == '__main__':
    print("Escritura de escritorio:  ",  calcular_velocidad_escritura(os.getcwd()))
    
    

    