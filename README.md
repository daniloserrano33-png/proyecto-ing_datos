# La Dona Dorada - Pipeline de Datos (Batch & Streaming)

Este proyecto implementa una arquitectura híbrida (Lambda) para el procesamiento de datos enfocados en una tienda de donas. 
Este proyecto procesa datos en **Batch** (con Airflow y Pandas) y en **Streaming** (con Apache Kafka). Todos los datos se centralizan en una base de datos PostgreSQL y se analizan visualmente en Apache Superset.

## Arquitectura
- **Generador de Datos:** Scripts en Python (Pandas) que simulan ventas de donas.
- **Batch Processing:** Apache Airflow ejecuta un DAG diario (`batch_donas_dag`) que lee un archivo CSV histórico, lo limpia e ingresa en PostgreSQL (`ventas_historicas`).
- **Streaming Processing:** `kafka_producer.py` envía eventos JSON de ventas en tiempo real a Kafka. `kafka_consumer.py` procesa estos eventos e inserta los registros en PostgreSQL (`ventas_streaming`).
- **Data Warehouse:** PostgreSQL.
- **Visualización:** Apache Superset para la creación de Dashboards.

## Requisitos Previos
- Docker y Docker Compose instalados.
- Python 3.9+ instalado localmente (para correr los scripts de simulación y el consumidor fuera de los contenedores por facilidad de pruebas).

## Guía de Ejecución Rápida

### 1. Iniciar Infraestructura (Docker)
Levanta todos los servicios (Postgres, Kafka, Zookeeper, Airflow, Superset):
```bash
docker-compose up -d
```
*Nota: Puede tardar unos minutos la primera vez mientras Airflow y Superset inicializan sus bases de datos.*

### 2. Generar Datos Históricos
Instala las dependencias y genera el archivo CSV inicial (creará la carpeta `data/` y el archivo `historial_ventas.csv`):
```bash
pip install -r requirements.txt
python scripts/generate_historical.py
```

### 3. Procesamiento Batch (Airflow)
1. Ingresar a la interfaz de Airflow: `http://localhost:8080` (Usuario: `admin`, Clave: `admin`).
2. Buscar el DAG `batch_donas_dag`.
3. Encender el DAG.
4. Este pipeline extraerá el CSV procesado mediante Pandas y cargará la tabla `ventas_historicas` en PostgreSQL.

### 4. Procesamiento Streaming (Kafka)
Abre dos terminales diferentes localmente.
En la **Terminal 1**, inicia el consumidor (que correrá en *background* escuchando):
```bash
python scripts/kafka_consumer.py
```
En la **Terminal 2**, inicia el productor para simular ventas continuas:
```bash
python scripts/kafka_producer.py
```
Se puede ver cómo los datos fluyen a través del *broker* (`http://localhost:9092`) de Kafka y se persisten al instante en PostgreSQL (`ventas_streaming`).

### 5. Visualización (Apache Superset)
1. Accede a Superset: `http://localhost:8088` (Usuario: `admin`, Clave: `admin`).
2. **Conectar Base de Datos**:
   - Ve a `Settings -> Database Connections`.
   - Agrega la conexión: `postgresql+psycopg2://postgres:postgres@postgres:5432/donas_db`
   - Haz clic en *Test Connection* y luego *Connect*.
3. **Crear Datasets y Dashboards**:
   - Ve a `Datasets -> + Dataset`, selecciona la BD `donas_db`, esquema `public`, y las tablas `ventas_historicas` o `ventas_streaming`.
   - Crea un par de gráficos atractivos (Ej: Barras de cantidad de donas por sucursal, Torta de métodos de pago).

## Notas para la Exposición y Criterios 
* **Diseño y Arquitectura:** Resalta que este esquema **Lambda** resuelve la problemática de contar con el historial profundo (Batch) a la vez que atiende informes operativos al segundo (Streaming).
* **Innovación:** El concepto de "La Dona Dorada" lo vuelve un proyecto original, diferenciándose de los datasets de pruebas usuales y conectando los eventos al giro de la pastelería.
