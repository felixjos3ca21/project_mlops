from fastapi import FastAPI
import pandas as pd
import math
import ast
import json
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

app = FastAPI()
#--------------------------------------------
@app.get("/")
def index():
    return {"Mensaje" : "Hola Mundo"}
#--------------------------------------------
    
#-----------------------------------------------------------------------------------------------------------------  
@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes:str):
    '''Se ingresa el mes y la funcion retorna la cantidad de peliculas que se estrenaron ese mes historicamente'''
    data = pd.read_csv('data_mes.csv')
    data["release_date"] = pd.to_datetime(data["release_date"])
    mes = mes.lower()
    # Verificar si el mes es válido
    meses_validos = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                     'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    if mes not in meses_validos:
        raise ValueError("El mes introducido no es válido.")
    # Filtrar las películas que fueron estrenadas en el mes dado
    peliculas_mes = data[data['release_date'].dt.month == meses_validos.index(mes) + 1]
    cantidad = peliculas_mes.shape[0]
    # Devolver la cantidad de películas del mes
    return {"cantidad" : cantidad , "mes": mes}

# ------------------------------------------------------------------------------------------------------------- 
@app.get('/cantidad_filmaciones_dia/{dia}')
def cantidad_filmaciones_dia(dia: str):
    '''Se ingresa el día y la función retorna la cantidad de películas que se estrenaron ese día históricamente'''
    data = pd.read_csv('data_dia.csv')
    data["release_date"] = pd.to_datetime(data["release_date"])
    # Convertir el día a minúsculas
    dia = dia.lower()
    # Corregir días "sábado" y "miércoles" alfabéticamente
    if dia == "sabado":
        dia = "sábado"
    elif dia == "miercoles":
        dia = "miércoles"
    # Verificar si el día es válido
    dias_validos = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
    if dia not in dias_validos:
        raise ValueError("El día introducido no es válido.")    
    # Filtrar las películas que fueron estrenadas en el día dado
    dia_numero = dias_validos.index(dia) + 1
    peliculas_dia = data[data['release_date'].dt.dayofweek + 1 == dia_numero]
    # Devolver la cantidad de películas del día
    cantidad_dia = peliculas_dia.shape[0]
    return {"cantidad": cantidad_dia, "dia": dia}

#-----------------------------------------------------------------------------------------------------------
@app.get('/score_titulo/{titulo}')
def score_titulo(titulo: str):
    '''Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score'''
    data = pd.read_csv('data_score.csv')
    # Tratamiento previo
    titulo = titulo.lower()
    data['release_year'] = pd.to_datetime(data['release_date']).dt.year
    data['popularity'] = data['popularity'].round(2) # Conversión a dos decimales
    
    # Filtrar el dataframe por título de película
    peliculas = data[data['title'].str.lower() == titulo]
    
    resultados = []
    for pelicula in peliculas.itertuples(index=False):
        # Obtener el título, año de estreno y puntaje de popularidad de cada película
        resultado = {
            'titulo': pelicula.title,
            'año_estreno': pelicula.release_year,
            'score': pelicula.popularity
        }
        resultados.append(resultado)
    
    return resultados

def print_resultados(resultados):
    if len(resultados) > 0:
        if len(resultados) == 1:
            print(resultados[0])
        else:
            for res in resultados:
                print(res)
    else:
        print("No se encontró la película en la base de datos.")
    return print_resultados(resultados)

#-------------------------------------------------------------------------------------------------------------------------------

@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo: str):
    '''Se ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor promedio de las votaciones. 
    La misma variable deberá de contar con al menos 2000 valoraciones, 
    caso contrario, debemos contar con un mensaje avisando que no cumple esta condición y que por ende, no se devuelve ningún valor.'''
    data = pd.read_csv('data_vote.csv')
    
    # Tratamiento previo
    titulo = titulo.lower()
    data['vote_count'] = data['vote_count'].astype(int)
    data['vote_average'] = data['vote_average'].round(2)  # Conversión a dos decimales
    data['release_year'] = pd.to_datetime(data['release_date']).dt.year
    
    # Filtrar el dataframe por título de película
    peliculas = data[data['title'].str.lower() == titulo]
    resultados = []
    
    if peliculas.empty:
        return {"mensaje": "No se encontró ninguna película con ese título."}
    
    for pelicula in peliculas.itertuples(index=False):
        if pelicula.vote_count > 2000:
            # Obtener el título, cantidad de votos y promedio de votos de cada película
            resultado = {
                'titulo': pelicula.title,
                'cantidad_de_votos': pelicula.vote_count,
                'promedio_de_votos': pelicula.vote_average
            }
            resultados.append(resultado)
        else:
            resultados.append({
                'titulo': pelicula.title,
                'mensaje': f"El título '{pelicula.title}' estrenada en el año '{pelicula.release_year}' no cuenta con más de 2000 votos para mostrar información."
            })
      
    return {"resultados": resultados}
#--------------------------------------------------------------------------------------------------------------------------------------
def convertir_a_dict(valor):
    datos_list = ast.literal_eval(valor)
    datos_str_list = [json.dumps(d) for d in datos_list]
    datos_dict_list = [json.loads(d) for d in datos_str_list]
    return datos_dict_list

@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor:str):
    '''Se ingresa el nombre de un actor que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
    Además, la cantidad de películas que en las que ha participado y el promedio de retorno'''
    data_actor = pd.read_csv('data_actor.csv')
    data_actor['name_actor'] = data_actor['name_actor'].apply(convertir_a_dict)
    data_actor['return'] = data_actor['return'].astype(float).round(2)
    
    actor_name = nombre_actor.lower().strip()
    filtro_actor = data_actor[data_actor['name_actor'].apply(lambda x: any(d['name'].lower().strip() == actor_name for d in x) if isinstance(x, list) else False)]
    cantidad_filmaciones = len(filtro_actor)
    retorno_total = filtro_actor['return'].sum()
    retorno_promedio = filtro_actor['return'].mean()

    if isinstance(retorno_promedio, str):
        retorno_promedio = float(retorno_promedio)
    
    if math.isinf(retorno_promedio):
        retorno_promedio = 'Infinity'

    retorno_total = round(retorno_total, 2)
    retorno_promedio = round(retorno_promedio, 2)
    response_data = {
        'actor': nombre_actor,
        'cantidad_filmaciones': cantidad_filmaciones,
        'retorno_total': retorno_total,
        'retorno_promedio': retorno_promedio
    }

    json_compatible_data = jsonable_encoder(response_data)

    return json_compatible_data   

#----------------------------------------------------------------------------------------------------------------------------------
@app.get('/get_director/{nombre_director}')
def get_director(nombre_director:str):
    ''' Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
    Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.'''
    data_director = pd.read_csv('data_director.csv')
    #Transformar la columna 'name_director' en una lista de diccionarios
    data_director['name_director'] = data_director['name_director'].apply(convertir_a_dict)
    nombre_director = nombre_director.lower().strip()
    filtro_director = data_director[data_director['name_director'].apply(lambda x: any(d['name'].lower().strip() == nombre_director for d in x) if isinstance(x, list) else False)]
    
    nombre_director = nombre_director
    retorno_total_director = filtro_director['return'].sum()
    
    peliculas = []
    for d, row in filtro_director.iterrows():
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
    
 #----------------------------------------------------------------------------------------------------------------------------------
    
    # ML
# Compilar la expresión regular fuera de la función
regex = re.compile(r'[^a-zA-Z]')
@app.get('/recomendacion/{titulo}')
def recomendacion(title:str):
    try:
        '''Ingresas un nombre de película y te recomienda las similares en una lista'''
        data_ml = pd.read_csv('data_ML.csv')
        # Compilar la expresión regular fuera de la función
        
        # Crear un objeto TfidfVectorizer para convertir el texto en vectores TF-IDF
        vectorizer = TfidfVectorizer(stop_words='english')
        # Aplicar el vectorizador a los datos de texto combinados y obtener la matriz de vectores TF-IDF
        vectorized_data = vectorizer.fit_transform(data_ml['combined_text'])
        
        # Crear y ajustar el modelo KNN fuera de la función
        knn_model = NearestNeighbors(metric='cosine', algorithm='brute')
        knn_model.fit(vectorized_data)
        
        
        # Preprocesamiento del título
        processed_title = re.sub(r'[^a-zA-Z]', ' ', title.lower())
        
        # Obtener índice de la película de consulta
        try:
            index = data_ml[data_ml['title'].str.lower() == processed_title].index[0]
        except IndexError:
            raise HTTPException(status_code=404, detail="Título de película no encontrado")
        
        # Numero de recomendaciones
        num_recomen = 5
        
        # Obtener recomendaciones basadas en el índice de consulta, menos el titulo que se ingresa
        _, indices = knn_model.kneighbors(vectorized_data[index], n_neighbors=num_recomen+1)
        
        # Obtener índices de las películas recomendadas
        index_title = indices.flatten()[1:]
        
        # Devolver una estructura de diccionario con los títulos recomendados
        result = {'lista recomendada': [title.title() for title in data_ml['title'].iloc[index_title].tolist()]}
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    
    
    
    
    
    
    
    
    
    
    
    
    