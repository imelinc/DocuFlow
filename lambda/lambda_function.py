import json # para manejas datos en formato JSON
import boto3 # biblioteca oficial de AWS que permite interactual con los servicios
import os # biblioteca para interactuar con el sistema operativo
from datetime import datetime # biblioteca para manejar fechas y horas
from urllib.parse import unquote_plus # biblioteca para decodificar URLs ("+", "%20", etc.)