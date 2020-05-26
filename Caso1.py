
from os import listdir
from os.path import isfile, join
from treelib import Node, Tree

"""En este metodo se obtienen los modelos de cada uno de los archivos que se encuentran en la carpeta models"""
def obtenerArchivos ():
    path = "./calificador/dashboard/models" #path de la carpeta models
    models={}
    onlyfiles = [f for f in listdir(path) if
                 isfile(join(path, f))] #Se extraen todos los archivos que hay en la carpeta
    for file in onlyfiles: # se recorre cada uno de los archivos
        filepath= path+"/"+file
        f = open(filepath,"r")
        arch = "".join(f)
        clases = arch.split("class") # se extraen cada de las clases definidas en cada archivo
        cla = {}
        for clas in clases:
            if "def" in clas:
                c = clas.split("def ")
                info = c[0].split("\n")
                nom = ""
                infodic = {}
                for i in info: # se extraen cada una de las lineas de los atributos
                    line = i.split(" = ")
                    if "models.Model" not in i and len(line) > 1: #se extraen cada uno de los parametros del modelo
                        name = line[0].replace(" ", "")

                        infodic[name] = line[1] #se agregan al diccionario cada uno de los parametros
                    elif "models.Model" in i:
                        nom = i.split("(")[0]

                cla[nom] = infodic # se agrega al diccionario de las clases del archivo
        #print(cla)
        n = file.split(".")[0]
        models[n]=cla # se agrega al diccionario de modelos
    return models

"""En esta se hace la comparacion de los modelos con los bloques html del archivo 
para saber que se esta llamando y en que linea"""
def comparacionBloques( modelos):
    path = "./calificador/dashboard/templates/dashboard/bloques" #Path donde esta la carpeta de los Bloques
    onlyfiles = [f for f in listdir(path) if
                 isfile(join(path, f))] #se extraen los archivos de lso bloques
    comparaciones = {}
    for file in onlyfiles: #se recorren todos los archivos en la carpeta bloques
        filepath = path + "/" + file
        f = open(filepath, "r")
        arch = "".join(f)
        lista = []
        for llave in modelos.keys():
            # print(modelos[llave].keys())
            clasificacion = []
            for l in modelos[llave].keys(): # Se revisan todos los modelos
                if l.lower() in arch and l != '': # se revisa si el modelo esta mencionado en el archivo
                    clasificacion.append(l.lower()) # se registran los modelos que aparecen en el archivo
            for i in clasificacion: #Se recorren los modelos que aparecen
                linea = 1
                for line in arch.split("\n"):
                    if i in line and "{" in line:
                        parts = line.split("}") #se extrae la linea donde se hace la mencion y se extraen las partes
                        for p in parts:
                            valor = ""
                            if "{" in p:
                                if p.count("{") > 1: #se extrae la informacion de la mencion
                                    valor = p.split("{")[2]
                                else:
                                    valor = p.split("{")[1]

                                nuevo = str(linea) + "_" + limpiarLinea(valor) #se agrega la informacion con el numeo de linea donde aparece
                                lista.append(nuevo)
                    linea += 1
        nombre = file.replace(".html","")
        comparaciones[nombre] = lista #se agrega la lista de menciones al diccionario de comparaciones
    return comparaciones

"""Esta funcion se utiliza para extraer parter que pueden estar incluidas
 dentro de la mencion que no se deben agregar a la lista como if, not url y include """
def limpiarLinea( linea):
    if "%" in linea:
        if "if" in linea:
            linea = linea.replace("% if", "")
            if "not" in linea:
                linea = linea.replace("not", "")
        elif "url" in linea:
            linea = linea.replace("% url", "")
        elif "include" in linea:
            linea = linea.replace("% include ","")
        linea = linea.replace("%","")
    return linea

"""Se reorganiza la informacion de forma que cada todas las menciones de un archivo queden juntas 
y que cada modelo tenga los archivos que los llaman """
def reorganizarinfo(modelos, resultados):
    grafo ={}
    for modelo in modelos.keys(): #se recorren todos los modelos
        name = modelo[0:len(modelo)-1]

        mod = []
        for result in resultados.keys(): #para cada archivo se extrae la informacion de que archivo y que nombres tienen
            lista = resultados[result]
            for i in lista:
                if name in i: # se revisa si el modelo aparece en la lista y en caso de que si se agrega la tupla con la informacion de la mencion y el nombre del archivo
                    mod.append((result,i))
        if len(mod)>0:
            grafo[modelo]=mod #se agrega al diccionario de resultados
    return grafo

"""Se genera el arbol para mostrar la informacion de una manera mas facil de entender"""
def generateTree(informacion):
    #print(informacion)
    tree = Tree() # se genera el arbol
    tree.create_node("calificador/dashboard/models", "raiz") # se genera la raiz
    for i in informacion.keys(): # se recorren las llaves del diccionario
        if tree.get_node(i) == None:
            tree.create_node(i, i, parent="raiz") # se agregan las llaves como hizos del nodo raiz
    for i in informacion.keys():
        lis = informacion[i]  # se extrae la lista de menciones del cada llave
        for j in lis:# se recorren la lista
            if tree.get_node(j[0]) == None: # se revisa si la el archivo (valor 0 en la tupla) ya existe en el arbol si no se agrega el nodo hijo
                tree.create_node(j[0], j[0], parent=i)
        for k in lis: # se vuelve a recorrer la lista
            if tree.get_node(k[1]) == None: # Se revisa que si la mencion (valor 1 en la tupla) ya existe en el nodo y si no se agrega al arbol con el archivo como padre
                tree.create_node(k[1], k[1], parent=k[0])
    tree.save2file("Modulos.txt") #se guarde el arbol en un archivo

    #print(tree.show())

"""Metodo que contiene todos los pasos del Caso 1
La funcion del caso 1 es generar una visualizacion de los llamados de los modelos de los diferentes archivos en la carpeta Bloques
De esta forma cuando se hagan modificaciones a los modelos o a la base de datos se pueda saber de manera rapida que lineas se de los
bloques fueron afectadas"""
def iniciarCaso1():
    modelos = obtenerArchivos()#se obtienen los modelos
    #print(modelos)
    resultado = comparacionBloques(modelos) # se obtienen las menciones
    #print( resultado)
    informacion = reorganizarinfo(modelos,resultado) # se reorganiza la informacion
    generateTree(informacion) # se genera el arbol

"""Se Ejecutan todos los pasos del Caso 1"""
iniciarCaso1()