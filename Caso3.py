import time
from selenium import webdriver
import networkx as nx
from graphviz import Digraph
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/graphviz-2.38/release/bin'

"""Esta funcion obtiene los urls que se esta registrados en el archivo urls"""
def obtainurls():
    path= "./calificador/dashboard/urls.py" #Path al archivo de los URLs
    urls =[]
    f = open(path, "r", encoding="utf-8") # se abre el archivo
    arch = "".join(f) # se obtiene el texto del archivo
    u = arch.split("[")[1].split("]")[0] #se obtiene la parte de los urls
    for line in u.split(",\n"): #se recorre linea por linea
        if line !="": #se revisa que la linea no este vacia
            path = line.split("(")[1].split(")")[0] #se limpia el url
            url = path.split(",")[0]
            urls.append(url)  # se agrega el url a la lista
    return urls

"""Esta funcion recorre las paginas con el web driver"""
def extract_links (driver, links):
    current = driver.current_url # se obtiene el url actual
    mybytes = driver.page_source # se obtiene el codigo html de la pagina
    problemas=[]
    est=[]
    envios=[]
    for line in mybytes.split('\n'): # se recorre el archivo por cada una de las lineas
        if "href" in line: # se buscan las referencias  de navegacion
            link = line.split('href="')[1].split('"')[0] #se extrae el url
            if "/" in link and "static" not in link  and link not in current : # se revisa que no sea referencia a imagenes
                if "/envios_" not in link: # se revisa si link es para envios
                    if link.count("/") <= 3 and "tag" not in link:
                        if "/problemas/" in link: # se revisa que  si el link es para problemas
                            problemas.append(link)
                        elif "/estudiante/analisis" in link: # se revisa si el link es para analisis de estudiantes
                            est.append(link)
                        elif "/envios/" in link: # se revisa si es para enviar
                            envios.append(link)

                        else:
                            if links.get(link) == None:
                                    links[link] = 1# se agrega el link
                            else:
                                links[link] += 1 # en caso de que se use mas de una vez se cuentan
    if len(problemas)!= 0:
        links[problemas[0]]=len(problemas) # Se agrega solo un problema
    if len(est) != 0:
        links[est[0]]=len(est) # se agrega solo un student analisis
    if len(envios) != 0:
            links[envios[0]] = len(envios) # se agrega un solo url de envios
    return links # se retornan todos los links

"""Se navegan los links  con el webdriver"""
def obtainlinks ():
    url = "https://senecode.virtual.uniandes.edu.co" # El url inicial
    driver = webdriver.Chrome(
        'C:/Users/Nicolás Bello/Documents/Andes/TESIS/chromedriver')  #se inicializa el webdrivre
    driver.get(url + "/home")
    time.sleep(5)  # Let the user actually see something!
    search_box = driver.find_element_by_name('usuario') # se ingresa el usuario
    search_box.send_keys('n.bello')
    search_box = driver.find_element_by_name('password') # se ingrea la contrasenha
    search_box.send_keys('nbellol1203')
    search_box.submit() #se ingresa a senecode
    time.sleep(5)

    extrac = {}
    extracted = extract_links(driver, extrac) # Se extraen los links de la primera pagina
    endlist = []
    for link in extracted: # se checkan los primero links extraidos

        if 'http' not in link: # se revisa si el link es una url externa
            endlist.append(("/home", link)) # se agrega a la lista final
    for link in extracted: # se recorre la list de links
        l = {}
        driver.get(url + link) # se navega a esa pagina
        l = extract_links(driver, l) # se extraen los urls de esa pagina
        for a in l:
            if 'http' not in a:
                endlist.append((link, a)) # se agrega a la la tupla lista final
    return endlist

"""Se construye el grafo"""
def generategraph(links):
    g = nx.Graph() # se inicializa el grafo
    for link in links:
        g.add_edge(link[0],link[1]) # se agregan las conecciones del grafo
    generateRender(g, "") # se genera el archivo con el grafo
    return g
"""Se genera en el grafo para generar el archivo"""
def generateRender(grafo,s):
    dot = Digraph(comment='Clicks') # se inicializa el grapho
    for node in grafo.nodes():# se recorren los nodos del grafo
        dot.node(node, node)# se agregan los nodos en el grafo render
    for edge in grafo.edges(): # se recorren las conecciones del grafo
        dot.edge(edge[0], edge[1]) # se agregan los edges al grafo render
    dot.render('niveles'+s+'.gv', view=True) # se genera el archivo del grafo

"""Metodo que contiene todos los pasos del Caso 3
La funcion del caso 3 es generar una visualizacion de la navegabilidad de la aplicacion. Se muestran todos los links a los que 
el usuario puede navegar dentro de la aplicacion. Esto nos permite ver que paginas se visitan mas y que paginas o urls no son accesibles
para los usuario"""
def iniciarCaso3():
    urls = obtainurls() # se obtiene los urls
    links = obtainlinks() # se obtiene los links navegables
    g = generategraph(links) # se genera el grafo
    notGraf =[] #Se genera una lista para los urls que no se navegan
    graf=[]
    for u in urls: # se recorren los urls
        if "<" in u: # se limpian los urls
            new = u.split("<")[0].replace("'","")
        else:
            new = u.replace("'","")

        for n in g.nodes():
            #print(new,n)
            if new in n and u !="''": # se agregan los urls que estan en el grafo
                graf.append(u)
    #print(len(graf))
    for u in urls: # se recorren los urls
        if u not in graf:
            notGraf.append(u) # se agregan los urls que no estan en el grafo
    notGraf.remove("''")
    notGraf.remove("'login/'")
    notGraf.remove("'home/'")
    f = open("UrlsFaltantes.txt", "w+") # se genera un archivo para escribir los urls faltantes
    f.write("Los "+str(len(notGraf)) +" urls que no se encuentran en la navegacion son:\n") # se escribe la primera linea
    for i in notGraf:
        f.write(i+"\n") #se escribe el url en la line
    f.close()

# se ejecuta el caso 3
iniciarCaso3()