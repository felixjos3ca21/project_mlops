from fastapi import FastAPI
import pandas as pd


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
    data = pd.read_csv('C:\project_mlops\datasets\data_endpoints.csv')
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
@app.get('/cantidad_filmaciones_dia{dia}')
def cantidad_filmaciones_dia(dia: str):
    '''Se ingresa el día y la función retorna la cantidad de películas que se estrenaron ese día históricamente'''
    data = pd.read_csv('C:\project_mlops\datasets\data_endpoints.csv')
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
    data = pd.read_csv('C:\project_mlops\datasets\data_endpoints.csv')
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
    data = pd.read_csv('C:\project_mlops\datasets\data_endpoints.csv')
    
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
@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor:str):
    '''Se ingresa el nombre de un actor que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
    Además, la cantidad de películas que en las que ha participado y el promedio de retorno'''
    
    
    return {'actor':nombre_actor, 'cantidad_filmaciones':respuesta, 'retorno_total':respuesta, 'retorno_promedio':respuesta}