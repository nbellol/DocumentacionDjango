
from os import listdir
from os.path import isfile, join, isdir

"""Esta funcion agrega el nuevo el ccs a las templates que tiene el repositorio"""
def modificarTemplates():
    path = "./calificador/templates" # path
    no = "range.html,radio.html,martor.html,js.html,d3_pie.html,busqueda.html" #archivos que no se deben modificar
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))] # se extraen los archivos
    for file in onlyfiles: # se recorren los archivos
        print(file)
        if file not in no: # se revisa si el archivo se debe modificar
            if file == "base.html":
                filepath = path + '/' + file
                process_files_base(filepath)# se llama la funcion para modificar
            else:
                filepath = path + '/' + file
                process_files_comp(filepath)# se llama la funcion para modificar

"""funcion que modifica el archivo base.html"""
def process_files_base(filepath):
    f = open(filepath, "r", encoding="latin-1") # se abre el archivo
    arch = f.read() # se extrae el texto del archivo
    f.close()
    f = open(filepath, "w", encoding="latin-1") # se abre el archivo para modificar
    mesagge = """<style>
    .documentationtip {
      position: relative;
      display: inline-block;
      border-bottom: 1px dotted black;
    }

    .documentationtip .doctiptext {
      visibility: hidden;
      width: 120px;
      background-color: black;
      color: #fff;
      text-align: center;
      border-radius: 6px;
      padding: 5px 0;

      /* Position the tooltip */
      position: absolute;
      z-index: 1;
    }

    .documentationtip:hover .doctiptext {
      visibility: visible;
    }
    </style>"""
    parts = arch.split('<body class="Site">')
    final = parts[0] + '\n<body class="Site">\n' + mesagge + '\n' + parts[1] # se genera el mensaje a agregar
    f.write(final) # se reescribe el archivo
    f.close()

"""Funcion que modifica los demas archivos """
def process_files_comp(filepath):
    f = open(filepath, "r", encoding="latin-1")# se abre el archivo para leer
    arch = f.read() # se extrae la informacion
    f.close()
    f = open(filepath, "w", encoding="latin-1") # se abre el archivo a modificar
    message = filepath.split(".")[0].upper()+"\n"+filepath
    print(message)
    arriba = '<div class="documentationtip">\n  <span class="doctiptext">'+ message+ '</span>\n'
    abajo = '</div>'

    final =  arriba + '\n' + arch + '\n'+abajo # se construye el archivo con el nuevo css
    f.write(final)
    f.close()
"""Esta funcion modifica los archivos de los templates agregando el css"""
def modificar_comp():
    path = "./calificador/dashboard/templates/dashboard" # path para los demas archivos
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))] # se extraen los archivos
    onlydir = [f for f in listdir(path) if isdir(join(path, f))] # se extraen los directorios

    for file in onlyfiles: # se recorren los archivos
        pathfile = path+"/"+file
        process_files_comp(pathfile) # se llama el archivo para modificar
    for dir in onlydir: # se recorren los directivos
        npath= path+"/"+dir
        files = [f for f in listdir(npath) if isfile(join(npath, f))]  # se extraer  los archivos del directorio
        for file in files:
            pathfile=npath+'/'+file
            process_files_comp(pathfile) # se llama la funcion para modificar

"""Metodo que contiene todos los pasos del Caso 4
La funcion del caso 4 Modifica los archivos .html del repositorio de de forma que tengan el nuevo css que se genero de forma 
la funcionalidad de hover se agrege en frio a los html templates que tiene el repositorio. Mostrando que componenter estan
 ubicados en que archivos"""
def iniciarCaso4():
   modificarTemplates()
   modificar_comp()

# se ejecuta el caso 4
iniciarCaso4()
