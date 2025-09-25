#!/usr/bin/env

import json
from urllib.parse import urlparse


def ler_har(path):
    """Función que lee un path

    Args:
        path (string): O path do string

    Returns:
        list: Devolve unha lista de datos
    """
    
    with open(path, 'r', encoding='utf-8') as ficheiro:
        datos = json.load(ficheiro)
    return datos


def filtrar_json_entries(har_datos):
    """Función que se encarga de filtrar los mime "application/json"

    Args:
        har_datos (dict): Pasamoslle un diccionario cos datos

    Returns:
        list: Devólvese un array cos datos xa filtrados
    """
    
    if not(type(har_datos) is dict):
        raise ValueError
    
    # Lista donde guardamos el json
    json_entries = []
    
    # Recorremos cada entrada
    for entry in har_datos.get('log', {}).get('entries', []):
        # Accedemos a 'response' de forma segura (diccionario vacío si no existe)
        response = entry.get("response", {})
        # Accedemos a "content" de forma segura 
        content = response.get("content", {})
        # Accedemos a mimetype de forma segura, en caso de no estar devolvemos texto vacio 
        mime_type = content.get("mimeType", "")
        
        
        if mime_type == "application/json; charset=utf-8":
            json_entries.append({
                "url": entry.get('request', {}).get('url', ''),   # URL de la petición
                "status": response.get('status', ''),             # Código HTTP
                "content": content.get('text', '')               # Contenido JSON
            })

    return json_entries


def filtrar_dominios(har_datos):
    """Función que filtra os dominios dunha lista

    Args:
        har_datos (list): Lista de datos

    Raises:
        TypeError: Se o tipo non é o correcto

    Returns:
        list: Lista cos dominios
    """
    if not(type(har_datos) is list):
        raise TypeError
    
    # Inicializo a lista de dominio
    dominios = []
    # Recorremos a lista 
    for entry in har_datos:
        #Collemos cada url
        url = entry.get("url", "")
        #Compruebo que la url no esté vacía 
        if not url:
            continue
        
        #Compruebo que la url tenga un formato válido 
        parsed = urlparse(url)
        
        #Compruebo que forme parte el protoco de la url, 
        if not parsed.scheme or not parsed.hostname:
            continue
        #Extraemos el dominio y lso añadimos a la lista si no está repetido 
        dominio = parsed.hostname
        
        if dominio not in dominios:
            dominios.append(dominio)
            
    return dominios
        
def gardar_lista_en_ficheiro(path, lista):
    with open(path, 'w', encoding='utf-8') as ficheiro:
        for liña in lista:
            ficheiro.write(liña + '\n')
 

# Poñemos a ruta completa do ficheiro HAR
ruta = "datos.har"

# Cargamos los datos 
try:
    contido = ler_har(ruta)
    print("Ficheiro HAR cargado correctamente!")
    print("Claves principais do HAR:", contido.keys())

except Exception as e:
    print(f"Erro ao ler o ficheiro HAR: {e}")

#Collemos o json cos tipo mime application/json
lista_json = filtrar_json_entries(contido)

#Agora collemos de esa lista json os dominios
lista_dominios = filtrar_dominios(lista_json)

gardar_lista_en_ficheiro("dominios.txt", lista_dominios)