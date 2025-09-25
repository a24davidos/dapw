import json

"""
Función que lee un ficheiro HAR
"""
def ler_har(path):
    with open(path, 'r', encoding='utf-8') as ficheiro:
        datos = json.load(ficheiro)
    return datos


if __name__ == "__main__":
    # Poñemos a ruta completa do ficheiro HAR
    ruta = "ficheiro.har"
    
    try:
        contido = ler_har(ruta)
        print("Ficheiro HAR cargado correctamente!")
        print("Claves principais do HAR:", contido.keys())
    except Exception as e:
        print(f"Erro ao ler o ficheiro HAR: {e}")
