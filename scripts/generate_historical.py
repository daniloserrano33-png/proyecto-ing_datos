import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Configuración
NUM_RECORDS = 50000
TIPOS_DONA = ['Glaseada', 'Chocolate', 'Rellena de Fresa', 'Boston Cream', 'Mapple', 'Azúcar y Canela']
PRECIOS = [1.50, 2.00, 2.25, 2.50, 1.75, 1.25]
METODOS_PAGO = ['Efectivo', 'Tarjeta de Crédito', 'Tarjeta de Débito', 'Transferencia']
SUCURSALES = ['Centro', 'Norte', 'Sur', 'Valle']
EMPLEADOS_IDS = [101, 102, 103, 104, 105, 106, 107, 108]

def generar_datos_historicos():
    print("Generando datos históricos...")
    
    fecha_fin = datetime.now() - timedelta(days=1)
    fecha_inicio = fecha_fin - timedelta(days=365) # 1 año de datos
    
    fechas = [fecha_inicio + timedelta(seconds=random.randint(0, int((fecha_fin - fecha_inicio).total_seconds()))) for _ in range(NUM_RECORDS)]
    fechas.sort() # Orden cronológico
    
    datos = []
    
    for i in range(NUM_RECORDS):
        idx_dona = random.randint(0, len(TIPOS_DONA) - 1)
        tipo = TIPOS_DONA[idx_dona]
        precio_uni = PRECIOS[idx_dona]
        cantidad = random.randint(1, 12)
        total = round(cantidad * precio_uni, 2)
        
        registro = {
            'id_venta': i + 1,
            'fecha_venta': fechas[i].strftime('%Y-%m-%d %H:%M:%S'),
            'tipo_dona': tipo,
            'cantidad': cantidad,
            'precio_unitario': precio_uni,
            'total': total,
            'metodo_pago': random.choice(METODOS_PAGO),
            'id_empleado': random.choice(EMPLEADOS_IDS),
            'sucursal': random.choice(SUCURSALES)
        }
        datos.append(registro)
        
    df = pd.DataFrame(datos)
    
    # Crear directorio si no existe
    os.makedirs('../data', exist_ok=True)
    filepath = '../data/historial_ventas.csv'
    df.to_csv(filepath, index=False)
    print(f"Generados {NUM_RECORDS} registros en {filepath}")

if __name__ == "__main__":
    generar_datos_historicos()
