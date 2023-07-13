
# Nombre: Josué Moreno Gálvez   Código:20203301 
import time
import math 
from multiprocessing import Pool

def verificar_num_primo(n: int) -> bool :
    # Función que verifica si n es primo o no

    # Primero vamos a realizar algunos casos especiales sobre el 1 y el 2.
    if n ==1:
        return False # Esto debido a que 1 no es primo ni par
    if n ==2:
        return True # Esto debido a que 2 si es primo. Es divisible entre 1 y 2.
    
    #Luego vamos a verificar la divisibilidad hasta la raíz cuadrada de n 

    for i in range (2, int(math.sqrt(n))+ 1):
        if n % i == 0: # Si es divisible por algun numero entonces no es primo
            return False
    # de lo contrario , si es primo
    return True 

def es_primo_rango(n, rango):
    for i in range(rango[0], rango[1]):
        if n % i == 0:
            return False
    return True 

def es_num_primo_multiprocess(n:int, num_proc: int):
    #Divide el rango de numeros en sub-rangos mas pequeños
    rangos = []
    tope = int(n ** 0.5) + 1
    chunk_size = (tope - 2) // num_proc + 1
    for i in range(2,tope, chunk_size):
        fin = min(i + chunk_size, tope)
        rangos.append((i, fin))
    
    print(rangos)    
    args = zip([n] * len(rangos), rangos) # Paso como argumento el valor de n como lista : [n] para que sea un objeto iterable
    p = Pool(processes = num_proc) # Creo un Pool, el valor de processes es según el numero del num_proc.
    res = p.starmap(es_primo_rango, args) # Paso como argumento la funcion y su argumento al p.map, el cual va a realizar la ejecucion en paralelo
    p.close()
    p.join()
    return all(res) # Se retorna el valor de resultado.
 

if __name__ == "__main__":
    n= 2_345_678_911_111_111 
    
    # se va a hallar el tiempo de ejecución de la funcion que verifica que si n es primo o no con implementación serial (sin paralelismo ni concurrencia) parte a
    inicio = time.perf_counter()
    es_num_primo = verificar_num_primo(n)
    fin = time.perf_counter()
    

    # se va a hallar el tiempo de ejecución de la funcion que verifica que si n es primo o no con paralelismo (Para esto uso el multiprocessing)
    inicio_paralelo = time.perf_counter()
    result_paralelo= es_num_primo_multiprocess(n, 2) #Le paso el valor de n y el numero de procesos (2) para la parte b ,a esta función
    fin_paralelo = time.perf_counter()

    print(f"¿ El número {n} es primo ?: {es_num_primo}. Se ha demorado {fin - inicio:0.4f} segundos en ejecutar la función")
    print(f"¿ El número {n} es primo ?: {result_paralelo}. Se ha demorado {fin_paralelo - inicio_paralelo:0.4f} segundos en ejecutar la función")

    #Hallo la diferencia entre fin e inicio para hallar el tiempo de ejecución  de ambas funciones y luego con ello hallo el speedup
    tiempo_1 = fin - inicio 
    tiempo_2 = fin_paralelo - inicio_paralelo
    speedup = tiempo_1 / tiempo_2

    print(f"El speedup de ambas funciones es: {speedup:0.4f}")
    #Antes de usar el assert , realizo la parte c que es hacer con 4 , 8 y 16 procesos. Porque si pongo el assert y como ambas funciones
    #tienen diferentes valores entonces en el assert va a salir error y no podre ejecutar esa parte de mi codigo.

    #Genero una lista con el num de procesos : 4, 8 y 16
    pool_sizes = [4, 8, 16]

    #Genero una lista vacía para los tiempos de ejecución de los procesos 
    tiempos = list()

    #Recorro la lista con el numero de procesos con num_proc
    for num_proc in pool_sizes:
        print(f"Evaluando proceso número: {num_proc}")
        
        inicio_mult_proc = time.perf_counter()
        es_num_primo_multiprocess(n, num_proc) #Llamo la función de multiprocesos y le paso el valor de n y el numero de procesos de la lista
        fin_mult_proc = time.perf_counter()
        tiempos.append(fin_mult_proc - inicio_mult_proc) # Despues de realizar la funcion, su tiempo de ejecucion lo pongo en la lista de tiempos

    print("Tiempos de ejecucion para diferentes tamaños de pool:")
    #Recorro la lista de pool_sizes para obtener el proceso con su tiempo de ejecucion respectivo
    for i in range(len(pool_sizes)):
        print("Pool size: ", pool_sizes[i], "Tiempo: ", tiempos[i])

    #Al final coloco el assert.
    assert tiempo_1 == tiempo_2, "Los tiempos no son iguales"
  