import os
import time
import socket
from statistics import mode
from collections import Counter


def leer_Archivo(nombre_directorio):
    archivo_nombre = nombre_directorio + "/" + "Lab4_viernes.csv"
    with open (archivo_nombre, "r") as f:
        contenido = f.read()
    lineas = contenido.split("\n")
    dateCrawled = []
    name = []
    seller = []
    offerType = []
    price = []
    abtest = []
    vehicleType = []
    yearofRegistration = []
    gearbox = []
    powerPS = []
    model = []
    kilometer = []
    monthOfRegistration = []
    fuelType = []
    brand = []
    notRepairedDamage = []
    dateCreated = []
    nrOfPictures = []
    postalCode = []
    lastSeen = []
    
    idx = 0
    for linea in lineas:
        if idx == 0:
            idx = idx + 1
            continue
        if linea == "":
            continue
        datos = linea.split(",")
    
    dateCrawled.append(datos[0]) 
    name.append(datos[1])
    seller.append(datos[2])
    offerType.append(datos[3])
    price.append(datos[4])
    abtest.append(datos[5])
    vehicleType.append(datos[6])
    yearofRegistration.append(datos[7])
    gearbox.append(datos[8])
    powerPS.append(datos[9])
    model.append(datos[10])
    kilometer.append(datos[11])
    monthOfRegistration.append(datos[12])
    fuelType.append(datos[13])
    brand.append(datos[14])
    notRepairedDamage.append(datos[15])
    dateCreated.append(datos[16])
    nrOfPictures.append(datos[17])
    postalCode.append(datos[18])
    lastSeen.append(datos[19])
    
    return dateCrawled,name,seller,offerType,price,abtest,vehicleType,yearofRegistration,gearbox,powerPS,model,kilometer,monthOfRegistration,fuelType,brand,notRepairedDamage,dateCreated,nrOfPictures,postalCode,lastSeen
    
def lista_horas_dia(lista_dias):
    lista_dias_aux = lista_dias
    lista_horas = []
    for i in range(len(lista_dias_aux)):
        lista_aux = lista_dias_aux[i].split(' ')
    try:
        lista_horas.append(lista_aux[1])
    except:
        pass
    hora_max = mode(lista_horas)
    
    return hora_max 
        
        

def lista_combustibles_autos_masPopular(lista_combustibles):
    lista_tipos_comb = []
    lista_autos = []
    mas_popular = 0
    lista_tipos_comb = list(Counter(lista_combustibles).keys())
    lista_autos = list(Counter(lista_combustibles).values())
    mas_popular = mode(lista_combustibles)
    return lista_tipos_comb, lista_autos, mas_popular
    
def lista_Autos_Marca(lista_marcaAutos):
    lista_carros = []
    lista_marcas = []
    lista_marcas = list(Counter(lista_marcaAutos).keys())
    lista_carros = list(Counter(lista_marcaAutos).values())
    return lista_marcas, lista_carros

    
    
    
if __name__ == "__main__":
    ruta = os.getcwd()
    dateCrawled, name,seller,offerType,price,abtest,vehicleType,yearofRegistration,gearbox,powerPS,model,kilometer,monthOfRegistration,fuelType,brand,notRepairedDamage,dateCreated,nrOfPictures, postalCode, lastSeen = leer_Archivo(ruta) 
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_address = ("0.0.0.0", 4000)
    
    print(f"Iniciando servidor en {server_address[0]} en el puerto {server_address[1]}")
    sock.bind(server_address)
    sock.listen(5)
    
    while True:
        print("Esperando conexión ...")
        conn,addr = sock.accept()
        try:
            print(f"Conexión establecida con {addr}")
            while True:
                data = conn.recv(1024)
                print(f"Recibido {data}")
                if data == b"hora":
                    mensaje_horaMax = f"La hora del dia en donde se recolecta más : {lista_horas_dia(dateCrawled)}"
                    print(mensaje_horaMax)
                    conn.sendall(mensaje_horaMax.encode("utf-8"))
                elif data == b"combustibles":
                    list_Comb, list_autos, masPopular = lista_combustibles_autos_masPopular(fuelType)
                    mensaje_Combustibles = f"Los tipos de combustibles son: {list_Comb}  "
                    mensaje_Combustibles = mensaje_Combustibles + f" Los tipos de autos que los consumen: {list_autos}  "
                    mensaje_Combustibles = mensaje_Combustibles + f" El combustible más popular es: {masPopular}  "
                    conn.sendall(mensaje_Combustibles.encode("utf-8"))
                elif data == b"autos":
                    lista_marcas , lista_carros = lista_Autos_Marca(brand)
                    mensaje_MarcasAutos = f" La lista de marcas de autos es: {lista_marcas}"
                    mensaje_MarcasAutos = mensaje_MarcasAutos + f" La lista de los autos que son de cada marca {lista_carros}"
                    conn.sendall(mensaje_MarcasAutos.encode("utf-8"))
                else:
                    print("No hay más datos")
                    break
        except Exception as e:
            print(f"Excepcion {e}")
        finally:
            print("Cerrando conexión con el cliente")
            conn.close()
            
                    
                
                
    
    
    
    
    