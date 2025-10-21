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
        
        # 1 - primero obtenemos informacion del evento s3
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = unquote_plus(event['Records'][0]['s3']['object']['key']) # usamos unquote_plus para decodificar el nombre del archivo

        print(f"Procesando archivo: {object_key} desde el bucket: {bucket_name}")

        # obtenemos metadata del archivo
        # con get_object obtenemos el objeto completo del archivo en S3 dando el nombre del bucket y el nombre del archivo
        # devuelve datos como: `Body` (formato stream), `LastModified`, `ContentType`, `ContentLength`, `Metadata`, etc en formato de diccionario.
        s3_object = s3_client.get_object(Bucket=bucket_name, Key=object_key)


        # 2 - Procesamos con Textract
        print("Iniciando analisis con Textract...")
        textract_response = textract_client.detect_document_text( # esto extrae todo el texto del documento.
            Document = {
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': object_key
                } # de esta forma leemos desde S3 el archivo pasandole el nombre del bucket y el nombre del archivo.
            }
        )

        # 3 - Extraer el texto del documento
        texto_extraido = "" # iniciamos una cadena de texto vacia para guardar el texto extraido.
        for item in textract_response['Blocks']: # iteramos sobre los bloques de texto extraido. Cada item es un diccionario con el texto extraido.
            if item['BlockType'] == 'LINE': # si el bloque es de tipo linea, agregamos el texto a la cadena.
                texto_extraido += item['Text'] + " " # agregamos el texto a la cadena.
        print(f"Texto extraido: {texto_extraido[:200]}...") # mostramos el texto extraido (primeros 200 caracteres).

        # 4 - creamos el registro para DynamoDB
        table = dynamodb.Table(DYNAMODB_TABLE)
        invoice_id = object_key.split('/')[-1] # usamos el nombre de archivo como ID de la factura.
    
    
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