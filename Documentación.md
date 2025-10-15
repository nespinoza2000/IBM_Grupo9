# Proyecto Aurelion
**Autor**: Grupo 9
**Fecha**: 28/09/2025

##  CONTEXTO DEL PROYECTO Y PLANTEAMIENTO DEL PROBLEMA

### TEMA:
Retail

### PROBLEMA:
Durante el análisis exploratorio realizado en la base de datos, **identificamos una falta de visibilidad sobre el comportamiento de ventas**, especialmente, en relación **con los medios de pago utilizados**. 
    - Se desconoce cuáles son los medios de pago más utilizados por los clientes

### PROPUESTA DE SOLUCIÓN
Planteamos desarrollar un sistema en Python que analice las ventas y detecte patrones de uso de los medios de pago en las ventas, con el objetivo de:
* Identificar qué medios de pago son los más usados.
* Identificar cuál es el ingreso promedio por venta que genera cada medio de pago.
* Detectar tendencias o patrones de uso según productos o regiones.

Con esa información pretendemos:
* Incentivar el uso de ciertos métodos de pago.
* Invertir en mejorar la infraestructura de cobro más demandado.
* Ofrecer al cliente su medio de pago preferido.

## REFLEXIONES INICIALES
En base a la problemática identificada, comenzamos a plantearnos algunas preguntas que podrían servirnos de guía para el análisis:
- ¿Cuáles son los medios de pago más utilizados? ¿Cuáles menos?
- ¿Qué volumen total de ventas representa cada medio de pago (en dinero y cantidad)?
- ¿Qué categorías de producto se asocian más con cada medio de pago?
    - Qué productos se compran más con cada método de pago?
- ¿Cuál es el ticket promedio por medio de pago? ¿Qué diferencias existen entre ellos?
- ¿Qué ciudades utilizan más cada medio de pago? ¿Los clientes cambian de medio o usan siempre el mismo?
    - ¿Qué clientes usan más de un medio de pago?
- ¿Qué días de la semana (lunes a domingo) se usan más y menos cada medio de pago?
    - ¿Influye el día o el monto total en la elección del medio de pago?
- ¿Existen relaciones entre tipo de producto y medio de pago? ¿Depende el medio de pago del monto total o del tipo de producto?
- ¿Se puede analizar el comportamiento por edades? ¿Tenemos ese campo?
    - ¿Qué datos nuevos serían necesarios para enriquecer el análisis?


## FUENTE DE DATOS

La base de datos está compuesta por 4 archivos de Excel (.xlsx). Los mismos representan una entidad diferente cada uno:
+ **Clientes** (Contiene información de los usuarios registrados).
+ **Productos** (Lista de productos disponibles con sus características).
+ **Ventas** (Registra cada transacción realizada por los clientes).
+ **Detalle_ventas** (Desglosa los productos vendidos en cada transacción, con cantidades e importes).

### ESCALA
La base de datos presenta una escala de:
* Clientes: 100 registros.
* Productos: 100 registros.
* Ventas: 120 registros.
* Detalle de ventas: más de 3000 registros (alta granularidad).

### ESTRUCTURA DE LAS ENTIDADES 

#### Clientes
Cuenta con 5 campos:
+ id_cliente (PK) -int-
+ nombre_cliente -str-          (NOMINAL)
+ email -str-                   (NOMINAL)
+ ciudad -str-                  (NOMINAL)  
    - Carlos Paz - Rio Cuarto - Villa Maria - Cordoba - Mendiolaza - Alta Gracia
+ fecha alta -date-             (INTERVALO)
    - 01/01/2023 a 10/04/2023

#### Productos
Cuenta con 4 campos:
+ id_producto (PK) -int-    (RAZON)
    - 1 a 100
+ nombre_producto -str-     (NOMINAL)
+ categoria -str-           (NOMINAL)
    - Alimentos - Limpieza
+ precio_unitario -int-     (RAZON)
    - 272 a 4982

#### Ventas
Cuenta con 5 campos:
+ id_venta (PK) -int-           (RAZON)
    - 1 a 120
+ fecha -date-                  (INTERVALO)
    - 2/01/2024 al 28/06/2024
+ id_cliente (FK) -int-         (RAZON)
+ email -str-                   (NOMINAL)
+ medio_pago -str-              (NOMINAL)
    - tarjeta - qr - transferencia - efectivo 

#### detalle ventas
Cuenta con 6 campos:
+ id_venta (FK)
+ id_producto (FK)          (RAZON)
+ nombre_producto           (NOMINAL)
+ cantidad                  (RAZON)
+ precio_unitario           (RAZON)
+ importe                   (RAZON)



## REFLEXIONES SOBRE LA BASE DE DATOS

Durante la revisión inicial, detectamos algunos obstáculos:
Las entidades no están completamente normalizadas. Por ejemplo:
  - En “Ventas” se repite información del cliente (nombre, email).
  - En “Detalle de Ventas” se repite información del producto (nombre, precio).
* No existen relaciones explícitas entre las entidades (PK-FK), por lo que hay que incluirlas en un modelo de datos relacional.

Algunos campos que pueden servir como llaves entre entidades podrían ser:
* id_cliente conecta clientes con ventas.
* id_venta conecta ventas con detalle_ventas.
* id_producto conecta detalle_ventas con productos.

# PROGRAMA PYTHON SOBRE DOCUMENTACIÓN

## PASOS
1. Mensaje de Bienvenida
2. Presentar las opciones en base a las secciones que queremos mostrar
3. El usuario elija cuál opción ver
    * Tema
    * Problema
    * Solución
    * Fuente de Datos
    * Estructura de las entidades
4. Mostrar información de la sección solicitada
5. Repetir las veces que sea necesario según lo solicite el usuario
6. FIN


## PSEUDOCÓDIGO
INICIO
    Mensaje de Bienvenida
    LEER Opciones_Sección
    INPUT Sección
        SI Opción = 1
            Mostrar = TEMA
        SI Opción = 2
            Mostrar = PROBLEMA
        SI Opción = 3
            Mostrar = PROPUESTA DE SOLUCIÓN
        SI Opción = 4
            Mostrar = BASE DE DATOS
        SINO
            Mostrar = MENSAJE DE CIERRE
FIN

## DIAGRAMA DE FLUJO

<img width="1024" height="682"  src="Diagrama de flujo Documentacion.jpg" />
