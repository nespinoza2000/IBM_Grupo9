import pandas as pd
import numpy as np
import openpyxl
import matplotlib.pyplot as plt
import seaborn as sns

ventas=pd.read_excel("Base\\Ventas.xlsx")
clientes=pd.read_excel('Base\\Clientes.xlsx')
detalle=pd.read_excel('Base\\Detalle_ventas.xlsx')
productos=pd.read_excel('Base\\Productos.xlsx')

ventas_detalle=pd.merge(ventas,detalle,on='id_venta')
datos=pd.merge(ventas_detalle,productos,on='id_producto')
datos=pd.merge(datos,clientes,on='id_cliente')
datos=pd.merge(datos, productos,on='id_producto')

medios,conteo=np.unique(datos['medio_pago'],return_counts=True)
frecuencia_medios=dict(zip(medios,conteo))
################################
#Menú
def mostrar_menu():
    print("MENÚ PRINCIPAL")
    print("1. Tema")
    print("2. Problema")
    print("3. Solución")
    print("4. Base de Datos")
    print("5. Salir")
################################
while True:
    mostrar_menu()
    opcion = input("Selecciona una opción:")
    if opcion == "1":
        print("\nTema:Análisis de los diferentes métodos de pago utilizados en las ventas de la tienda Aurelion \n")
    elif opcion == "2":
        print("\nProblema:\n")
        print("La tienda no tiene visibilidad sobre los métodos de pago usados por los clientes.\n")
        print("Actualmente, vende sin medir el comportamiento de pago, lo que impide:\n")
        print("- Identificar qué medios de pago son los más usados.\n")
        print("- Detectar tendencias o patrones de uso según productos o regiones.\n")
        print("- Tomar decisiones informadas sobre qué servicios financieros priorizar.\n")
    elif opcion == "3":
        print("\nSolución: Desarrollar un sistema en Python para analizar las ventas y detectar patrones de uso de medios de pago.\n")
        print("Frecuencia de métodos de pago")
        for medio, total in frecuencia_medios.items():
            print(f"{medio}:{total}")

        productos_por_medio =(
            datos.groupby(['medio_pago','nombre_producto'])['cantidad']
            .sum()
            .reset_index()
        )

        top_productos=productos_por_medio.sort_values(
            ['medio_pago','cantidad'],ascending=[True,False]
        ).groupby('medio_pago').head(3)

        print('Productos más vendidos por medio de pago')
        print(top_productos)

        ciudades=(
            datos.groupby(['medio_pago','ciudad'])['id_cliente']
            .nunique()
            .reset_index()
            .rename(columns={'id_cliente':'num_clientes'})
        )
        top_ciudades=ciudades.sort_values(['medio_pago','num_clientes'],ascending=[True,False]).groupby('medio_pago').head(3)
        print('Ciudades con mayor indicencia por medio de pago')
        print(top_ciudades)

        datos['fecha']=pd.to_datetime(datos['fecha'])
        datos['dia_semana']=datos['fecha'].dt.day_name()

        dias=(
            datos.groupby(['medio_pago','dia_semana'])['id_venta']
            .nunique()
            .reset_index()
            .rename(columns={'id_venta':'ventas_dia'})
        )

        print('Ventas por día de la semana y medio de pago')
        print(dias)

        medios=list(frecuencia_medios.keys())
        conteo=list(frecuencia_medios.values())

        plt.figure(figsize=(6,4))
        sns.barplot(x=medios, y=conteo, palette='viridis')
        plt.title('Frecuencia de métodos de pago')
        plt.ylabel('Cantidad de transacciones')
        plt.xlabel('Método de pago')
        plt.show()

        plt.figure(figsize=(10,6))
        sns.barplot(data=top_productos, x='nombre_producto', y='cantidad', hue='medio_pago')
        plt.xticks(rotation=45,ha='right')
        plt.title("Top 3 productos por método de pago")
        plt.xlabel("Producto")
        plt.ylabel("Cantidad vendida")
        plt.legend(title="Medio de pago")
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(10,6))
        sns.barplot(data=top_ciudades, y='ciudad', x='num_clientes', hue='medio_pago', dodge=True)
        plt.title("Top 3 ciudades por medio de pago")
        plt.xlabel("Número de clientes")
        plt.ylabel("Ciudad")
        plt.show()

        plt.figure(figsize=(10,6))
        sns.lineplot(data=dias, x='dia_semana', y='ventas_dia', hue='medio_pago', marker='o')
        plt.title("Ventas por día de la semana y medio de pago")
        plt.xlabel("Día de la semana")
        plt.ylabel("Número de ventas")
        plt.show()

        print("Conclusión \n")
        print("El método de pago más usado es el efectivo con 111 clientes.")
        print("El método de pago menos usado es la tarjeta con 69 clientes")
        print("Los 3 productos más comprados con efectivo son:\n Chicle Menta \n Aceite de Girasol 1L \n Pizza Congelada Muzzarella")
        print("Los 3 productos más comprados con tarjeta son: \n Aceitunas Verdes 200g \n Energética Nitro 500ml \n Toallas Húmedas x50")
        print("Tanto la ciudad de Cordoba como Rio Cuarto usan efectivo para comprar.")
        print("Rio Cuarto usa más QR que efectivo, siendo efectivo el segundo método de pago más usado.")
        print("Los días Lunes, Martes y Viernes los clientes compran con efectivo.")
        print("Los días Jueves usan más el QR para comprar en la tienda.")
        print("Los días Miércoles usan tarjeta para comprar en la tienda.")
        print("Los días Sábados usan más los QR y transferencia para comprar la tienda.")
    elif opcion == "4":
        print("\nBase de Datos: Contiene las tablas de transacciones, estudiantes y productos.\n")
        print(ventas.head(5))
        print(clientes.head(5))
        print(detalle.head(5))
        print(productos.head(5))
    elif opcion == "5":
        print("\nSaliendo del programa.\n")
        break
    else:
        print("\nOpción no válida. Intenta de nuevo.\n")
################################
