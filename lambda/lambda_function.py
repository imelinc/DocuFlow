import json # para manejas datos en formato JSON
import boto3 # biblioteca oficial de AWS que permite interactual con los servicios
import os # biblioteca para interactuar con el sistema operativo
from datetime import datetime # biblioteca para manejar fechas y horas
from urllib.parse import unquote_plus # biblioteca para decodificar URLs ("+", "%20", etc.)

# Vamos a crear las conexiones con los servicios de AWS que vamos a utilizar

"""
boto3.client(s3): es un objeto que permite interactuar con el servicio S3 (Simple Storage Service) de AWS.
boto3.client(textract): es un objeto que permite interactuar con el servicio Textract de AWS.
boto3.resource(dynamodb): es un recurso que permite interactuar con el servicio DynamoDB de AWS, 
se utiliza resource ya que es mas intuitivo trabajar con esto para las tablas.
"""
s3_client = boto3.client('s3') 
textract_client = boto3.client('textract')
dynamodb = boto3.resource('dynamodb')

# VARIABLE DE ENTORNO
DYNAMODB_TABLE = os.environ.get('DYNAMODB_TABLE') # os.environ.get() lee las variables de entorno 

def lambda_handler(event, context):
    """
    Funcion principal que se ejecuta cuando llega un archivo a S3.
    event: diccionario JSON que contiene la informacion del disparo de la funcion, en este caso, 
    informacion sobre el archivos que se subio a S3.
    context: objeto que contiene informacion sobre el contexto de la funcion, como el tiempo de ejecucion, 
    el entorno, etc.
    """
    try:
        # Logica de procesamiento del archivo
        pass
    except Exception as e:
        # Capturamos cualquier error que ocurra
        print(f"Error procesando la factura: {str(e)}")
        return {
            'statusCode': 500, # codigo HTTP de error
            'body': json.dumps({ # cuerpo de la respuesta en formato JSON
                'message': f'Error procesando la factura: {str(e)}',
                'error': str(e)
            })
        }