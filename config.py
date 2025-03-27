"""
Archivo de configuración para la consulta de la API EIA de petróleo.

Notas importantes sobre los parámetros:
- La frecuencia de consulta ('FREQUENCY') solo puede ser 'annual' según la documentación de la API.
- El año de inicio ('START_YEAR') puede ser desde 1984 en adelante.
- El año de fin ('END_YEAR') puede ser un valor numérico (ej: 2023) o None.
    * Si se deja como None, la API traerá la información disponible hasta el último año/momento cargado por la EIA.
"""

# URL base de la API de EIA para precios de petróleo crudo
BASE_URL = 'https://api.eia.gov/v2/petroleum/crd/pres/data/'

# Año de inicio de la consulta (1984 en adelante)
START_YEAR = 2000  # Cambiar a partir de 1984 según necesidad

# Año de fin de la consulta:
# - Puede ser un año específico (ej: 2023)
# - O None, para traer hasta el último año disponible en la API
END_YEAR = None

# Frecuencia de los datos:
# IMPORTANTE: La API solo acepta 'annual' para esta consulta
FREQUENCY = 'annual'

# Número máximo de registros a recuperar en la consulta
LENGTH = 10000

#Carpeta que simula el data lake 
FOLDER_DL = "DL"

#Archvio con la data cruda 
FILE_DL = 'crude_reserves_prod.csv'


#Carpeta que simula el datawarehouse 
FOLDER_DWH = "DWH"

#Archvio con la data cruda 
FILE_FACT = 'fact_crude_reserves_prod.csv'

FILE_DIM_AREA = "dim_area.csv"

FILE_DIM_PROCESS = "dim_process.csv"

FILE_DIM_PRODUCT= "dim_product.csv"

FILE_DIM_TIME="dim_time.csv"