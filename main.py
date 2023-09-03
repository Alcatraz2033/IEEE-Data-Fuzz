import api_request as apr
import urllib.parse, sys, os, signal, time
import process as ps


banner = """
·▄▄▄▄   ▄▄▄· ▄▄▄▄▄ ▄▄▄· ·▄▄▄▄• ▄▌·▄▄▄▄•·▄▄▄▄•
██▪ ██ ▐█ ▀█ •██  ▐█ ▀█ ▐▄▄·█▪██▌▪▀·.█▌▪▀·.█▌
▐█· ▐█▌▄█▀▀█  ▐█.▪▄█▀▀█ ██▪ █▌▐█▌▄█▀▀▀•▄█▀▀▀•
██. ██ ▐█ ▪▐▌ ▐█▌·▐█ ▪▐▌██▌.▐█▄█▌█▌▪▄█▀█▌▪▄█▀
▀▀▀▀▀•  ▀  ▀  ▀▀▀  ▀  ▀ ▀▀▀  ▀▀▀ ·▀▀▀ •·▀▀▀ • 1.0v
        Escuela Politecnica Nacional
"""
def crtl_c(sig, frame): # Controla la salida del programa al hacer ctrl + c
    print("\n\n[!] SALIENDO...")
    sys.exit(1)
signal.signal(signal.SIGINT, crtl_c)

def limpiar_terminal():
    # Verifica el sistema operativo para determinar el comando adecuado
    sistema_operativo = os.name
    if sistema_operativo == 'posix':  # Para sistemas Unix/Linux/Mac
        os.system('clear')
    elif sistema_operativo == 'nt':  # Para sistemas Windows
        os.system('cls')
        
def search_data():
    data = str(input("[+] Ingrese el dato a buscar: ")) # Guarda el input del usuario
    
    with open('last_search.txt', 'w+') as archivo:
        archivo.write(data)
    
    urlencode_query = urllib.parse.quote(data) # Pasa el texto en forma url encode
    apr.api_request(urlencode_query) # Comienza el proceso principal

def select(): # Esta funcion se encarga de proporcionar el menu al usuario para poder selccionar las opciones a utilizar
    try:
        with open('last_search.txt', 'r') as archivo: # Comprueba si se puede habrir el archivo last_search.txt lo que quiere decir que si hubo una busqueda anterior
            contenido = archivo.read()
        print("[$] Busqueda reciente: ", contenido) # Si hubo una busqueda anterior te la muestra
    except:
        print("[$] No hay Busquedas recientes") # Caso contrario muestra que no hubo busquedas recientes
        
    print("\n1) Mostrar Key-words de la busqueda mas reciente\n2) Buscar nuevos datos\n3) Borrar datos guardados")
    opt = str(input("\nieee@fuzz:~$ ")) # Entrada de tados por parte del usuario
    return opt
    
if __name__ == "__main__":
    limpiar_terminal()
    print(banner)
    opt = select() # Hace que el usuario realice la primera seleccion de opciones

    while True: # Bucle infinito para seleccionar multiples opciones
        if opt == '1': # Opcion 1 Mostrar keywords
            limpiar_terminal()
            print(banner)
            if not os.listdir('jsonData'):
                print("[!] No hay datos guardados\n")
                sys.exit(1)
            else:
                ps.exec_tables_search() # Llama a la funcion que muestra las keywords
                break
        
        elif opt == '2': # Busca nuevos datos
            for archivo in os.listdir('jsonData'):
                ruta_archivo = os.path.join('jsonData', archivo)
                if os.path.isfile(ruta_archivo):
                    try:
                        os.remove(ruta_archivo) # Elimina cualquier dato de busquedas anteriores para que no afecten a las nuevas
                    except:
                        pass
                    
            limpiar_terminal()
            print(banner)
            search_data()
            time.sleep(1)
            limpiar_terminal()
            print(banner)  
            opt = select() # Muestra nuevamente al usuario el menu principal
            
        elif opt == '3': # Elimina cualquier busqueda previa guardada
            limpiar_terminal()
            print(banner)
            
            try:
                os.remove('last_search.txt')
            except:
                pass
            
            for archivo in os.listdir('jsonData'):
                ruta_archivo = os.path.join('jsonData', archivo)
                if os.path.isfile(ruta_archivo):
                    try:
                        os.remove(ruta_archivo) # Elimina los datos guardados de anteriores busquedas
                    except:
                        pass
                    
            print("[+] Se eliminarion los datos de busqueda guardados\n")
            time.sleep(1.5)
            
            limpiar_terminal()
            print(banner)  
            opt = select()
            
        else: # En caso de que el dato introcuciono no corresponda con ninguno de los dispinibles en el menu principal
            limpiar_terminal()
            print(banner)
            print("[!] Opcion incorrecta\n")
            sys.exit(1)