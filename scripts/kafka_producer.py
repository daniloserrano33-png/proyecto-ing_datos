import json
import time
import random
from datetime import datetime
from confluent_kafka import Producer

# Configuración de Kafka (referenciando localhost o el nombre del contenedor)
KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'ventas_topic'

TIPOS_DONA = ['Glaseada', 'Chocolate', 'Rellena de Fresa', 'Boston Cream', 'Mapple', 'Azúcar y Canela']
PRECIOS = [1.50, 2.00, 2.25, 2.50, 1.75, 1.25]
METODOS_PAGO = ['Efectivo', 'Tarjeta de Crédito', 'Tarjeta de Débito', 'Transferencia']
SUCURSALES = ['Centro', 'Norte', 'Sur', 'Valle']
EMPLEADOS_IDS = [101, 102, 103, 104, 105, 106, 107, 108]

def acked(err, msg):
    if err is not None:
        print(f"Error al enviar mensaje: {err}")
    else:
        print(f"Mensaje enviado a {msg.topic()} partición [{msg.partition()}]")

def generar_venta():
    idx_dona = random.randint(0, len(TIPOS_DONA) - 1)
    tipo = TIPOS_DONA[idx_dona]
    precio_uni = PRECIOS[idx_dona]
    cantidad = random.randint(1, 4)
    total = round(cantidad * precio_uni, 2)
    
    venta = {
        'fecha_venta': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'tipo_dona': tipo,
        'cantidad': cantidad,
        'precio_unitario': precio_uni,
        'total': total,
        'metodo_pago': random.choice(METODOS_PAGO),
        'id_empleado': random.choice(EMPLEADOS_IDS),
        'sucursal': random.choice(SUCURSALES)
    }
    return venta

def iniciar_producer():
    conf = {'bootstrap.servers': KAFKA_BROKER}
    producer = Producer(conf)
    
    print(f"Iniciando simulación de ventas en tiempo real... (Topic: {TOPIC_NAME})")
    try:
        while True:
            venta = generar_venta()
            # Enviar mensaje a Kafka
            producer.produce(TOPIC_NAME, json.dumps(venta).encode('utf-8'), callback=acked)
            # Esperar a que se envíe
            producer.poll(0)
            
            # Simular tiempo entre ventas (1 a 5 segundos)
            time.sleep(random.uniform(1.0, 5.0))
            
    except KeyboardInterrupt:
        print("\nDeteniendo productor...")
    finally:
        producer.flush()

if __name__ == "__main__":
    iniciar_producer()
