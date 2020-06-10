from os import listdir
from os.path import isfile, join, isdir

"""
Se agrega estas lineas en el archivo setting.py de forma que se pueda activar y desactivar
la visualizacion

HOVER_TAG = True
HOVER_TEMPLATE = 'calificador.templatetags.custom_tag'
if not HOVER_TAG:
    HOVER_TEMPLATE= 'calificador.templatetags.custom_tag2'
print(HOVER_TEMPLATE)

Se agrega esta informacion en la Seccion de Templates del archivo settings.py
'libraries':{
                'custom_tag': 'calificador.templatetags.custom_tag',

            }
Se agrega la carpeta Templatetags con el archivo custom_tag.py y un archivo __init__.py"""

"""Esta funcion agrega el nuevo tag a las templates que tiene el repositorio"""
def modificarTemplates():
    path = "./calificador/templates" # path de las templates
    no = "range.html,radio.html,martor.html,js.html,d3_pie.html,busqueda.html" #archivos que no deben ser modificados
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))] #se extraen los archivos que estan en el directorio
    n = 0
    for file in onlyfiles: # se recorren los archivos
        print(file)
        if file not in no: # se revisa si el archivo se va a modificar
            if file == "base.html": # si el archivo es el base se modifica diferente
                filepath = path + '/' + file
                process_files_base(filepath)# se llama la funcion para modificar
            else:
                filepath = path + '/' + file
                process_files_comp(filepath,n) # se llama la funcion para modificar el archivo
                n+=1
    return n

"""funcion que modifica el archivo base.html"""
def process_files_base(filepath):
    f = open(filepath, "r", encoding="latin-1") # se lee el archivo
    arch = f.read() # se extrae el archivo
    f.close()
    f = open(filepath, "w",encoding="latin-1") # se abre el archivo para modificar
    mesagge = ""
    parts = arch.split('<body class="Site">')
    final = parts[0] + '\n<body class="Site">\n' + mesagge + '\n' + parts[1]# se agregan las partes
    f.write(final) # se escriben los cambios
    f.close()

"""Funcion que modifica los demas archivos """
def process_files_comp(filepath,n):
    f = open(filepath, "r", encoding="latin-1") # se abre el archivo para leer
    arch = f.read() # se extrae toda la informacion del archivo
    f.close()
    f = open(filepath, "w",encoding="latin-1") # se abre el archivo para modificar
    name = filepath.split("/")
    message = name[len(name)-1].upper()# se optiene parte del mensage
    final = ""
    if '{% extends "base.html" %}' in arch: # se revisa que tags tiene el archivo
       print("caso1")
       parts = arch.split('{% extends "base.html" %}')# se obtiene  las partes del archivo
       s = '{% extends "base.html" %}\n{% load custom_tag %} \n  {% hover ' + message + ' %}\n'
       a = '\n {% endhover %}' # se agregan las nuevas tags
       final = s + parts[1] + a #se arma el mesage final

    elif '{% load humanize %}' in arch: #se revisa que tags tiene el archivo
        print("caso2")
        parts = arch.split('{% load humanize %}') # se obtienen las partes del archivo

        s = '{% load custom_tag %}\n {% load humanize %}\n  {% hover ' + message + ' %}\n'
        a = '\n {% endhover %}' # se agrega el nuevo tag
        final = s + parts[1] + a # se genera el nuevo archivo
    else:
        print("caso3")
        s = '{% load custom_tag %}\n {% hover '+message+' %}\n' # se genera el  nuevo tag
        a = '\n {% endhover %}'
        final = s+arch+a # se genera el nuevo archivo

    f.write(final) # se escribe el archivo otra ves
    f.close()
"""Esta funcion modifica los archivos de los templates agregando los nuevos tags """
def modificar_comp(n):
    path = "./calificador/dashboard/templates/dashboard" # el path para los arhcivos
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))] # se obtienen los archivos en el path
    onlydir = [f for f in listdir(path) if isdir(join(path, f))] # se obtienen los directorios en el path
    x=n
    for file in onlyfiles:# se recorren los archivos
        print(file)
        pathfile = path+"/"+file
        process_files_comp(pathfile,x) # se llama la funcion para agregar el tag al archivo
        x+=1
    for dir in onlydir: # se recorren los directorios
        npath= path+"/"+dir
        files = [f for f in listdir(npath) if isfile(join(npath, f))] # se extraen los archiovs
        for file in files:

            pathfile=npath+'/'+file
            print(pathfile)
            process_files_comp(pathfile,x) # se llama la funcion para agregar el tag al archivo
            x+=1
"""Metodo que contiene todos los pasos del Caso 4
La funcion del caso 4 Modifica los archivos .html del repositorio de de forma que tengan el nuevo tag que se genero de forma 
la funcionalidad de hover se agrege en caliente a los html templates que tiene el repositorio. Mostrando que componenter estan
 ubicados en que archivos"""
def iniciarCaso4():
   cant = modificarTemplates() # se llama para modificar los archivos en la carpeta template
   modificar_comp(cant) # se llama para modificar los archivos dentro de dashboard templates

#se ejecuta el caso 4
iniciarCaso4()
