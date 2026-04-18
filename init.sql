CREATE DATABASE airflow_db;
CREATE DATABASE superset_db;

\c donas_db;

CREATE TABLE ventas_historicas (
    id_venta SERIAL PRIMARY KEY,
    fecha_venta TIMESTAMP,
    tipo_dona VARCHAR(50),
    cantidad INT,
    precio_unitario NUMERIC(5,2),
    total NUMERIC(10,2),
    metodo_pago VARCHAR(50),
    id_empleado INT,
    sucursal VARCHAR(50)
);

CREATE TABLE ventas_streaming (
    id_venta SERIAL PRIMARY KEY,
    fecha_venta TIMESTAMP,
    tipo_dona VARCHAR(50),
    cantidad INT,
    precio_unitario NUMERIC(5,2),
    total NUMERIC(10,2),
    metodo_pago VARCHAR(50),
    id_empleado INT,
    sucursal VARCHAR(50)
);
