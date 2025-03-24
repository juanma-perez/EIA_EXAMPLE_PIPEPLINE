import requests
import json
from pyspark.sql import DataFrame, SparkSession

class EIAApiClient:
    """
    Cliente para consumir la API de la U.S. Energy Information Administration (EIA)
    y cargar los resultados directamente en un DataFrame de Spark.

    Atributos:
        api_key (str): Clave de acceso a la API de EIA.
        spark (SparkSession): Sesión activa de Spark.
        base_url (str): URL base de la API que se va a consumir.
    """

    def __init__(self, api_key: str, spark_session: SparkSession, base_url: str):
        """
        Inicializa el cliente con la API Key, la sesión de Spark y la URL de la API.

        Args:
            api_key (str): Clave de autenticación para la API de EIA.
            spark_session (SparkSession): Objeto SparkSession activo.
            base_url (str): URL base de la API que se va a consumir.
        """
        self.api_key = api_key
        self.spark = spark_session
        self.base_url = base_url

    def fetch_data_as_spark_df(self, start_year=2000, end_year=None, frequency='annual', length=5000) -> DataFrame:
        """
        Realiza la solicitud a la API de EIA y retorna los datos como un DataFrame de Spark.

        Args:
            start_year (int, opcional): Año de inicio de la consulta. Por defecto es 2000.
            end_year (int, opcional): Año de fin de la consulta. Por defecto es None (hasta el más reciente).
            frequency (str, opcional): Frecuencia de los datos ('annual', 'monthly', etc.). Por defecto 'annual'.
            length (int, opcional): Número máximo de registros a recuperar. Por defecto 5000.

        Returns:
            DataFrame: DataFrame de Spark con los datos obtenidos de la API.

        Raises:
            Exception: Si la API devuelve un error o si la respuesta no contiene datos.
        """
        x_params = {
            "frequency": frequency,
            "data": ["value"],
            "facets": {},
            "start": str(start_year),
            "end": end_year,
            "sort": [{"column": "period", "direction": "desc"}],
            "offset": 0,
            "length": length
        }

        headers = {
            'Content-Type': 'application/json',
            'X-Params': json.dumps(x_params),
            'X-Api-Key': self.api_key
        }

        response = requests.get(self.base_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            records = data.get('response', {}).get('data', [])
            if not records:
                raise Exception("La respuesta no contiene datos.")
            return self.spark.createDataFrame(records)
        else:
            raise Exception(f"API Error {response.status_code}: {response.text}")
