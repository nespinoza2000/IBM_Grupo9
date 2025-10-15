print("¡Bienvenido! Este es el Proyecto del Grupo 9 sobre la Tienda Aurelion")
print("Estas son las secciones del menú que puede consultar:\n 1. Tema\n 2. Problema\n 3. Solución\n 4. Base de datos\n 5. Cierre")

Tema = "Retail"
Problema = "falta  de visibilidad sobre el comportamiento de ventas, especialmente con los medios de pago utilizados.\n Esto dificulta la toma de decisiones sobre qué servicios financieros priorizar"
Solución = "un análisis del comportamiento en los métodos de pago, con el objetivo de:\n * Identificar patrones de compra y preferencias de los clientes.\n *Qué medios de pago son los más usados.\n * Detectar tendencias o patrones de uso según productos o regiones."
Base_de_datos = "La base de datos está compuesta por 4 archivos de Excel\n * Clientes\n * Productos\n * Ventas\n * Detalle ventas"
Salida = "Esto es todo por ahora. Pronto tendremos más detalles del proyecto"

Opciones_menu = {"1": Tema, "2": Problema, "3": Solución, "4": Base_de_datos, "5": Salida}

while True:
    Opciones_menu = input("Seleccione la sección que desea ver (1-5): ")
    if Opciones_menu == "1":
        print(f'El tema es {Tema}')
    elif Opciones_menu == "2":
        print(f'El problema es {Problema}')
    elif Opciones_menu == "3":
        print(f'La solución propuesta es {Solución}')
    elif Opciones_menu == "3":
        print(Solución)
    elif Opciones_menu == "4":
        print(Base_de_datos)
    elif Opciones_menu == "5":
        print(Salida)
        break
    else:
        print("Error. Por favor, seleccione una opción válida.")


