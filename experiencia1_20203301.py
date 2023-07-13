import asyncio 
import time
import random

lista_resultados = [['Magnus', 0], ['Vladimir',0], ['Peter',0], ['Levon',0]]
lista_final_ajedrez = [['Anand', 0]]

def leer_archivo_csv():
    idx = 0
    lista_jugadores = []
    with open("players.csv" , "r") as f:
        contenido = f.read()
    
    lineas = contenido.split("\n")
    
    for linea in lineas:
        if idx == 0:
            idx += 1
            continue
        if linea == "":
            continue
        jugador = linea.split(";")
        lista_jugadores.append(jugador)
    lista_jugadores = dict(lista_jugadores)
    return lista_jugadores 

# -----------------------------Funciones para la fase de rondas-----------------------------
async def fase_dias_async(lista, dia):
    if dia == 1:
        if lista['Vladimir'] > lista['Magnus'] :
            lista_resultados[1][1] = lista_resultados[1][1] + 1
        else:
            lista_resultados[0][1] = lista_resultados[0][1] + 1
        
        if lista['Levon'] > lista['Peter'] :
            lista_resultados[3][1] = lista_resultados[3][1] + 1
        else:
            lista_resultados[2][1] = lista_resultados[2][1] + 1

    if dia == 2:
        if lista['Peter'] > lista['Magnus'] :
            lista_resultados[2][1] = lista_resultados[2][1] + 1
        else:
            lista_resultados[0][1] = lista_resultados[0][1] + 1
        
        if lista['Levon'] > lista['Vladimir'] :
            lista_resultados[3][1] = lista_resultados[3][1] + 1
        else:
            lista_resultados[1][1] = lista_resultados[1][1] + 1
   
    if dia == 3:
        if lista['Levon'] > lista['Magnus'] :
            lista_resultados[3][1] = lista_resultados[3][1] + 1
        else:
            lista_resultados[0][1] = lista_resultados[0][1] + 1
        
        if lista['Vladimir'] > lista['Peter'] :
            lista_resultados[1][1] = lista_resultados[1][1] + 1
        else:
            lista_resultados[2][1] = lista_resultados[2][1] + 1
    
    await asyncio.sleep(0.15)   

    return None

def obtener_valor(tupla):
    return tupla[1]

async def fase_rondas_async():
    lista_jugadores = leer_archivo_csv()
    tasks = []
    for dia in range (1,4):
        tasks.append(asyncio.create_task(fase_dias_async(lista_jugadores, dia)))
    await asyncio.gather(*tasks)
    
    diccionario_resultados = dict(lista_resultados)
    
    return max (diccionario_resultados.items(), key=obtener_valor)[0]

def fase_dias_sync(lista,dia):
    if dia == 1:
        if lista['Vladimir'] > lista['Magnus'] :
            lista_resultados[1][1] = lista_resultados[1][1] + 1
        else:
            lista_resultados[0][1] = lista_resultados[0][1] + 1
        
        if lista['Levon'] > lista['Peter'] :
            lista_resultados[3][1] = lista_resultados[3][1] + 1
        else:
            lista_resultados[2][1] = lista_resultados[2][1] + 1

    if dia == 2:
        if lista['Peter'] > lista['Magnus'] :
            lista_resultados[2][1] = lista_resultados[2][1] + 1
        else:
            lista_resultados[0][1] = lista_resultados[0][1] + 1
        
        if lista['Levon'] > lista['Vladimir'] :
            lista_resultados[3][1] = lista_resultados[3][1] + 1
        else:
            lista_resultados[1][1] = lista_resultados[1][1] + 1
   
    if dia == 3:
        if lista['Levon'] > lista['Magnus'] :
            lista_resultados[3][1] = lista_resultados[3][1] + 1
        else:
            lista_resultados[0][1] = lista_resultados[0][1] + 1
        
        if lista['Vladimir'] > lista['Peter'] :
            lista_resultados[1][1] = lista_resultados[1][1] + 1
        else:
            lista_resultados[2][1] = lista_resultados[2][1] + 1
    
    time.sleep(0.15)   

    return None

def fase_rondas_sync():
    lista_jugadores = leer_archivo_csv()
    for dia in range (1,4):
       fase_dias_sync(lista_jugadores, dia)
    diccionario_resultados = dict(lista_resultados)
    return max (diccionario_resultados.items(), key=obtener_valor)[0]
    
#-----------------------Funciones para la fase final ----------------------------------------------------------------
async def partida_final_async():
    #0 si es que gana Anand, 1 si es que gana el ganador de las rondas y 2 si empatan
    num_random = random.randint(0,2)
    
    if num_random == 0:
        lista_final_ajedrez[0][1] = lista_final_ajedrez[0][1] + 1
    
    if num_random == 1:
        lista_final_ajedrez[1][1] = lista_final_ajedrez[1][1] + 1
    
    if num_random == 2:
        lista_final_ajedrez[0][1] = lista_final_ajedrez[0][1] + 0.5    
        lista_final_ajedrez[1][1] = lista_final_ajedrez[1][1] + 0.5
        
    await asyncio.sleep(0.15)

    return None

async def fase_final_async():
    tasks = []
    for _ in range (1,13):
        tasks.append(asyncio.create_task(partida_final_async()))
    await asyncio.gather(*tasks)
    
    diccionario_resultados = dict(lista_final_ajedrez)
    return max (diccionario_resultados.items(), key=obtener_valor)[0]

def partida_final_sync():
    #0 si es que gana Anand, 1 si es que gana el ganador de las rondas y 2 si empatan
    num_random = random.randint(0,2)
    
    if num_random == 0:
        lista_final_ajedrez[0][1] = lista_final_ajedrez[0][1] + 1
    
    if num_random == 1:
        lista_final_ajedrez[1][1] = lista_final_ajedrez[1][1] + 1
    
    if num_random == 2:
        lista_final_ajedrez[0][1] = lista_final_ajedrez[0][1] + 0.5    
        lista_final_ajedrez[1][1] = lista_final_ajedrez[1][1] + 0.5
        
    time.sleep(0.15)

def fase_final_sync():
    num_partida = 0
    while lista_final_ajedrez[0][1] <= 6.5 or lista_final_ajedrez[1][1] <= 6.5:
        num_partida = num_partida + 1
        partida_final_sync()
    print(f"Numero de partidas hasta llegar a 6.5 puntos : {num_partida}")
    diccionario_resultados = dict(lista_final_ajedrez)
    return max (diccionario_resultados.items(), key=obtener_valor)[0]


#----------------------------MAIN----------------------------------
if __name__ == "__main__":
    lista_jugadores = leer_archivo_csv()
    print(lista_jugadores)
    
    inicio_ronda_async = time.perf_counter()
    ganador_rondas_async = asyncio.run(fase_rondas_async())
    print(ganador_rondas_async)
    fin_ronda_async = time.perf_counter()
    
    print(f"El tiempo de ejecución para la funcion asincrona es {fin_ronda_async - inicio_ronda_async} segundos")
    
    inicio_ronda_sync = time.perf_counter()
    ganador_rondas_sync = fase_rondas_sync()
    print(ganador_rondas_sync)
    fin_ronda_sync = time.perf_counter()
    
    print(f"El tiempo de ejecución para la funcion sincrona es {fin_ronda_sync - inicio_ronda_sync} segundos")
    
    
    lista_final_ajedrez.append([ganador_rondas_async,0])

    inicio_final_async = time.perf_counter()    
    ganador_final_async = asyncio.run(fase_final_async())
    print(ganador_final_async)
    fin_final_async = time.perf_counter()
    
    print(f"El tiempo de ejecución para la funcion asincrona es {fin_final_async - inicio_final_async}")
  
    inicio_final_sync = time.perf_counter() 
    ganador_final_sync = fase_final_sync()
    print(ganador_final_sync)
    fin_final_sync = time.perf_counter()
    
    print(f"El tiempo de ejecución para la funcion sincrona es {fin_final_sync - inicio_final_sync}")
        
    
    


                                         
    
    
    