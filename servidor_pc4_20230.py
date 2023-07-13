import random
import asyncio
import itertools
import time
from threading import Thread
import socket
import pickle
equipos = ['ATL','BOS','BRK','CHA','DAL','DEN','DET','GSW','LAC','LAL','MEM','MIA','NOP','NYK','OKC','ORL','POR','SAC','SAS','SEA','WAS','CHI','CLE','UTA','HOU','IND','MIL','MIN','PHI','PHX','TOR','BOL'] #CONTIENE EL NOMBRE DE CADA EQUIPO QUE PARTICIPARA EN LA FASE DE GRUPOS

listas_jugadores_equipos = [[] for _ in range(len(equipos))] #LISTA DE TOP 5 JUGADORES DE CADA EQUIPO,EN EL MISMO ORDEN DE COMO ESTA EN EL ARREGLO "EQUIPOS"
clasificados_async = []#lista de equipos clasificados en la fase de grupos asincronica
clasificados_sync = []#lista de equipos clasificados en la fase de grupos sincronica
jugadores = [] # CONTIENE LA INFORMACION DE UN JUGADOR EN EL FORMATO: NOMBRE,EQUIPO,PTS TOTALES, MINUTOS TOTALES
puntosPromd = []
SOCK_BUFFER = 1024
num_clientes = 0
t_grupos_async = 0
t_grupos_sync = 0
t_elim_async = 0
t_elim_sync = 0
#Para mover el cursor del mouse para leer partes especificas del archivo .csv
def moverCursor(linea,pos):
    i = 0
    contador = 0
    while(contador<=pos):
        if(linea[i]==';'):
            contador = contador + 1
        i = i + 1
    return i

#Funcion para leer un str cualquiera
def leerPalabra(linea,i):
    palabra = ""
    while(linea[i]!=';'):
                palabra +=linea[i]
                i = i + 1
    return palabra

#Funcion para sumarle valores a los acumuladores de cada jugador
def asignarValores(jugador,puntaje,minutos):
    i=jugadores.index(jugador)#posicion del nombre del jugador
    j = i + 2 #Posicion de su puntaje
    k = j + 1 #Posicion de los minutos
    jugadores[j]+=puntaje
    jugadores[k]+=minutos

#En esta función leemos el archivo .csv y llenamos el arreglo de jugadores con sus datos
def leerDatos():
    with open("datos.csv","r") as arch:
        arch.readline()
        while True:
            linea=arch.readline()
            if not linea:
                break

            i = moverCursor(linea,3)# 3: pos del nombre del equipo
            equipo = leerPalabra(linea,i)
            
            if equipo in equipos:
                i = moverCursor(linea,2) # 2: pos del nombre del jugador
                jugador = leerPalabra(linea,i)

                i = moverCursor(linea,5) #5: pos de los minutos jugados
                minutos = leerPalabra(linea,i)
                if minutos !='':
                    minutosNum = float(minutos)
                else:
                    minutosNum = 0

                i = moverCursor(linea,20) #20: pos de los puntos
                puntos = leerPalabra(linea,i)
                if puntos !='':
                    puntosNum = int(puntos)
                else:
                    puntosNum = 0
                if not jugador in jugadores:
                    jugadores.append(jugador)#nombre del jugador
                    jugadores.append(equipo)#nombre de su equipo
                    jugadores.append(puntosNum)# inicializando sus puntos totales
                    jugadores.append(minutosNum)# inicializando sus minutos totales
                else:
                    asignarValores(jugador,puntosNum,minutosNum)

#Funcion para calcular el puntaje promedio de todos los equipos y almacenarlo en una lista
def calcularPuntajePromd():
    for i in range(len(equipos)):
        k = 1
        contador = 0 #La cuenta de los jugadores por equipo
        puntaje = 0 # la suma de los puntos de los jugadores de cada equipo
        while(k<len(jugadores)):
            if(jugadores[k] == equipos[i]):
               puntaje += jugadores[k+1]
               contador +=1
            k+=4
        promedio = puntaje/contador
        puntosPromd.append(promedio)

#ESTA FUNCION ORDENA DE MANERA DESCENDENTE UNA LISTA CON RESPECTO AL SEGUNDO PARAMETRO
def ordenar(li1, li2):
    lista_unida = list(zip(li1, li2))#uniendo ambas listas
    lista_ordenada = sorted(lista_unida, key=lambda x: x[1], reverse=True) #orden descendente
    return [jugador[0] for jugador in lista_ordenada]

def hallarTOP5minutosJugados(equipo,i):
    listas_jugadores = []
    k = 3 #posicion de los minutos jugados del primer jugador de la lista
    cantJug = 0 #contador de jugadores en el top
    lista_minutos =[] #lista de los minutos de los jugadores en el top
    while(k<len(jugadores)):
        if(jugadores[k-2]==equipo):
            if(cantJug<5):
                listas_jugadores.append(jugadores[k-3])
                lista_minutos.append(jugadores[k])
                cantJug += 1
            else:
                listas_jugadores=ordenar(listas_jugadores,lista_minutos)
                for j in range(len(listas_jugadores)):
                    if jugadores[k]>lista_minutos[j]:
                        lista_minutos.insert(j,jugadores[k])#insertamos la cant de minutos
                        listas_jugadores.insert(j,jugadores[k-3])# y el nombre del jugador
                        cantJug-=1
                        break
        k +=4#siguiente
    return listas_jugadores

def generarListaDeJugadores():
    for i in range(len(listas_jugadores_equipos)):
        lista_jugadores=hallarTOP5minutosJugados(equipos[i],i)
        listas_jugadores_equipos[i] = lista_jugadores[:5] #COPIAMOS EL TOP 5 AL ARREGLO GLOBAL

#Funcion para generar un ganador aleatorio entre 2 equipos
def partido(equipo1,equipo2):
    numero_x = random.random() # numero aleatorio entre 0 a 1
    if(round(numero_x)==0): #lo redondeo para que salga o bien 0 o bien 1
        return equipo1
    else:
        return equipo2

async def jugar_partido_grupo_async(equipo1, equipo2,puntosPromd,puntos):
    print(f"BIENVENIDOS AL PARTIDO ENTRE {equipo1} vs. {equipo2}")
    await asyncio.sleep(0.15)
    idx1 = equipos.index(equipo1)
    idx2 = equipos.index(equipo2)
    #SUPONEMOS QUE NO HAY EMPATES
    if(puntosPromd[idx1]>puntosPromd[idx2]):
        puntos[equipo1] +=3
    else:
        puntos[equipo2] +=3
    print(f"FINAL DEL PARTIDO ENTRE {equipo1} vs. {equipo2}")

#Funcion principal para simular la fase de grupos de manera asincronica
async def grupos_async():
    idx = 0
    c_async = []
    for k in range(8):
        equipos_grupo = []
        for i in range(4):
            equipos_grupo.append(equipos[idx])
            idx += 1
        puntos_grupo = {equipo: 0 for equipo in equipos_grupo} #diccionario para seguir los puntos de cada equipo
        print(f"COMIENZAN LOS PARTIDOS DEL GRUPO {k+1}")
        partidos = list(itertools.combinations(equipos_grupo, 2))#contiene todas las combinaciones posibles de partidos
        resolucion = [jugar_partido_grupo_async(equipo1, equipo2,puntosPromd,puntos_grupo) for equipo1, equipo2 in partidos]
        await asyncio.gather(*resolucion)
        clasificacion = sorted(puntos_grupo.items(), key=lambda x: x[1], reverse=True)#ordenamos la clasificacion de manera descendente (mayor a menor)
        print(f"FINAL DEL GRUPO {k+1}")
        print("Clasificación final:")
        contadorTop = 0
        for equipo, puntos in clasificacion:
            if(contadorTop<2):
                c_async.append(equipo)
            print(f"{equipo}: {puntos} puntos")
            contadorTop+=1
    print("FIN DE LA FASE DE GRUPOS")
    return c_async

def jugar_partido_grupo_sync(equipo1, equipo2,puntosPromd,puntos):
    print(f"BIENVENIDOS AL PARTIDO ENTRE {equipo1} vs. {equipo2}")
    time.sleep(0.15)
    idx1 = equipos.index(equipo1)
    idx2 = equipos.index(equipo2)
    #SUPONEMOS QUE NO HAY EMPATES
    if(puntosPromd[idx1]>puntosPromd[idx2]):
        puntos[equipo1] +=3
    else:
        puntos[equipo2] +=3
    print(f"FINAL DEL PARTIDO ENTRE {equipo1} vs. {equipo2}")

#Funcion principal para simular la fase de grupos de manera sincronica
def grupos_sync():
    idx = 0
    c_sync = []
    for k in range(8):
        equipos_grupo = []
        for i in range(4):
            equipos_grupo.append(equipos[idx])
            idx += 1
        puntos_grupo = {equipo: 0 for equipo in equipos_grupo} #diccionario para seguir los puntos de cada equipo
        print(f"COMIENZAN LOS PARTIDOS DEL GRUPO {k+1}")
        partidos = list(itertools.combinations(equipos_grupo, 2))#contiene todas las combinaciones posibles de partidos
        for equipo1,equipo2 in partidos:
            jugar_partido_grupo_sync(equipo1, equipo2,puntosPromd,puntos_grupo) 
        clasificacion = sorted(puntos_grupo.items(), key=lambda x: x[1], reverse=True)#ordenamos la clasificacion de manera descendente (mayor a menor)
        print(f"FINAL DEL GRUPO {k+1}")
        print("Clasificación final:")
        contadorTop = 0
        for equipo, puntos in clasificacion:
            if(contadorTop<2):
                c_sync.append(equipo)
            print(f"{equipo}: {puntos} puntos")
            contadorTop+=1
    print("FIN DE LA FASE DE GRUPOS")
    return c_sync

async def simularFase2(equipos_grupo,puntos_grupo,equipo1,equipo2):
        print(f"partido entre {equipo1} y {equipo2}")
        ganador=partido(equipo1,equipo2)
        asyncio.sleep(0.15)
        idxGanador = equipos_grupo.index(ganador)
        puntos_grupo[idxGanador]+=3

async def fase2_async(clasificados_elim):
    k=0
    for i in range(4):
        equipos_grupo = []
        #creamos el grupo con el primero y el segundo de 2 grupos consecutivos
        for j in range(2):
            equipos_grupo.append(clasificados_async[k+j*2])
            equipos_grupo.append(clasificados_async[k+1+j*2])
        k+=4
        puntos_grupo = [0,0,0,0] #inicializamos los puntos de cada equipo
        print(f"COMIENZAN LOS PARTIDOS DEL GRUPO {i+1} POR LA FASE 2")
        partidos = list(itertools.combinations(equipos_grupo, 2))#contiene todas las combinaciones posibles de partidos
        await asyncio.gather(*[simularFase2(equipos_grupo,puntos_grupo,equipo1,equipo2) for equipo1, equipo2 in partidos])#simulando fase 2 todos los partidos a la vez
        equipos_grupo=ordenar(equipos_grupo,puntos_grupo)#ordenamos la clasificacion de manera ascendente (mayor a menor)
        clasificados_elim.append(equipos_grupo[0])
        clasificados_elim.append(equipos_grupo[1])
        print(f"FINAL DEL GRUPO {i+1}")
        print("Ganadores:")
        print(equipos_grupo[0],equipos_grupo[1])

async def simularEliminatoria(equipos,equipo1,equipo2):
        print(f"partido entre {equipo1} y {equipo2}")
        ganador=partido(equipo1,equipo2)
        asyncio.sleep(0.15)
        return ganador

async def eliminatorias_enfrentamientos_async(clasificados_elim):
    #creando emparejamientos contenidos en una lista de tuplas
    emparejamientos = [(clasificados_elim[0],clasificados_elim[3]),(clasificados_elim[4],clasificados_elim[7]),(clasificados_elim[1],clasificados_elim[2]),(clasificados_elim[5],clasificados_elim[6])]
    emparejamientos = await asyncio.gather(*[simularEliminatoria(clasificados_elim,equipo1,equipo2) for equipo1, equipo2 in emparejamientos])
    print(f"PASARON A SEMIFINALES:{emparejamientos}")
    copia = emparejamientos #copia para posteriormente hacer la operacion (**op**)
    emparejamientos = [(emparejamientos[0],emparejamientos[1]),(emparejamientos[2],emparejamientos[3])]
    emparejamientos = await asyncio.gather(*[simularEliminatoria(clasificados_elim,equipo1,equipo2) for equipo1, equipo2 in emparejamientos])
    print(f"PASARON A LA GRAN FINAL:{emparejamientos}")
    eliminados = list(set(copia) - set(emparejamientos))#ESTA ES LA OPERACION **op** la cual excluye los valores de que no se repiten en la copia de los de emparejamientos, asi obteniendo quienes juegan el partido de tercer y cuarto puesto
    print(f"JUEGAN POR EL TERCER Y CUARTO PUESTO:{eliminados}")
    tercerpuesto=partido(eliminados[0],eliminados[1])
    primerPuesto=partido(emparejamientos[0],emparejamientos[1])
    idx = emparejamientos.index(primerPuesto)
    emparejamientos.pop(idx) #elimino al que quedo primer puesto, para que solo quede el segundo
    segundoPuesto = emparejamientos[0]
    Podio = [primerPuesto,segundoPuesto,tercerpuesto]
    print("FIN DEL CAMPEONATO")
    print("EL PODIO QUEDO ASÍ:")
    print(f"Primer puesto:{primerPuesto}")
    print(f"Segundo puesto:{segundoPuesto}")
    print(f"Tercer puesto:{tercerpuesto}")
    return Podio

#FUNCION PRINCIPAL ELIMINATORIAS SINCRONICA
async def eliminatorias_async():
    clasificados_elim=[]
    await fase2_async(clasificados_elim)
    print("FIN DE LA FASE 2, PASAMOS A LA RONDA DE ELMINACION DIRECTA")
    print("MUCHA SUERTE A LOS EQUIPOS FINALISTAS:",clasificados_elim)
    Podio = await eliminatorias_enfrentamientos_async(clasificados_elim)
    return Podio

def fase2_sync(clasificados_elim):
     k=0
     for i in range(4):
        equipos_grupo = []
        #creamos el grupo con el primero y el segundo de 2 grupos consecutivos
        for j in range(2):
            equipos_grupo.append(clasificados_sync[k+j*2])
            equipos_grupo.append(clasificados_sync[k+1+j*2])
        k+=4
        puntos_grupo = [0,0,0,0] #inicializamos los puntos de cada equipo
        print(f"COMIENZAN LOS PARTIDOS DEL GRUPO {i+1} POR LA FASE 2")
        partidos = list(itertools.combinations(equipos_grupo, 2))#contiene todas las combinaciones posibles de partidos
        for equipo1,equipo2 in partidos:
            simularFase2_sync(equipos_grupo,puntos_grupo,equipo1,equipo2)
        equipos_grupo=ordenar(equipos_grupo,puntos_grupo)#ordenamos la clasificacion de manera ascendente (mayor a menor)
        clasificados_elim.append(equipos_grupo[0])
        clasificados_elim.append(equipos_grupo[1])
        print(f"FINAL DEL GRUPO {i+1}")
        print("Ganadores:")
        print(equipos_grupo[0],equipos_grupo[1])

def eliminatorias_enfrentamientos_sync(clasificados_elim):
    #creando emparejamientos contenidos en una lista de tuplas
    emparejamientos = [(clasificados_elim[0],clasificados_elim[3]),(clasificados_elim[4],clasificados_elim[7]),(clasificados_elim[1],clasificados_elim[2]),(clasificados_elim[5],clasificados_elim[6])]
    resultados = []
    for equipo1,equipo2 in emparejamientos:
        resultados.append(simularEliminatoria_sync(clasificados_elim,equipo1,equipo2))
    emparejamientos = resultados #actualizamos emparejamientos
    resultados = [] #lo reseteamos
    print(f"PASARON A SEMIFINALES:{emparejamientos}")
    copia = emparejamientos #copia para posteriormente hacer la operacion (**op**)
    emparejamientos = [(emparejamientos[0],emparejamientos[1]),(emparejamientos[2],emparejamientos[3])]
    for equipo1,equipo2 in emparejamientos:
        resultados.append(simularEliminatoria_sync(clasificados_elim,equipo1,equipo2))
    emparejamientos = resultados
    print(f"PASARON A LA GRAN FINAL:{emparejamientos}")
    eliminados = list(set(copia) - set(emparejamientos))#ESTA ES LA OPERACION **op** la cual excluye los valores de que no se repiten en la copia de los de emparejamientos, asi obteniendo quienes juegan el partido de tercer y cuarto puesto
    print(f"JUEGAN POR EL TERCER Y CUARTO PUESTO:{eliminados}")
    tercerpuesto=partido(eliminados[0],eliminados[1])
    primerPuesto=partido(emparejamientos[0],emparejamientos[1])
    idx = emparejamientos.index(primerPuesto)
    emparejamientos.pop(idx)#elimino al que quedo primer puesto, para que solo quede el segundo
    segundoPuesto = emparejamientos[0]
    Podio = [primerPuesto,segundoPuesto,tercerpuesto]
    print("FIN DEL CAMPEONATO")
    print("EL PODIO QUEDO ASÍ:")
    print(f"Primer puesto:{primerPuesto}")
    print(f"Segundo puesto:{segundoPuesto}")
    print(f"Tercer puesto:{tercerpuesto}")
    return Podio

def simularFase2_sync(equipos_grupo,puntos_grupo,equipo1,equipo2):
        print(f"partido entre {equipo1} y {equipo2}")
        ganador=partido(equipo1,equipo2)
        time.sleep(0.15)
        idxGanador = equipos_grupo.index(ganador)
        puntos_grupo[idxGanador]+=3


def simularEliminatoria_sync(clasificados_elim,equipo1,equipo2):
     print(f"partido entre {equipo1} y {equipo2}")
     ganador=partido(equipo1,equipo2)
     time.sleep(0.15)
     return ganador

#FUNCION PRINCIPAL ELIMINATORIAS ASINCRONICA
def eliminatorias_sync():
    clasificados_elim=[]
    fase2_sync(clasificados_elim)
    print("FIN DE LA FASE 2, PASAMOS A LA RONDA DE ELMINACION DIRECTA")
    print("MUCHA SUERTE A LOS EQUIPOS FINALISTAS:",clasificados_elim)
    Podio = eliminatorias_enfrentamientos_sync(clasificados_elim)
    return Podio

##FUNCION QUE USE PARA HACER LA PRIMERA PARTE DEL INFORME
def funcionPruebaFunciones():
    leerDatos(jugadores)
    #print(jugadores)
    calcularPuntajePromd(puntosPromd,jugadores)
    #print(puntosPromd)
   # generarListaDeJugadores(jugadores)
    #for i in range(len(listas_jugadores_equipos)):
      #  print("Lista TOP 5 jugadores del",equipos[i],":",listas_jugadores_equipos[i])
    #ganador=partido('ATL','BOS')
    #print(ganador)
    #tic = time.perf_counter()
    #clasificados_async= asyncio.run(grupos_async(puntosPromd))
   # tac = time.perf_counter()
   # T_asincronico = tac - tic
    #print(clasificados_async)
    #tic = time.perf_counter()
    clasificados_sync = grupos_sync(puntosPromd)
   # tac = time.perf_counter()
    #T_sincronico = tac - tic
   # print(clasificados_sync)
    #print(f"Tiempo de ejecucion con asincronico:{T_asincronico}")
    #print(f"Tiempo de ejecucion con sincronico:{T_sincronico}")
   # podio_async=asyncio.run(eliminatorias_async())
    podio_sync = eliminatorias_sync()

#FUNCION PARA ATENDER AL CLIENTE
def client_handler(conn, client_address):
    global num_clientes
    global listas_jugadores_equipos
    global clasificados_async
    global clasificados_sync
    global podio_async
    global podio_sync
    global t_grupos_async
    global t_grupos_sync
    global t_elim_async
    global t_elim_sync
    num_clientes += 1
    print(f"Numero de clientes conectados: {num_clientes}")
    try:
        print(f"Conexión desde {client_address}")
        data = conn.recv(SOCK_BUFFER)
        if data:
            conn.sendall("Procesando data....".encode("utf-8"))
        time.sleep(3)
        while True:
            data = conn.recv(SOCK_BUFFER)
            print(f"Recibido: {data}")
            if data == "equipos".encode("utf-8"):
                generarListaDeJugadores()
                listas_jugadores_equipos_b = pickle.dumps(listas_jugadores_equipos)#convertirlo a bytes
                conn.sendall(listas_jugadores_equipos_b)
            if data == "fase de grupos asincronico".encode("utf-8"):
                clasificados_async_b = pickle.dumps(clasificados_async)
                conn.sendall(clasificados_async_b)
            if data == "fase de grupos sincronico".encode("utf-8"):
                clasificados_sync_b = pickle.dumps(clasificados_sync)
                conn.sendall(clasificados_sync_b)
            if data == "eliminatorias asincronico".encode("utf-8"):
                podio_async_b = pickle.dumps(podio_async)
                conn.sendall(podio_async_b)
            if data == "eliminatorias sincronico".encode("utf-8"):
                podio_sync_b = pickle.dumps(podio_sync)
                conn.sendall(podio_sync_b)
            if data == "reporte".encode("utf-8"):
                datos_reporte =[clasificados_async,clasificados_sync,podio_async,podio_sync,t_grupos_async,t_grupos_sync,t_elim_async,t_elim_sync]
                with open("reporte.txt","w") as arch:
                  arch.write("Reporte de Tiempos de ejecucion ASINCRONICO VS SINCRONICO\n")
                  arch.write("Para la fase de grupos:\n")
                  arch.write(f"La lista del asincronico: {datos_reporte[0]}\n")
                  arch.write(f"La lista del sincronico: {datos_reporte[1]}\n")
                  if(datos_reporte[0] == datos_reporte[1]):
                    arch.write("Las listas son iguales, lo normal, puesto que en esta fase usualmente pasan los mejores, basado en la base de datos que tengo\n")
                  else:
                    arch.write("Las listas son diferentes, muy raro, problamente haya un fallo de programación\n")
                  arch.write(f"Tiempo de ejecucion asincronico: {datos_reporte[4]} segundos\n")
                  arch.write(f"Tiempo de ejecucion sincronico: {datos_reporte[5]} segundos\n")
                  arch.write("Para la eliminatoria:\n")
                  arch.write(f"La lista del asincronico: {datos_reporte[2]}\n")
                  arch.write(f"La lista del sincronico: {datos_reporte[3]}\n")
                  if(datos_reporte[2] == datos_reporte[3]):
                    arch.write("Las listas son iguales,muy raro pero posible\n")
                  else:
                    arch.write("Las listas son diferentes demuestra la aleatoriedad de los partidos en estas instancias\n")
                  arch.write(f"Tiempo de ejecucion asincronico: {datos_reporte[6]} segundos\n")
                  arch.write(f"Tiempo de ejecucion sincronico: {datos_reporte[7]} segundos\n")
                msg = "El reporte ha sido creado por el servidor".encode("utf-8")
                conn.sendall(msg)
            if  data =="".encode("utf-8"):
                break
    except Exception as e:
        print(f"Excepcion: {e}")
    finally:
        print("Cerrando conexión con el cliente")
        num_clientes -= 1
        conn.close()

if __name__ == '__main__':
    leerDatos()
    #funcionesPruebaFunciones(jugadores,puntosPromd)
    calcularPuntajePromd()
    tic = time.perf_counter()
    clasificados_async= asyncio.run(grupos_async())
    tac = time.perf_counter()
    t_grupos_async = tac - tic
    tic = time.perf_counter()
    clasificados_sync = grupos_sync()
    tac = time.perf_counter()
    t_grupos_sync = tac - tic
    tic = time.perf_counter()
    podio_async=asyncio.run(eliminatorias_async())
    tac = time.perf_counter()
    t_elim_async = tac - tic
    tic = time.perf_counter()
    podio_sync = eliminatorias_sync()
    tac = time.perf_counter()
    t_elim_sync = tac - tic


    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ("0.0.0.0", 5000)
    print(f"Iniciando servidor en {server_address[0]}:{server_address[1]}")
    sock.bind(server_address)

    sock.listen(1)

    while True:
        print("Esperando conexión...")

        conn, client_address = sock.accept()

        client_thread = Thread(target=client_handler, args=(conn, client_address))
        client_thread.start()