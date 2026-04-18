import os
import pandas as pd
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from sqlalchemy import create_engine

# Conexión a la base de datos de Postgres
DB_CONN = "postgresql+psycopg2://postgres:postgres@postgres/donas_db"

# Ruta dentro del contenedor de Airflow donde estará el archivo
# Al usar en docker-compose, mapeamos ../data a /opt/airflow/data
CSV_FILE_PATH = "/opt/airflow/data/historial_ventas.csv"

def get_db_engine():
    return create_engine(DB_CONN)

def extract_and_load_data():
    """
    Lee datos del CSV histórico usando Pandas, hace limpieza y lo carga en la BD.
    """
    if not os.path.exists(CSV_FILE_PATH):
        raise FileNotFoundError(f"El archivo {CSV_FILE_PATH} no existe. Por favor ejecutar generate_historical.py primero.")
        
    print(f"Leyendo archivo temporal {CSV_FILE_PATH}")
    df = pd.read_csv(CSV_FILE_PATH)
    
    # Ejemplo de limpieza/transformación con pandas
    print("Transformando y limpiando datos...")
    df['fecha_venta'] = pd.to_datetime(df['fecha_venta'])
    df.fillna('Desconocido', inplace=True)
    df['total'] = df['cantidad'] * df['precio_unitario'] # asegurar la integridad del precio
    
    # Cargamos en PostgreSQL, anexando datos nuevos en caso de reprocesamiento.
    # idealmente `if_exists='append'`, pero aquí vamos a usar replace para un entorno local mas limpio
    engine = get_db_engine()
    
    print(f"Cargando {len(df)} registros a la tabla 'ventas_historicas'...")
    # 'append' significa que añadirá, pero el primary key en serie puede desbordarse. 
    # Mantenemos append para modelar de forma clásica un Batch Addivo.
    df.to_sql('ventas_historicas', engine, if_exists='append', index=False)
    
    print("Carga exitosa en batch concluida.")

# Definición del DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'batch_donas_dag',
    default_args=default_args,
    description='Procesa datos históricos de ventas de donas (Batch)',
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['batch', 'donas']
) as dag:

    procesar_datos_batch = PythonOperator(
        task_id='procesar_datos_csv',
        python_callable=extract_and_load_data
    )

    procesar_datos_batch
