from os import listdir
from os.path import isfile, join,isdir
from treelib import Node, Tree

"""Esta funcion obtiene las menciones de las imagenes """
def obtainfiles():
    path = "./calificador/dashboard/templates/dashboard"
    images = []
    allfiles = [f for f in listdir(path)] # se obtienen todos los archivos y directorios en el path

    for i in allfiles: #se recorren todos los directorios y archivos
        if isdir(path+"/"+i): #se chequea si es una carpeta o un archivo

            fileFiles =[f for f in listdir(path+"/"+i)] # se extraen los archivos de la carpeta
            for f in fileFiles:
                extrap = "/"+i+"/"+f
                filepath = path+extrap
                f = open(filepath, "r") # se obtiene  el texto del archivo
                arch = "".join(f)
                con = 1
                for line in arch.split("\n"): #se divide en las lineas del archivo
                    if "<img" in line: # Se revisa si se tiene imgen en la linea
                        nombre= extrap
                        images.append((nombre, "line:"+str(con)+" - "+line.strip())) #se agrega la tupla del archivo y la linea donde se tiene la imagen
                    con+=1
        elif isfile(join(path, i)):#en caso de ser archivo
            filepath = path + "/" + i
            f = open(filepath,"r")
            arch = "".join(f)# se obtiene el texto del archivo
            con = 1
            for line in arch.split("\n"): # se divide el archivo por lineas
                if "<img" in line:# se busca si tiene imagen la linea
                    nombre =i
                    images.append((nombre,"line:"+ str(con)+ " - "+line.strip()))# se agrega la tupla del archivo y la linea donde se hace el llamado a la imagen
                con+=1
    return images

"""Esta funcion genera el arbol de forma que se pueda visualizar de manera facil"""
def generatetree(lista):
    tree = Tree() # se genera el arbol
    tree.create_node("calificador/dashboard/templates/dashboard", "raiz") # se agrega la raiz  como el dashboard
    for i in lista:
        if tree.get_node(i[0])==None:# se revisa si el archivo  esta en el arbol y se arregla
            tree.create_node(i[0],i[0],parent="raiz") # se agrega el archivo al arbol
    for i in lista:
        if tree.get_node(i[1]) == None: # se revisa si la iimagen se ha agregado al arbol
            tree.create_node(i[1],i[1],parent=i[0]) # se agrega la imagen al arbol
    tree.save2file("imagenes.txt")

"""Metodo que contiene todos los pasos del Caso 2
La funcion del caso 2 es generar una visualizacion de los llamados de imagenes  de los diferentes archivos en la carpeta en las diferentes templates
De esta forma cuando se hagan modificaciones a las imagenes o se rompa una imagen se pueda saber de manera rapida que lineas  de las
 templates fueron afectadas"""
def iniciarCaso2():
    lista = obtainfiles()
    #print(lista)
    generatetree(lista)

iniciarCaso2()