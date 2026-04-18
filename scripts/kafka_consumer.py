import json
from confluent_kafka import Consumer, KafkaError
from sqlalchemy import create_engine
import pandas as pd

# Usar 'localhost' para correr este script fuera de Docker. 
# Si se corre DENTRO de la red de Docker se debe cambiar a 'kafka:29092'.
KAFKA_BROKER = 'localhost:9092' 
TOPIC_NAME = 'ventas_topic'
GROUP_ID = 'grupo_ventas_streaming'
DB_CONN = "postgresql+psycopg2://postgres:postgres@localhost:5432/donas_db"

def start_consumer():
    conf = {
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': GROUP_ID,
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(conf)
    consumer.subscribe([TOPIC_NAME])
    
    engine = create_engine(DB_CONN)
    
    print(f"Escuchando a Kafka en {KAFKA_BROKER} - Topic: {TOPIC_NAME}...")

    try:
        while True:
            msg = consumer.poll(1.0)
            
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print('Fin de partición alcanzado {0}/{1}'
                          .format(msg.topic(), msg.partition()))
                else:
                    print(f"Error: {msg.error()}")
                continue
                
            # Procesar el mensaje
            mensaje_str = msg.value().decode('utf-8')
            venta = json.loads(mensaje_str)
            print(f"Procesando venta realtime: {venta}")
            
            # Formateamos un DataFrame con Pandas 
            df_venta = pd.DataFrame([venta])
            # Aseguramos el tipo date
            df_venta['fecha_venta'] = pd.to_datetime(df_venta['fecha_venta'])
            
            # Guardamos en bd usando pandas to_sql
            df_venta.to_sql('ventas_streaming', engine, if_exists='append', index=False)

    except KeyboardInterrupt:
        print("\nDeteniendo consumidor...")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        consumer.close()

if __name__ == "__main__":
    start_consumer()
