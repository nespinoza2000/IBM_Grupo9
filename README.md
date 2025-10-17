# Presentación
<img width="1024" height="682" alt="Guayerd" src="https://github.com/user-attachments/assets/de4886dc-1ec3-49a9-8d48-6661cdc20159" />

---

## Integrantes

- Ivan Zirulnik
- Nicolas Espinoza
- Karina Pineda
- Juan Chero
- Agostina Torres
- Yeisim Cerna
- Diego Gutiérrez
- Sofia González
- Andrea Castro

# TEMA:
RETAIL - Análisis de los métodos de pago utilizados en las ventas

# PROBLEMA: 
Durante el análisis exploratorio realizado en la base de datos, identificamos una **falta de visibilidad sobre el comportamiento de ventas**, especialmente, en relación **con los medios de pago utilizados**.

# SOLUCIÓN:
Planteamos desarrollar un sistema en Python que analice las ventas y detecte patrones de uso de los medios de pago en las ventas, con el objetivo de:
    - Identificar qué medios de pago son los más usados.
    - Identificar cuál es el ingreso promedio por venta que genera cada medio de pago.
    - Detectar tendencias o patrones de uso según productos o regiones.

Con esa información pretendemos:
    - Incentivar el uso de ciertos métodos de pago.
    - Invertir en mejorar la infraestructura de cobro más demandado.
    - Ofrecer al cliente su medio de pago preferido.

# DATASET DE REFERENCIA

## FUENTE DE DATOS Y DEFINICIÓN
La base de datos proviene de la tienda Aurelion y está compuesta por 4 archivos de Excel (.xlsx).

Incluye 4 tablas principales: 
- **Clientes** (Contiene información de los usuarios registrados que compran en la tienda)
- **Productos** (Lista de productos disponibles con sus características)
- **Ventas** (Registra cada transacción realizada por los clientes)
- **Detalle_Ventas** (Desglosa los productos vendidos en cada transacción, con cantidades e importes)

## ESTRUCTURA Y TIPO DE DATO
### Clientes (5 campos):

| Campo          | Tipo   |
|----------------|--------|
| id_cliente     | int    |
| nombre_cliente | str    |
| email          | str    |
| ciudad         | str    |
| fecha_alta     | date   |

---

### Productos (4 campos):

| Campo           | Tipo  |
|-----------------|-------|
| id_producto     | int   |
| nombre_producto | str   |
| categoria       | str   |
| precio_unitario | float |

---

### Ventas (5 campos):

| Campo          | Tipo |
|----------------|------|
| id_venta       | int  |
| fecha          | date |
| id_cliente     | int  |
| nombre_cliente | str  |
| email          | str  |
| medio_pago     | str  |

---

### Detalle_ventas (6 campos):

| Campo           | Tipo  |
|-----------------|-------|
| id_venta        | int   |
| id_producto     | int   |
| nombre_producto | str   |
| cantidad        | int   |
| precio_unitario | float |
| importe         | float |

## ESCALA
La base de datos presenta una escala de:
* Clientes: 100 registros.
* Productos: 100 registros.
* Ventas: 120 registros.
* Detalle de ventas: más de 3000 registros (alta granularidad).

# REFLEXIONES SOBRE LA BASE DE DATOS
Durante la revisión inicial, detectamos algunos obstáculos:
Las entidades no están completamente normalizadas. Por ejemplo:
  - En “Ventas” se repite información del cliente (nombre, email).
  - En “Detalle de Ventas” se repite información del producto (nombre, precio).
* No existen relaciones explícitas entre las entidades (PK-FK), por lo que hay que incluirlas en un modelo de datos relacional.

Algunos campos que pueden servir como llaves entre entidades podrían ser:
* id_cliente conecta clientes con ventas.
* id_venta conecta ventas con detalle_ventas.
* id_producto conecta detalle_ventas con productos.

# INFORMACIÓN
La tienda puede invertir en mejorar los métodos de pago más demandados. Puede incentivar ciertos métodos de pago.

- ¿Cuáles son los métodos de pago más utilizados?
- ¿Qué volumen total de ventas representa cada medio de pago (en dinero y cantidad)?
- ¿Qué productos son los más comprados según el método de pago?
- ¿Existen relaciones entre tipo de producto y medio de pago? 
- ¿De qué lugares provienen los clientes que usan esos métodos de pago?
- ¿Los clientes usan siempre el mismo método de pago?
- ¿Qué días de la semana se usan más y menos los diferentes métodos de pago?
- ¿Qué datos son necesarios para el análisis del problema?
- ¿Necesitamos nuevos campos de datos para realizar un mejor análisis?

# PASOS
1. Leer los datos desde los archivos excel del dataset(Clientes, Ventas, Productos y Detalle_ventas).
2. Procesar y unificar la información para:
    - Detectar los métodos de pago más frecuentes.
    - Identificar los productos más vendidos y menos vendidos por tipo de pago.
    - Determinar los lugares con mayor incidencia de cada método de pago.
    - Analizar variaciones temporales(por días de la semana o fechas específicas).
3. Generar gráficos y reportes para una mejor interpretación.

# PSEUDOCÓDIGO MENÚ
1. Tema
    1. Imprimir temática
2. Problema
    1. Imprimir problemática
3. Solución 
    1. Importar librerías(pandas y numpy)
    2. Cargar los datos(los 4 datasets)
    3. Unir tablas por claves
        - ventas_detalle ← unir(ventas, detalle, por="id_venta")
        - data ← unir(ventas_detalle, clientes, por="id_cliente")
        - data ← unir(data, productos, por="id_producto")
    4. Analizar métodos de pago:
        - listar los medios de pago
        - contar los métodos de pago
        - ver los métodos de pago más usados (contar)
    5. Analizar productos por método de pago:
        - agrupar los métodos de pago según el id del producto
        - sumar cantidad vendida
        - obtener top productos por métodos de pago
    6. Analizar ciudades:
        - agrupar datos de métodos de pago según la ciudad
        - contar clientes por métodos de pago y ciudad
    7. Analizar días de la semana:
        - extraer el día de la semana
        - agrupar por medio_pago y dia_semana
        - contar número de ventas
    8. Mostrar resultados
        - imprimir frecuencia de medios de pago
        - imprimir productos más vendidos por medio
        - imprimir ciudades con mayor incidencia
        - imprimir uso por día de semana
4. Base de datos
    1. Imprimir el contenido de Clientes, Ventas, Productos y Detalle_ventas.

# DIAGRAMA DEL PROGRAMA
![Diagrama de flujo](Diagrama_de_flujo.png)
# SUGERENCIAS Y MEJORAR APLICADAS CON COPILOT
