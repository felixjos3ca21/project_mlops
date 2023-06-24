"""
ETL
"""
    
import pandas as pd
import numpy as np
from datetime import datetime
import Funciones

#---------------------------------------------------------------------------------------------------------

movies = pd.read_csv('movies_dataset.csv')

#--------------------------------------------------------------------------------------------------------

"""
Eliminamos las columnas que no vamos a necesitar 

"""
columnas = ['video','imdb_id', 'adult','original_title','poster_path','homepage']

movies.drop(columnas, axis= 1, inplace=True)
#---------------------------------------------------------------------------------------------------------
"""
Identificamos errores en la columna 'id' y las eliminamos 
al observar que las filas no contienen información relevante para el dataset se procede a eliminar 
Eliminar las filas con los índices identificados
"""
indices_errores = Funciones.validar_errores(movies, 'id')

movies.drop(indices_errores, inplace=True)

# Reiniciar los índices
movies.reset_index(drop=True, inplace=True)

#--------------------------------------------------------------------------------------------------------

# Procedemos a la transformación de la columna 'id'
movies['id'] = movies['id'].astype(int)
"""
se consultaron 5 Ids al ver que contienen la misma información se procede a eliminar estos duplicados
como criterio de eliminación se tomo la columna popularity que en ocasiones se diferencian
#Antes debemos convertir los valores de la columna "popularity" a tipo numérico
"""
movies['popularity'] = pd.to_numeric(movies['popularity'], errors='coerce')

# Eliminar filas duplicadas basadas en la columna "popularity"
movies = movies.sort_values('popularity', ascending=False)  # Ordenar por "popularity" de forma descendente
movies.drop_duplicates(subset='id', keep='first', inplace=True)  # Mantener la primera ocurrencia de cada "id"

# Reiniciar los índices
movies.reset_index(drop=True, inplace=True)
# -----------------------------------------------------------------------------------------------------
"""
Los valores null o Nan del las columnas Budget y revenue
Estos valores serán reemplazados al valor neutro 0.
"""

movies['budget'] = movies['budget'].apply(Funciones.null_a_cero)
movies['revenue'] = movies['revenue'].apply(Funciones.null_a_cero)
#----------------------------------------------------------------------------------------------------
"""
Una vez explorados las fila que contienen estos datos Nan en la columna 'release_date' y  tomando en cuanta la 
premisa de eliminar los valores null, de esa columna.
como la finalidad de la API es que no brinde cierta información de la columna se decidió eliminar las filas 
donde el campo 'release_date' es null
"""
movies.dropna(subset=['release_date'], inplace=True)
movies.reset_index(drop=True, inplace=True)

#-----------------------------------------------------------------------------------------------------

# se transforman los datos de la columna release_dato al formato AAAA-MM-DD

movies['release_date'] = pd.to_datetime(movies['release_date'], format='%Y-%m-%d')

#-----------------------------------------------------------------------------------------------------
"""
Creación de la columna "release_year"
"""
movies["release_year"] = pd.to_datetime(movies["release_date"], format="%Y")

#-----------------------------------------------------------------------------------------------------
""" 
Creación de la columna return que refleja, el calculo del retorno de inversión (ROI) en base a los ingresos y presupuesto.
"""
#Aseguramos que ambas columnas tenga el mismo tipo de datos 
movies['budget'] = movies['budget'].astype(float)
movies['revenue'] = movies['revenue'].astype(float)

movies['return'] = movies.apply(lambda row: Funciones.calcular_return(row['revenue'], row['budget']), axis=1)

#-----------------------------------------------------------------------------------------------------

credits = pd.read_csv('credits.csv')

#------------------------------------------------------
# Una vez verificado la duplicidad de las filas, procedemos a eliminarlas
credits.drop_duplicates(subset='id', keep='first', inplace=True)  # Mantener la primera ocurrencia de cada "id"

# Reiniciar los índices
credits.reset_index(drop=True, inplace=True)

#---------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------
print(movies.info())
print(credits.info())