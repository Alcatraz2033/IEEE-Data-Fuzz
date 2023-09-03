import requests, json, sys, signal
from IEEapi import api_key

## variables globales
url = "http://ieeexploreapi.ieee.org"

# controla la salida del programa
def ctrl_c(sig, frame):
    print("\n[!] Saliendo...")
    sys.exit(1)
signal.signal(signal.SIGINT, ctrl_c)

# esta funcion se encarga de hacer la peticion al ieee
def make_request(pi_key, pre_value_range, end_value_range, meta_data):
    r = requests.get(url + f"/api/v1/search/articles?apikey={api_key}&format=json&max_records={end_value_range}&start_record={pre_value_range}&sort_order=desc&sort_field=article_number&meta_data={meta_data}")

    try:
        data_json = json.loads(r.text) ## lee el output en json
        return data_json
    
    except: ## en caso de que no lo pueda leer quiere decir que nos han baneado y salta al error
        print("[!] DEMASIADAS PETICIONES EN UN TIEMPO TAN CORTO, SERVICIO DENEGADO, ESPERE UNOS MINUTOS MIENTRAS SE LE OTORGA ACCESO NUEVAMENTE")
        sys.exit(0)

# checha si el resultado de la busqueda tiene mas de 200 papers o no
def check_value(meta_data):
    data_json = make_request(api_key, 1, 1, meta_data) # primero hace la busqueda un paper ya que ahi se encuentra el mazimo de papers
        
    total_json_data = int(data_json['total_records'])
    print(f"[+] Total records: {total_json_data}") # imprime el numero total de papers para esa busqueda
    
    if total_json_data <= 200:
        return total_json_data, 0 # si es menor igual a 200 devuelve esos datos

    elif total_json_data > 200:
        return int(total_json_data / 200), total_json_data%200 # si es mayor a 200 devuelve el numero de tandas de 200 necesarios para abarcar todo mas el sobrante
    
# realiza el munero de peticiones web necesarios para abarcar todos los papaers de la busqueda haciendo uso de las otras funciones
def api_request(meta_data):
    n_rep, excess = check_value(meta_data) # almacena las tandas y el sobrante
    pre_value_range = 0
    end_value_range = 1
    counter = 0
    
    if excess == 0:
        print(f"[+] En total seran necesario 1 archivos para abarcar todos los papers.\n")
        data_json = make_request(api_key, 0, n_rep, meta_data) # hace una sola peticion ya que son menos de 200 papers
        with open(f"jsonData/Archivo_{counter +1}.json", 'w+') as archivo:
                json.dump(data_json, archivo) # guarda el contenido en un archivo json
        print(f"[>] Archivo {counter + 1} escrito") # imprime el nombre del archivo escrito  
    
    else:
        print(f"[+] En total seran necesarios {n_rep + 1} archivos para abarcar todos los papers.\n")
        for i in range(n_rep):
            pre_value_range = end_value_range
            end_value_range += 200
            counter += 1
            # print(pre_value_range, end_value_range)
            
            data_json = make_request(api_key, pre_value_range, end_value_range, meta_data) # hace la peticion en el rango espesificado
            with open(f"jsonData/Archivo_{counter}.json", 'w+') as archivo:
                    json.dump(data_json, archivo) # guarda el contenido en un archivo json
            print(f"[>] Archivo {counter} escrito")                 
    
        pre_value_range = end_value_range
        end_value_range += (excess - 1)
        # print(pre_value_range, end_value_range)
        
        data_json = make_request(api_key, pre_value_range, end_value_range, meta_data) # hace la peticion sobrante
        with open(f"jsonData/Archivo_{counter + 1}.json", 'w+') as archivo:
            json.dump(data_json, archivo) # guarda el contenido en un archivo json
        print(f"[>] Archivo {counter + 1} escrito")
