import pandas as pd
import ast
import json

data_director = pd.read_csv('C:\project_mlops\datasets\data_director.csv')

def convertir_a_dict(valor):
    datos_list = ast.literal_eval(valor)
    datos_str_list = [json.dumps(d) for d in datos_list]
    datos_dict_list = [json.loads(d) for d in datos_str_list]
    return datos_dict_list

# Transformar la columna 'name_director' en una lista de diccionarios
data_director['name_director'] = data_director['name_director'].apply(convertir_a_dict)

def director_info(director_name: str):
    director_name = director_name.lower().strip()
    filtro_director = data_director[data_director['name_director'].apply(lambda x: any(d['name'].lower().strip() == director_name for d in x) if isinstance(x, list) else False)]
    
    nombre_director = director_name
    retorno_total_director = filtro_director['return'].sum()
    
    peliculas = []
    for _, row in filtro_director.iterrows():
        pelicula = {
            'titulo': row['title'],
            'anio': row['release_date'],
            'retorno_pelicula': row['return'],
            'budget_pelicula': row['budget'],
            'revenue_pelicula': row['revenue']
        }
        peliculas.append(pelicula)

    return {
        'director': nombre_director,
        'retorno_total_director': retorno_total_director,
        'peliculas': peliculas
    }

director_name = input("Ingrese el nombre del director: ")
result = director_info(director_name)
print(result)