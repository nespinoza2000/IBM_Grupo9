import pandas as pd

def menu():

    print("\n" + "="*60)
    print("  EXPLORADOR DE ARCHIVOS - GRUPO 9")
    print("="*60)
    print("Archivos disponibles:\n " \
      "1. Clientes.csv\n " \
      "2. Detalle_ventas.csv\n " \
      "3. Productos.csv\n " \
      "4. Ventas.csv\n " \
      "5. Salir")
    print("-"*60)

def leer_archivo(nombre_archivo):
    """Lee un archivo CSV y muestra información básica"""
    try:
        ruta = f"Base/{nombre_archivo}"
        # Leer el archivo CSV
        df = pd.read_csv(ruta, encoding='utf-8', sep=';')
        
        print(f"\n{'='*60}")
        print(f"  ARCHIVO: {nombre_archivo}")
        print(f"{'='*60}")
        
        # Mostrar información básica
        print(f"\n📊 Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
        print(f"\n📋 Columnas: {list(df.columns)}")
        
        print(f"\n🔍 Primeras 5 filas:")
        print(df.head())
        
        print(f"\n📈 Información del DataFrame:")
        print(df.info())
        
        print(f"\n📊 Estadísticas descriptivas:")
        print(df.describe())
        
    except FileNotFoundError:
        print(f"\n❌ Error: El archivo '{nombre_archivo}' no se encontró.")
    except Exception as e:
        print(f"\n❌ Error al leer el archivo: {e}")

def main():
    """Función principal del programa"""
    
    print("\n¡Bienvenido al Explorador de Archivos del Grupo 9!")
    
    # Diccionario con los nombres de archivos
    archivos = {
        "1": "Clientes.csv",
        "2": "Detalle_ventas.csv",
        "3": "Productos.csv",
        "4": "Ventas.csv"
    }
    
    while True:
        menu()
        opcion = input("\nSeleccione el archivo que desea explorar (1-5): ").strip()
        
        if opcion in archivos:
            leer_archivo(archivos[opcion])
            
        elif opcion == "5":
            print("\n¡Hasta pronto!")
            break
            
        else:
            print("\n❌ Error. Por favor, seleccione una opción válida (1-5).")
        
        input("\nPresiona Enter para continuar...")

# Ejecutar el programa
if __name__ == "__main__":
    main()