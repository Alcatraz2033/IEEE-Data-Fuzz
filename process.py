import json, signal, sys, os
from collections import Counter
from tabulate import tabulate

## controla la salida del programa
def crtl_c(sig, frame):
    print("\n\n[!] SALIENDO...")
    sys.exit(1)
signal.signal(signal.SIGINT, crtl_c)

# extrae los ieee terms y los author thers del json
def extract_terms_from_json(json_data):
    iee_terms = json_data.get("index_terms", {}).get("ieee_terms", {}).get("terms", [])
    author_terms = json_data.get("index_terms", {}).get("author_terms", {}).get("terms", [])
    return iee_terms, author_terms

## cuenta las palagras y las veces que se repiten
def count_terms(term_list):
    term_counter = Counter(term_list)
    return term_counter

## flujo principal del programa
def exec_tables_search():
    
    all_iee_terms = []
    all_author_terms = []
    table_ieee = []
    table_author = []
    col_ieee_names = ["IEEE-TERMS", "REPETICIONES"]
    col_author_names = ["AUTHOR-TERMS", "REPETICIONES"]


    files = os.listdir('jsonData')
    if not files:
        print("[!] No existen datos a cargar")
        sys.exit(1)

    for file in files:
        with open('jsonData/' + file, "r", encoding="utf-8") as file:
            data = json.load(file)
            articles = data.get("articles", [])

        for article in articles:
            iee_terms, author_terms = extract_terms_from_json(article)
            all_iee_terms.extend(iee_terms)
            all_author_terms.extend(author_terms)

        iee_terms_count = count_terms(all_iee_terms)
        author_terms_count = count_terms(all_author_terms)
    print("[+] Datos cargados exitosamente\n")

    #IEEE Terms y sus repeticiones
    for i, j in iee_terms_count.items():
        table_ieee.append([i, j])
        
    table_ieee.sort()
    # Author Terms y sus repeticiones
    for i, j in author_terms_count.items():
        table_author.append([i, j])
    table_author.sort()
    print("[1] Mostrar los IEEE-Terms")
    print("[2] Mostrar los Author-Terms")
    print("[3] Seleccionar las Key-Words para buscar los Titulos de las Obras\n")
    
    opt = str(input("ieee@fuzz:~$ "))
    if opt == '1':
        print(f'\n{tabulate(table_ieee, headers=col_ieee_names, tablefmt="fancy_grid", showindex=True)}')
    
    elif opt == '2':
        print(f'\n{tabulate(table_author, headers=col_author_names, tablefmt="fancy_grid", showindex=True)}')
    
    elif opt == '3':
        # Escojer datos para los ieee
        print(f'\n{tabulate(table_ieee, headers=col_ieee_names, tablefmt="fancy_grid", showindex=True)}')
        print("\n[+] Sleccione el numero de los terminos IEEE separados por comas, ejemplo: 1,4,7")
        
        data_ieee = []
        ieee_opt = str(input("ieee@fuzz:~$ ")).split(',')
        for i in ieee_opt:
            data_ieee.append(table_ieee[int(i)][0])
        ieee_related_titles = []

        for article in data["articles"]:
            ieee_terms_title = article.get("index_terms", {}).get("ieee_terms", {}).get("terms", [])
            title = article.get("title", "")
            
            for term in ieee_terms_title:
                if term in data_ieee and title not in ieee_related_titles:
                    ieee_related_titles.append(title)
            
        # Escojer datos para los author
        print(f'\n{tabulate(table_author, headers=col_author_names, tablefmt="fancy_grid", showindex=True)}')
        print("\n[+] Sleccione el numero de los terminos AUTHOR separados por comas, ejemplo: 1,4,7")
        
        data_author = []
        author_opt = str(input("ieee@fuzz:~$ ")).split(',')
        for i in author_opt:
            data_author.append(table_author[int(i)][0])
        author_related_titles = []
        
        for article in data["articles"]:
            author_terms_title = article.get("index_terms", {}).get("author_terms", {}).get("terms", [])
            title = article.get("title", "")
            
            for term in author_terms_title:
                if term in data_author and title not in author_related_titles:
                    author_related_titles.append(title)
        
        # Mostrar titulos
        # Titulos en base al ieee term                 
        print("\n[+] Títulos IEEE relacionados:")
        for idx, title in enumerate(ieee_related_titles, start=1):
            print(f"{idx}. {title}")
        
        # Titulos en base al author term
        print("\n[+] Títulos AUTHOR relacionados:")
        for idx, title in enumerate(author_related_titles, start=1):
            print(f"{idx}. {title}")

    else:
        print("[!] Opcion Incorresta")
        sys.exit(1)
