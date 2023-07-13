import time
from multiprocessing import Process, cpu_count,Pool

def hallar_sumatoria(num: int):
    suma = 0
    while num > 0:
        suma = suma + (2 * num - 1)
        num = num - 1
    
    return suma
    
resultados = []


def hallar_sumatoria_paralell(args):
    menor = int(args[0])
    mayor = int(args[1])
    
    suma = 0
    while mayor > (menor - 1):
        suma = suma + (2 * mayor - 1)
        mayor = mayor - 1
    
    return suma
    
def sumatoria_multiprocess(n:int, cantProcesos:int):
    args = [n]
    proces = Pool(processes= cantProcesos)
    result = proces.map(hallar_sumatoria, args)
    proces.close()
    proces.join()
    return result 
    
    
if __name__ == '__main__':
    lista_n = [1000000, 500000, 100000, 10000, 1000]
    num_Proceso = 1
    texto = ""
    for item in lista_n:
        texto += f"Número de procesos : {num_Proceso}\n"
        #serial 
        inicio_serial = time.perf_counter()
        sumatoria_serial = hallar_sumatoria(item)
        fin_serial = time.perf_counter()
        tiempo_serial = fin_serial-inicio_serial
        print(f"el valor de la suma es {sumatoria_serial} para el numero {item}")
        texto += f"Tiempo de ejecución serial para n {item} : {tiempo_serial}s\n"
       # print(f"La sumatoria de los valores de n {lista_n} es {resultados}")
       #Paralelo
        cantProcesos = cpu_count()
        tam_segmento = item/cantProcesos
        inicio_paralelo = time.perf_counter()
        jobs = []
        for i in range(0,cantProcesos):
            jobs.append((i*tam_segmento+1, (i+1)*tam_segmento))
        pool = Pool(cantProcesos).map(hallar_sumatoria_paralell, jobs)
        result = sum(pool)
        suma = result
        fin_paralelo = time.perf_counter()
        #args = [item]
        #proces = Pool(processes= cantProcesos)
        #sumatoria_multproc = proces.map(hallar_sumatoria, args)
        #proces.close()
        #proces.join()
        tiempo_paralelo = fin_paralelo-inicio_paralelo
        print(f"el valor de la suma es {suma} para el numero {item}")
        texto += f"Tiempo de ejecución paralela para n {item}: {tiempo_paralelo}s\n"
        #print(f" La lista de resultados es {result_paralelo}")
        assert(sumatoria_serial == suma)
        
        num_Proceso += 1
        speedup = tiempo_serial / tiempo_paralelo
        
        print(f"En el proceso {num_Proceso-1}, el speedup del número {item} es {speedup}")
       
    with open('ResultadoPreg1.txt', 'w') as file:
        file.write(texto)
    # for item in lista_n:
    #    numProcesos = cpu_count()
    #
     #   manager = Manager()
      #  resultado = manager.list()

       # for i in range(1,numProcesos+1):
        #    procs = Process(target = sumatoria_paralelizada, args = (item*i/numProcesos, i, resultado) )
         #   procs.start()
          #  procs.join()
        
   # print( f" lista : {resultado}")
             
