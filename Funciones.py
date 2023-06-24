import pandas as pd
from datetime import datetime

# Creamos una función para validar errores en la columna 'id' y obtener los índices correspondientes
def validar_errores(df, columna):
    """
    Valida los errores en una columna específica de un DataFrame y devuelve los índices correspondientes.

    Argumentos:
        df (pandas.DataFrame): DataFrame que contiene los datos.
        columna (str): Nombre de la columna a validar.

    Returns:
        list: Lista de índices correspondientes a los valores erróneos en la columna.
    """
    indices_errores = []
    for i, valor in enumerate(df[columna]):
        try:
            int(valor)  # Intenta convertir a entero
        except ValueError:
            indices_errores.append(i)
    return indices_errores
# ---------------------------------------------------------------------------------------------
def null_a_cero(value):
    """
    Reemplaza un valor nulo por cero.

    Argumento:
        value: El valor a ser evaluado.

    Returns:
        El valor original si no es nulo, o cero si es nulo.
    """
    if pd.isnull(value):
        value = 0
    return value

#---------------------------------------------------------------------------------------------

def calcular_return(revenue, budget):
    """
    Calcula el retorno de inversión (ROI) en base a los ingresos y presupuesto.

    Argumentos:
        revenue (float): Los ingresos generados.
        budget (float): El presupuesto invertido.

    Returns:
        float: El retorno de inversión (ROI) calculado.

    Raises:
        None

    Examples:
        >>> calcular_return(100000, 50000)
        2.0
        >>> calcular_return(0, 10000)
        0.0
        >>> calcular_return(50000, 0)
        0.0
    """
    if pd.isnull(revenue) or pd.isnull(budget):
        return 0 
    elif budget == 0:
        return 0
    else:
        return revenue / budget
#-----------------------------------------------------------------------------------------------------------

