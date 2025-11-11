Autor : Grupo 9 - Integrantes:

Andrea Castro
Yeism Cerna
Juan Chero
Nicolás Espinoza
Sofía González
Diego Gutiérrez
Karina Pineda
Agostina Torres
Iván Zirulnik

"""
Este script contiene el informe del proyecto de análisis de ventas 
en formato Markdown y una función para guardarlo como un archivo .md.
"""

def generar_y_guardar_informe():
    """
    Genera el contenido Markdown del informe y lo guarda en un archivo.
    """
    
    informe_markdown = """
# 📊 Análisis de Métodos de Pago de la Tienda Aurelion

Este documento detalla el proyecto de análisis de datos implementado en Python, enfocado en el estudio de las ventas y la distribución de los medios de pago utilizados por los clientes de la tienda Aurelion.

---

## 1. Tema del Proyecto
**Análisis de los diferentes métodos de pago utilizados en las ventas de la tienda Aurelion.**

El objetivo principal es transformar los datos transaccionales en información valiosa para la toma de decisiones financieras y operativas.

## 2. Problema a Solucionar
La tienda **no tiene visibilidad clara sobre los métodos de pago** que usan sus clientes. Actualmente, vende sin medir el comportamiento de pago de forma sistemática, lo que genera las siguientes limitaciones:

* Identificar qué medios de pago son los más usados y por qué.
* Detectar tendencias o patrones de uso según los productos comprados, las regiones (ciudades) o los días de la semana.
* Tomar decisiones informadas sobre qué servicios financieros o promociones priorizar.

## 3. Solución Propuesta (Metodología y Resultados)

La solución consiste en desarrollar un sistema de análisis de datos robusto en Python, utilizando las librerías **Pandas, NumPy, Matplotlib, Seaborn y SciPy**, para integrar la información y realizar análisis descriptivos y exploratorios.

### 3.1. Preparación y Unión de Datos

Se cargan cuatro bases de datos (archivos Excel) y se fusionan en un único *DataFrame* llamado `datos`:

| Archivo | Contenido | Clave de Unión |
| :--- | :--- | :--- |
| `Ventas.xlsx` | Transacciones de venta | `id_venta` |
| `Detalle_ventas.xlsx` | Productos vendidos por transacción | `id_venta` y `id_producto` |
| `Productos.xlsx` | Información de los productos | `id_producto` |
| `Clientes.xlsx` | Información demográfica del cliente | `id_cliente` |

El DataFrame final (`datos`) contiene toda la información de la venta, el cliente, el producto y el medio de pago asociado, lista para el análisis.

### 3.2. Hallazgos Clave (Resultados de la Opción "Solución")

El análisis exploratorio reveló los siguientes patrones de compra:

| Medio de Pago | Frecuencia (Total de Clientes) |
| :--- | :--- |
| **Efectivo** | 111 |
| **Tarjeta** | 69 |
| **QR** | (Otros) |

**Productos más vendidos por medio de pago:**

| Medio de Pago | Top 1 Producto | Top 2 Producto | Top 3 Producto |
| :--- | :--- | :--- | :--- |
| **Efectivo** | Chicle Menta | Aceite de Girasol 1L | Pizza Congelada Muzzarella |
| **Tarjeta** | Aceitunas Verdes 200g | Energética Nitro 500ml | Toallas Húmedas x50 |

**Ciudades con mayor incidencia por medio de pago:**
* Tanto la ciudad de **Córdoba** como **Río Cuarto** usan efectivo para comprar.
* **Río Cuarto** usa **más QR que efectivo**, siendo efectivo el segundo método de pago más usado en esa ciudad.

**Ventas por Día de la Semana:**
* Los días **Lunes, Martes y Viernes** los clientes compran predominantemente con **Efectivo**.
* Los días **Jueves** usan más el **QR** para comprar en la tienda.

---

## 4. Análisis Metodológico Detallado

El script original incluye funciones avanzadas de Data Science para asegurar la calidad y el entendimiento de las variables numéricas:

### 4.1. Estadísticas Descriptivas (Opción 5)

La función `estadisticas_descriptivas()` calcula y presenta métricas clave para las variables numéricas:

* **Medidas de Tendencia Central:** Media, Mediana y Moda.
* **Medidas de Dispersión:** Desviación Estándar, Varianza, Mínimo, Máximo y Rango.
* **Medidas de Forma:** Asimetría (*Skewness*) y Curtosis (*Kurtosis*).

### 4.2. Análisis de Distribución (Integrado en Opción 5)

La función `analizar_distribucion()` aplica múltiples pruebas estadísticas para determinar si las variables numéricas siguen una **Distribución Normal** (un requisito para muchas pruebas paramétricas):

| Prueba | Tipo de Análisis | Criterio de Normalidad ($\alpha=0.05$) |
| :--- | :--- | :--- |
| **Shapiro-Wilk** | Normalidad (Muestras pequeñas $\le 5000$) | $P$-valor $> 0.05$ |
| **Kolmogorov-Smirnov** | Normalidad (ajuste a la curva normal) | $P$-valor $> 0.05$ |
| **D'Agostino-Pearson** | Normalidad (basado en Skewness y Kurtosis) | $P$-valor $> 0.05$ |
| **Anderson-Darling** | Normalidad (comparación con valores críticos) | Estadístico $<$ Valor Crítico (5%) |

### 4.3. Detección de Outliers (Opción 6)

La función `detectar_outliers()` identifica valores atípicos mediante cinco métodos robustos:

1.  **Rango Intercuartílico (IQR)**
2.  **Z-Score**
3.  **Modified Z-Score (MAD)**
4.  **Percentiles Extremos**
5.  **Desviación Estándar ($\pm 3\sigma$)**

---

## 5. Gráficos Representativos (Opción 7)

La función `generar_graficos_representativos()` genera visualizaciones para la exploración de datos, incluyendo:

* **Matriz de Correlación** (Heatmap).
* **Histogramas** de variables numéricas.
* **Gráficos de Barras de Conteo** de variables categóricas.
* **Box Plots** para comparación de dispersión y detección visual de *outliers*.
"""
    
    nombre_archivo = "informe_analisis_ventas.md"
    try:
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(informe_markdown.strip())
        print(f"Informe guardado exitosamente como: {nombre_archivo}")
    except Exception as e:
        print(f"Error al escribir el archivo: {e}")


if __name__ == "__main__":
    generar_y_guardar_informe()

