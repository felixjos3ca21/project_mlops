<p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p>

# <h1 align=center> **PROYECTO INDIVIDUAL Nº1** </h1>

# <h1 align=center>**`Machine Learning Operations (MLOps)`**</h1>

<p align="center">
<img src="https://user-images.githubusercontent.com/67664604/217914153-1eb00e25-ac08-4dfa-aaf8-53c09038f082.png"  height=300>
</p>


**Contenido**

[TOCM]

[TOC]

#Contexto
##H2 header
###H3 header
####H4 header
#####H5 header
######H6 header


<hr>  

## **Descripción del problema (Contexto y rol a desarrollar)**

## Contexto

En este proyecto, nos encontramos frente a la emocionante tarea de llevar nuestro modelo de recomendación al mundo real. Después de lograr buenas métricas en su rendimiento, surge la pregunta: ¿cómo lo implementamos y mantenemos en producción?

El ciclo de vida de un proyecto de Machine Learning abarca desde la recopilación y procesamiento de los datos (tareas propias de un Ingeniero de Datos) hasta el entrenamiento y mantenimiento continuo del modelo de Machine Learning a medida que llegan nuevos datos.


## Rol a desarrollar

En mi rol como Data Scientist en esta startup, nos enfrentamos al desafío de brindar servicios de agregación de plataformas de streaming. Nuestro objetivo principal es desarrollar un sistema de recomendación basado en Machine Learning, el cual aún no ha sido implementado.

Al adentrarme en los datos existentes, me he dado cuenta de que su calidad es deficiente (o incluso inexistente). Los datos están desorganizados, sin transformar, y carecen de procesos automatizados para la actualización de nuevas películas o series, entre otros problemas. Esta situación dificulta enormemente mi trabajo como Data Scientist.

<hr>  


## ETL
# Propuesta de trabajo (requerimientos de aprobación)

**`Transformaciones`**:  Para este MVP no necesitas perfección, ¡necesitas rapidez! ⏩ Vas a hacer estas, ***y solo estas***, transformaciones a los datos:


+ Algunos campos, como **`belongs_to_collection`**, **`production_companies`** y otros (ver diccionario de datos) están anidados, esto es o bien tienen un diccionario o una lista como valores en cada fila, ¡deberán desanidarlos para poder  y unirlos al dataset de nuevo hacer alguna de las consultas de la API! O bien buscar la manera de acceder a esos datos sin desanidarlos.

+ Los valores nulos de los campos **`revenue`**, **`budget`** deben ser rellenados por el número **`0`**.
  
+ Los valores nulos del c
+ De haber fechas, deberán tener el formato **`AAAA-mm-dd`**, además deberán crear la columna **`release_year`** donde extraerán el año de la fecha de estreno.

+ Crear la columna con el retorno de inversión, llamada **`return`** con los campos **`revenue`** y **`budget`**, dividiendo estas dos últimas **`revenue / budget`**, cuando no hay datos disponibles para calcularlo, deberá tomar el valor **`0`**.

+ Eliminar las columnas que no serán utilizadas, **`video`**,**`imdb_id`**,**`adult`**,**`original_title`**,**`poster_path`** y **`homepage`**.

<hr>  

## **Implementacion de la API**
<br/>

**`Desarrollo API`**:   Propones disponibilizar los datos de la empresa usando el framework ***FastAPI***. Las consultas que propones son las siguientes:

Deben crear 6 funciones para los endpoints que se consumirán en la API, recuerden que deben tener un decorador por cada una (@app.get(‘/’)).
  
+ def **cantidad_filmaciones_mes( *`Mes`* )**:
    Se ingresa un mes en idioma Español. Debe devolver la cantidad de películas que fueron estrenadas en el mes consultado en la totalidad del dataset.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ejemplo de retorno: *`X` cantidad de películas fueron estrenadas en el mes de `X`*
         

+ def **cantidad_filmaciones_dia( *`Dia`* )**:
    Se ingresa un día en idioma Español. Debe devolver la cantidad de películas que fueron estrenadas en día consultado en la totalidad del dataset.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ejemplo de retorno: *`X` cantidad de películas fueron estrenadas en los días `X`*

+ def **score_titulo( *`titulo_de_la_filmación`* )**:
    Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score.
    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ejemplo de retorno: *La película `X` fue estrenada en el año `X` con un score/popularidad de `X`*

+ def **votos_titulo( *`titulo_de_la_filmación`* )**:
    Se ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor promedio de las votaciones. La misma variable deberá de contar con al menos 2000 valoraciones, caso contrario, debemos contar con un mensaje avisando que no cumple esta condición y que por ende, no se devuelve ningun valor.
    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ejemplo de retorno: *La película `X` fue estrenada en el año `X`. La misma cuenta con un total de `X` valoraciones, con un promedio de `X`*

+ def **get_actor( *`nombre_actor`* )**:
    Se ingresa el nombre de un actor que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. Además, la cantidad de películas que en las que ha participado y el promedio de retorno. **La definición no deberá considerar directores.**
    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ejemplo de retorno: *El actor `X` ha participado de `X` cantidad de filmaciones, el mismo ha conseguido un retorno de `X` con un promedio de `X` por filmación*

+ def **get_director( *`nombre_director`* )**:
    Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.



<br/>


**`Deployment`**: Conoces sobre Render 

<br/>
