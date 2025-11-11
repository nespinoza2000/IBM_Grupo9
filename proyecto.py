import pandas as pd
import numpy as np
import openpyxl
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import shapiro, normaltest, anderson, kstest, skew, kurtosis
from sklearn.preprocessing import StandardScaler
from sklearn.covariance import EllipticEnvelope

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
    print("5. Estadísticas Descriptivas")
    print("6. Detección de Outliers")
    print("7. Gráficos Representativos")
    print("8. Salir")

def generar_graficos_representativos():
    """
    Genera gráficos representativos del dataset
    """
    print("\n" + "="*70)
    print("GRÁFICOS REPRESENTATIVOS DEL DATASET")
    print("="*70 + "\n")
    
    columnas_numericas = datos.select_dtypes(include=[np.number]).columns
    columnas_categoricas = datos.select_dtypes(include=['object']).columns
    
    # ==================== 1. Matriz de Correlación ====================
    if len(columnas_numericas) > 1:
        fig, ax = plt.subplots(figsize=(10, 8))
        corr_matrix = datos[columnas_numericas].corr()
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                   square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)
        plt.title('Matriz de Correlación (Variables Numéricas)', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    # ==================== 2. Distribuciones de Variables Numéricas ====================
    if len(columnas_numericas) > 0:
        n_cols = min(3, len(columnas_numericas))
        n_rows = (len(columnas_numericas) - 1) // n_cols + 1
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
        if n_rows == 1 and n_cols == 1:
            axes = [axes]
        elif n_rows == 1 or n_cols == 1:
            axes = axes.flatten()
        else:
            axes = axes.flatten()
        
        for idx, col in enumerate(columnas_numericas):
            ax = axes[idx]
            ax.hist(datos[col].dropna(), bins=30, color='skyblue', edgecolor='black', alpha=0.7)
            ax.axvline(datos[col].mean(), color='red', linestyle='--', linewidth=2, label='Media')
            ax.axvline(datos[col].median(), color='green', linestyle='--', linewidth=2, label='Mediana')
            ax.set_xlabel('Valor')
            ax.set_ylabel('Frecuencia')
            ax.set_title(f'Distribución: {col}', fontweight='bold')
            ax.legend()
            ax.grid(alpha=0.3)
        
        # Ocultar subplots vacíos
        for idx in range(len(columnas_numericas), len(axes)):
            axes[idx].axis('off')
        
        plt.tight_layout()
        plt.show()
    
    # ==================== 3. Conteos de Variables Categóricas ====================
    if len(columnas_categoricas) > 0:
        n_cols = min(2, len(columnas_categoricas))
        n_rows = (len(columnas_categoricas) - 1) // n_cols + 1
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(14, 6*n_rows))
        if n_rows == 1 and n_cols == 1:
            axes = [axes]
        elif n_rows == 1 or n_cols == 1:
            axes = axes.flatten()
        else:
            axes = axes.flatten()
        
        for idx, col in enumerate(columnas_categoricas):
            ax = axes[idx]
            valor_counts = datos[col].value_counts()
            colores = plt.cm.Set3(np.linspace(0, 1, len(valor_counts)))
            valor_counts.plot(kind='bar', ax=ax, color=colores, edgecolor='black')
            ax.set_xlabel(col)
            ax.set_ylabel('Cantidad')
            ax.set_title(f'Distribución: {col}', fontweight='bold')
            ax.grid(alpha=0.3, axis='y')
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Ocultar subplots vacíos
        for idx in range(len(columnas_categoricas), len(axes)):
            axes[idx].axis('off')
        
        plt.tight_layout()
        plt.show()
    
    # ==================== 4. Box Plots de Variables Numéricas ====================
    if len(columnas_numericas) > 0:
        fig, ax = plt.subplots(figsize=(12, 6))
        
        datos_boxplot = [datos[col].dropna() for col in columnas_numericas]
        bp = ax.boxplot(datos_boxplot, labels=columnas_numericas, patch_artist=True)
        
        # Colorear los boxes
        for patch, color in zip(bp['boxes'], plt.cm.Pastel1(np.linspace(0, 1, len(bp['boxes'])))):
            patch.set_facecolor(color)
        
        ax.set_ylabel('Valor', fontsize=11)
        ax.set_title('Box Plots: Comparación de Variables Numéricas', fontsize=14, fontweight='bold')
        ax.grid(alpha=0.3, axis='y')
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
    
    # ==================== 5. Gráfico de Estadísticas ====================
    if len(columnas_numericas) > 0:
        fig, ax = plt.subplots(figsize=(12, 6))
        
        estadisticas = {
            'Media': [datos[col].mean() for col in columnas_numericas],
            'Mediana': [datos[col].median() for col in columnas_numericas],
            'Desv. Est.': [datos[col].std() for col in columnas_numericas]
        }
        
        x = np.arange(len(columnas_numericas))
        width = 0.25
        
        for idx, (stat, valores) in enumerate(estadisticas.items()):
            ax.bar(x + idx*width, valores, width, label=stat, edgecolor='black')
        
        ax.set_xlabel('Variables', fontsize=11)
        ax.set_ylabel('Valor', fontsize=11)
        ax.set_title('Comparativa de Estadísticas por Variable', fontsize=14, fontweight='bold')
        ax.set_xticks(x + width)
        ax.set_xticklabels(columnas_numericas, rotation=45, ha='right')
        ax.legend()
        ax.grid(alpha=0.3, axis='y')
        plt.tight_layout()
        plt.show()
    
    print("✓ Gráficos generados exitosamente\n")

def graficar_outliers(serie, nombre_variable, outliers_dict):
    """
    Crea gráficos para visualizar los outliers detectados
    """
    datos_validos = serie.dropna()
    
    if len(datos_validos) < 3:
        return
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(f'Análisis de Outliers: {nombre_variable}', fontsize=16, fontweight='bold')
    
    # Colores
    color_normal = 'skyblue'
    color_outlier = 'red'
    
    # ==================== GRÁFICO 1: Box Plot con Outliers ====================
    ax1 = axes[0, 0]
    
    bp = ax1.boxplot(datos_validos, vert=True, patch_artist=True, 
                      widths=0.5, showmeans=True,
                      meanprops=dict(marker='D', markerfacecolor='green', markersize=8))
    bp['boxes'][0].set_facecolor(color_normal)
    
    # Resaltar outliers detectados con IQR
    outliers_iqr = outliers_dict['iqr']
    ax1.scatter([1]*len(outliers_iqr), outliers_iqr, color=color_outlier, s=100, 
               zorder=3, label='Outliers (IQR)', marker='o', edgecolor='darkred', linewidth=2)
    
    ax1.set_ylabel('Valor', fontsize=11)
    ax1.set_title('Box Plot con Outliers (IQR)', fontweight='bold')
    ax1.grid(alpha=0.3, axis='y')
    ax1.legend()
    
    # ==================== GRÁFICO 2: Scatter Plot con Z-Score ====================
    ax2 = axes[0, 1]
    
    z_scores = np.abs(stats.zscore(datos_validos))
    colores = [color_outlier if z > 3 else color_normal for z in z_scores]
    
    ax2.scatter(range(len(datos_validos)), datos_validos, c=colores, alpha=0.6, s=50, edgecolors='black')
    
    # Líneas de límite
    media = datos_validos.mean()
    desv_est = datos_validos.std()
    ax2.axhline(media + 3*desv_est, color='red', linestyle='--', linewidth=2, label='Límite ±3σ')
    ax2.axhline(media - 3*desv_est, color='red', linestyle='--', linewidth=2)
    ax2.axhline(media, color='green', linestyle='--', linewidth=1, alpha=0.5, label='Media')
    
    ax2.set_xlabel('Índice', fontsize=11)
    ax2.set_ylabel('Valor', fontsize=11)
    ax2.set_title('Scatter Plot con Z-Score (±3σ)', fontweight='bold')
    ax2.grid(alpha=0.3)
    ax2.legend()
    
    # ==================== GRÁFICO 3: Histograma con Outliers Destacados ====================
    ax3 = axes[1, 0]
    
    # Histograma de todos los datos
    ax3.hist(datos_validos, bins=30, color=color_normal, alpha=0.7, edgecolor='black', label='Valores normales')
    
    # Histograma de outliers
    if len(outliers_dict['iqr']) > 0:
        ax3.hist(outliers_dict['iqr'], bins=30, color=color_outlier, alpha=0.7, 
                edgecolor='darkred', label='Outliers', linewidth=2)
    
    ax3.set_xlabel('Valor', fontsize=11)
    ax3.set_ylabel('Frecuencia', fontsize=11)
    ax3.set_title('Histograma con Outliers Resaltados', fontweight='bold')
    ax3.grid(alpha=0.3, axis='y')
    ax3.legend()
    
    # ==================== GRÁFICO 4: Comparativa de Métodos ====================
    ax4 = axes[1, 1]
    
    # Contar outliers por método
    metodos = []
    conteos = []
    
    for metodo, outliers in outliers_dict.items():
        if len(outliers) > 0:
            metodos.append(metodo.upper())
            conteos.append(len(outliers))
    
    if len(metodos) > 0:
        colores_barras = ['#FF6B6B' if c > 0 else '#95E1D3' for c in conteos]
        barras = ax4.bar(metodos, conteos, color=colores_barras, edgecolor='black', linewidth=1.5)
        
        # Añadir valores en las barras
        for barra, conteo in zip(barras, conteos):
            altura = barra.get_height()
            ax4.text(barra.get_x() + barra.get_width()/2., altura,
                    f'{int(conteo)}', ha='center', va='bottom', fontweight='bold')
        
        ax4.set_ylabel('Cantidad de Outliers', fontsize=11)
        ax4.set_title('Comparativa de Métodos de Detección', fontweight='bold')
        ax4.grid(alpha=0.3, axis='y')
    else:
        ax4.text(0.5, 0.5, 'No hay outliers detectados', 
                ha='center', va='center', transform=ax4.transAxes, fontsize=12)
        ax4.set_title('Comparativa de Métodos', fontweight='bold')
    
    plt.tight_layout()
    plt.show()

def detectar_outliers(serie, nombre_variable):
    """
    Detecta outliers usando múltiples métodos estadísticos
    """
    print(f"\n🎯 DETECCIÓN DE OUTLIERS: {nombre_variable.upper()}")
    print("="*70)
    
    datos_validos = serie.dropna()
    
    if len(datos_validos) < 3:
        print("⚠️  Datos insuficientes para detección de outliers")
        return
    
    # ==================== MÉTODO 1: IQR (Rango Intercuartílico) ====================
    print("\n📊 MÉTODO 1: IQR (Rango Intercuartílico)")
    print("-"*70)
    
    Q1 = datos_validos.quantile(0.25)
    Q3 = datos_validos.quantile(0.75)
    IQR = Q3 - Q1
    
    limite_inferior_iqr = Q1 - 1.5 * IQR
    limite_superior_iqr = Q3 + 1.5 * IQR
    
    outliers_iqr = datos_validos[(datos_validos < limite_inferior_iqr) | (datos_validos > limite_superior_iqr)]
    
    print(f"Q1 (25%): {Q1:.4f}")
    print(f"Q3 (75%): {Q3:.4f}")
    print(f"IQR: {IQR:.4f}")
    print(f"Límite inferior: {limite_inferior_iqr:.4f}")
    print(f"Límite superior: {limite_superior_iqr:.4f}")
    print(f"Outliers detectados: {len(outliers_iqr)}")
    
    if len(outliers_iqr) > 0:
        print(f"Porcentaje de outliers: {len(outliers_iqr)/len(datos_validos)*100:.2f}%")
        print(f"Valores: {sorted(outliers_iqr.values)}")
    else:
        print("✓ No hay outliers detectados con este método")
    
    # ==================== MÉTODO 2: Z-Score ====================
    print(f"\n📊 MÉTODO 2: Z-Score")
    print("-"*70)
    
    z_scores = np.abs(stats.zscore(datos_validos))
    umbral_z = 3  # Desviaciones estándar
    
    outliers_zscore = datos_validos[z_scores > umbral_z]
    
    print(f"Umbral Z-Score: {umbral_z} desviaciones estándar")
    print(f"Outliers detectados (|z| > {umbral_z}): {len(outliers_zscore)}")
    
    if len(outliers_zscore) > 0:
        print(f"Porcentaje de outliers: {len(outliers_zscore)/len(datos_validos)*100:.2f}%")
        print(f"Valores: {sorted(outliers_zscore.values)}")
    else:
        print("✓ No hay outliers detectados con este método")
    
    # Z-Score más sensible (2.5)
    outliers_zscore_25 = datos_validos[z_scores > 2.5]
    print(f"\nOutliers detectados (|z| > 2.5 - más sensible): {len(outliers_zscore_25)}")
    if len(outliers_zscore_25) > 0:
        print(f"Porcentaje: {len(outliers_zscore_25)/len(datos_validos)*100:.2f}%")
    
    # ==================== MÉTODO 3: Modified Z-Score (MAD) ====================
    print(f"\n📊 MÉTODO 3: Modified Z-Score (Desviación Absoluta Mediana)")
    print("-"*70)
    
    mediana = np.median(datos_validos)
    mad = np.median(np.abs(datos_validos - mediana))
    
    if mad == 0:
        print("⚠️  No se puede calcular (MAD = 0)")
    else:
        modified_z_scores = 0.6745 * (datos_validos - mediana) / mad
        outliers_mad = datos_validos[np.abs(modified_z_scores) > 3.5]
        
        print(f"Mediana: {mediana:.4f}")
        print(f"MAD (Desviación Absoluta Mediana): {mad:.4f}")
        print(f"Outliers detectados (|modified_z| > 3.5): {len(outliers_mad)}")
        
        if len(outliers_mad) > 0:
            print(f"Porcentaje de outliers: {len(outliers_mad)/len(datos_validos)*100:.2f}%")
            print(f"Valores: {sorted(outliers_mad.values)}")
        else:
            print("✓ No hay outliers detectados con este método")
    
    # ==================== MÉTODO 4: Aislamiento por Percentiles ====================
    print(f"\n📊 MÉTODO 4: Percentiles Extremos (1% y 99%)")
    print("-"*70)
    
    p1 = datos_validos.quantile(0.01)
    p99 = datos_validos.quantile(0.99)
    
    outliers_percentiles = datos_validos[(datos_validos < p1) | (datos_validos > p99)]
    
    print(f"P1 (1%): {p1:.4f}")
    print(f"P99 (99%): {p99:.4f}")
    print(f"Outliers detectados: {len(outliers_percentiles)}")
    
    if len(outliers_percentiles) > 0:
        print(f"Porcentaje de outliers: {len(outliers_percentiles)/len(datos_validos)*100:.2f}%")
        print(f"Valores: {sorted(outliers_percentiles.values)}")
    else:
        print("✓ No hay outliers detectados con este método")
    
    # ==================== MÉTODO 5: Aislamiento por Desviación Estándar ====================
    print(f"\n📊 MÉTODO 5: Desviación Estándar (±3σ)")
    print("-"*70)
    
    media = datos_validos.mean()
    desv_est = datos_validos.std()
    
    limite_inf_std = media - 3 * desv_est
    limite_sup_std = media + 3 * desv_est
    
    outliers_std = datos_validos[(datos_validos < limite_inf_std) | (datos_validos > limite_sup_std)]
    
    print(f"Media: {media:.4f}")
    print(f"Desviación estándar: {desv_est:.4f}")
    print(f"Límite inferior (μ - 3σ): {limite_inf_std:.4f}")
    print(f"Límite superior (μ + 3σ): {limite_sup_std:.4f}")
    print(f"Outliers detectados: {len(outliers_std)}")
    
    if len(outliers_std) > 0:
        print(f"Porcentaje de outliers: {len(outliers_std)/len(datos_validos)*100:.2f}%")
        print(f"Valores: {sorted(outliers_std.values)}")
    else:
        print("✓ No hay outliers detectados con este método")
    
    # ==================== RESUMEN ====================
    print(f"\n{'='*70}")
    print("📋 RESUMEN DE OUTLIERS DETECTADOS")
    print("="*70)
    
    total_outliers_unicos = len(set(outliers_iqr.index) | set(outliers_zscore.index) | 
                               set(outliers_mad.index if mad != 0 else []) | 
                               set(outliers_percentiles.index) | set(outliers_std.index))
    
    print(f"\nTotal de outliers únicos detectados (combinado): {total_outliers_unicos}")
    print(f"Porcentaje del dataset: {total_outliers_unicos/len(datos_validos)*100:.2f}%")
    
    print(f"\nRecomendaciones:")
    print(f"• Si < 5% de outliers: Probablemente son valores legítimos extremos")
    print(f"• Si 5-10% de outliers: Investiga y considera tratamiento")
    print(f"• Si > 10% de outliers: Revisa la calidad de los datos")
    
    print("="*70 + "\n")
    
    return {
        'iqr': outliers_iqr,
        'zscore': outliers_zscore,
        'mad': outliers_mad if mad != 0 else pd.Series(),
        'percentiles': outliers_percentiles,
        'desv_est': outliers_std
    }

def graficar_distribucion(serie, nombre_variable):
    """
    Crea gráficos para visualizar la distribución de una variable
    """
    datos_validos = serie.dropna()
    
    if len(datos_validos) < 3:
        return
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'Análisis de Distribución: {nombre_variable}', fontsize=16, fontweight='bold')
    
    # 1. Histograma con curva normal
    ax1 = axes[0, 0]
    ax1.hist(datos_validos, bins=30, density=True, alpha=0.7, color='skyblue', edgecolor='black')
    
    # Superponer curva normal teórica
    mu = datos_validos.mean()
    sigma = datos_validos.std()
    x = np.linspace(datos_validos.min(), datos_validos.max(), 100)
    ax1.plot(x, stats.norm.pdf(x, mu, sigma), 'r-', linewidth=2, label='Normal teórica')
    ax1.set_xlabel('Valor')
    ax1.set_ylabel('Densidad')
    ax1.set_title('Histograma con curva Normal')
    ax1.legend()
    ax1.grid(alpha=0.3)
    
    # 2. Q-Q Plot
    ax2 = axes[0, 1]
    stats.probplot(datos_validos, dist="norm", plot=ax2)
    ax2.set_title('Q-Q Plot (Normal)')
    ax2.grid(alpha=0.3)
    
    # 3. Density Plot con KDE
    ax3 = axes[1, 0]
    datos_validos.plot(kind='density', ax=ax3, color='green', linewidth=2)
    ax3.axvline(datos_validos.mean(), color='red', linestyle='--', linewidth=2, label='Media')
    ax3.axvline(datos_validos.median(), color='orange', linestyle='--', linewidth=2, label='Mediana')
    ax3.set_title('Gráfico de Densidad (KDE)')
    ax3.set_xlabel('Valor')
    ax3.set_ylabel('Densidad')
    ax3.legend()
    ax3.grid(alpha=0.3)
    
    # 4. Box Plot
    ax4 = axes[1, 1]
    box = ax4.boxplot(datos_validos, vert=True, patch_artist=True)
    box['boxes'][0].set_facecolor('lightblue')
    ax4.set_ylabel('Valor')
    ax4.set_title('Box Plot')
    ax4.grid(alpha=0.3, axis='y')
    
    # Añadir estadísticas en el gráfico
    stats_text = f"""
    Media: {datos_validos.mean():.2f}
    Mediana: {datos_validos.median():.2f}
    Std Dev: {datos_validos.std():.2f}
    Asimetría: {skew(datos_validos):.2f}
    Curtosis: {kurtosis(datos_validos):.2f}
    """
    ax4.text(1.3, datos_validos.mean(), stats_text, fontsize=9, 
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.show()

def analizar_distribucion(serie, nombre_variable):
    """
    Analiza el tipo de distribución de una variable numérica
    usando múltiples pruebas estadísticas
    """
    print(f"\n🔍 ANÁLISIS DE DISTRIBUCIÓN: {nombre_variable.upper()}")
    print("-" * 60)
    
    datos_validos = serie.dropna()
    
    if len(datos_validos) < 3:
        print("⚠️  Datos insuficientes para análisis de distribución")
        return
    
    # 1. Prueba de Shapiro-Wilk (mejor para muestras pequeñas)
    if len(datos_validos) <= 5000:
        stat_shapiro, p_shapiro = shapiro(datos_validos)
        print(f"\n📊 Prueba de Shapiro-Wilk:")
        print(f"  • Estadístico: {stat_shapiro:.4f}")
        print(f"  • P-valor: {p_shapiro:.6f}")
        print(f"  • Resultado: {'Normal ✓' if p_shapiro > 0.05 else 'No Normal ✗'} (α=0.05)")
    
    # 2. Prueba de Kolmogorov-Smirnov
    stat_ks, p_ks = kstest(datos_validos, 'norm', args=(datos_validos.mean(), datos_validos.std()))
    print(f"\n📊 Prueba de Kolmogorov-Smirnov:")
    print(f"  • Estadístico: {stat_ks:.4f}")
    print(f"  • P-valor: {p_ks:.6f}")
    print(f"  • Resultado: {'Normal ✓' if p_ks > 0.05 else 'No Normal ✗'} (α=0.05)")
    
    # 3. Prueba de D'Agostino-Pearson
    stat_dagostino, p_dagostino = normaltest(datos_validos)
    print(f"\n📊 Prueba de D'Agostino-Pearson:")
    print(f"  • Estadístico: {stat_dagostino:.4f}")
    print(f"  • P-valor: {p_dagostino:.6f}")
    print(f"  • Resultado: {'Normal ✓' if p_dagostino > 0.05 else 'No Normal ✗'} (α=0.05)")
    
    # 4. Prueba de Anderson-Darling
    resultado_anderson = anderson(datos_validos, dist='norm')
    print(f"\n📊 Prueba de Anderson-Darling:")
    print(f"  • Estadístico: {resultado_anderson.statistic:.4f}")
    print(f"  • Valor crítico (5%): {resultado_anderson.critical_values[2]:.4f}")
    print(f"  • Resultado: {'Normal ✓' if resultado_anderson.statistic < resultado_anderson.critical_values[2] else 'No Normal ✗'}")
    
    # 5. Análisis de Asimetría y Curtosis
    asimetria = skew(datos_validos)
    kurt = kurtosis(datos_validos)
    
    print(f"\n📐 Análisis de Forma:")
    print(f"  • Asimetría (Skewness): {asimetria:.4f}")
    
    if abs(asimetria) < 0.5:
        interpretacion_asimetria = "Simétrica (distribución normal)"
    elif asimetria > 0:
        interpretacion_asimetria = "Asimétrica positiva (cola derecha)"
    else:
        interpretacion_asimetria = "Asimétrica negativa (cola izquierda)"
    print(f"    → {interpretacion_asimetria}")
    
    print(f"\n  • Curtosis (Kurtosis): {kurt:.4f}")
    if abs(kurt) < 0.5:
        interpretacion_curtosis = "Mesocúrtica (normal)"
    elif kurt > 0:
        interpretacion_curtosis = "Leptocúrtica (colas pesadas, picos altos)"
    else:
        interpretacion_curtosis = "Platicúrtica (colas ligeras, picos bajos)"
    print(f"    → {interpretacion_curtosis}")
    
    # 6. Detección de distribuciones alternativas
    print(f"\n🎯 PRUEBAS DE OTRAS DISTRIBUCIONES:")
    
    # Exponencial
    stat_exp, p_exp = kstest(datos_validos, lambda x: stats.expon.cdf(x, scale=datos_validos.std()))
    print(f"\n  • Distribución Exponencial:")
    print(f"    P-valor: {p_exp:.6f} → {'Posible ✓' if p_exp > 0.05 else 'Descartada ✗'}")
    
    # Uniforme
    stat_unif, p_unif = kstest(datos_validos, lambda x: stats.uniform.cdf(x, loc=datos_validos.min(), scale=datos_validos.max()-datos_validos.min()))
    print(f"\n  • Distribución Uniforme:")
    print(f"    P-valor: {p_unif:.6f} → {'Posible ✓' if p_unif > 0.05 else 'Descartada ✗'}")
    
    # Gamma
    alpha_gamma, loc_gamma, scale_gamma = stats.gamma.fit(datos_validos)
    stat_gamma, p_gamma = kstest(datos_validos, lambda x: stats.gamma.cdf(x, alpha_gamma, loc_gamma, scale_gamma))
    print(f"\n  • Distribución Gamma:")
    print(f"    P-valor: {p_gamma:.6f} → {'Posible ✓' if p_gamma > 0.05 else 'Descartada ✗'}")
    
    # Weibull
    try:
        params_weibull = stats.weibull_min.fit(datos_validos)
        stat_weib, p_weib = kstest(datos_validos, lambda x: stats.weibull_min.cdf(x, *params_weibull))
        print(f"\n  • Distribución Weibull:")
        print(f"    P-valor: {p_weib:.6f} → {'Posible ✓' if p_weib > 0.05 else 'Descartada ✗'}")
    except:
        print(f"\n  • Distribución Weibull: No se pudo calcular")
    
    # 7. Resumen y recomendación
    print(f"\n{'='*60}")
    print(f"📋 CONCLUSIÓN:")
    
    pruebas_normalidad = [p_shapiro > 0.05 if len(datos_validos) <= 5000 else None,
                         p_ks > 0.05,
                         p_dagostino > 0.05]
    pruebas_normalidad = [p for p in pruebas_normalidad if p is not None]
    
    normales_count = sum(pruebas_normalidad)
    
    if normales_count >= 2:
        print(f"✓ La variable probablemente sigue una DISTRIBUCIÓN NORMAL")
        print(f"  Puedes usar: pruebas t, ANOVA, regresión lineal")
    else:
        print(f"✗ La variable NO sigue una distribución normal")
        print(f"  Recomendaciones:")
        print(f"  - Usa pruebas no paramétricas (Mann-Whitney, Kruskal-Wallis)")
        print(f"  - Considera transformaciones (log, raíz cuadrada, Box-Cox)")
        print(f"  - O aumenta el tamaño de la muestra si es pequeño")
    
    print(f"{'='*60}\n")

def estadisticas_descriptivas():
    """Calcula estadísticas descriptivas básicas del dataset"""
    print("\n" + "="*60)
    print("ESTADÍSTICAS DESCRIPTIVAS DEL DATASET")
    print("="*60 + "\n")
    
    # Estadísticas generales del dataset
    print("📊 INFORMACIÓN GENERAL DEL DATASET:")
    print(f"Total de registros: {len(datos)}")
    print(f"Total de columnas: {len(datos.columns)}")
    print(f"Columnas: {list(datos.columns)}\n")
    
    # Estadísticas de variables numéricas
    print("📈 ESTADÍSTICAS DE VARIABLES NUMÉRICAS:\n")
    stats_df = datos.describe()
    print(stats_df)
    
    # Análisis específico por columna numérica
    print("\n" + "-"*60)
    print("ANÁLISIS DETALLADO POR VARIABLE:\n")
    
    columnas_numericas = datos.select_dtypes(include=[np.number]).columns
    
    for col in columnas_numericas:
        print(f"📌 {col.upper()}:")
        print(f"  • Media: {datos[col].mean():.2f}")
        print(f"  • Mediana: {datos[col].median():.2f}")
        print(f"  • Moda: {datos[col].mode().values[0] if len(datos[col].mode()) > 0 else 'N/A'}")
        print(f"  • Desviación estándar: {datos[col].std():.2f}")
        print(f"  • Varianza: {datos[col].var():.2f}")
        print(f"  • Mínimo: {datos[col].min():.2f}")
        print(f"  • Máximo: {datos[col].max():.2f}")
        print(f"  • Rango: {datos[col].max() - datos[col].min():.2f}")
        print(f"  • Q1 (25%): {datos[col].quantile(0.25):.2f}")
        print(f"  • Q3 (75%): {datos[col].quantile(0.75):.2f}")
        print(f"  • IQR: {datos[col].quantile(0.75) - datos[col].quantile(0.25):.2f}")
        print(f"  • Asimetría: {datos[col].skew():.2f}")
        print(f"  • Curtosis: {datos[col].kurtosis():.2f}\n")
    
    # NUEVO: Análisis de distribución
    print("\n" + "="*60)
    print("ANÁLISIS DE DISTRIBUCIONES")
    print("="*60)
    
    generar_graficos = input("\n¿Deseas generar gráficos de distribución para todas las variables? (s/n): ").lower()
    
    for col in columnas_numericas:
        analizar_distribucion(datos[col], col)
        if generar_graficos == 's':
            graficar_distribucion(datos[col], col)
    
    # Análisis de variables categóricas
    print("-"*60)
    print("ANÁLISIS DE VARIABLES CATEGÓRICAS:\n")
    
    columnas_categoricas = datos.select_dtypes(include=['object']).columns
    
    for col in columnas_categoricas:
        print(f"📌 {col.upper()}:")
        print(f"  • Valores únicos: {datos[col].nunique()}")
        print(f"  • Más frecuente: {datos[col].mode().values[0]}")
        print(f"  • Frecuencia del más frecuente: {datos[col].value_counts().iloc[0]}")
        print(f"  • Valores faltantes: {datos[col].isna().sum()}\n")
    
    # Correlación entre variables numéricas
    print("-"*60)
    print("MATRIZ DE CORRELACIÓN:\n")
    print(datos.corr(numeric_only=True))
    
    # Valores faltantes
    print("\n" + "-"*60)
    print("VALORES FALTANTES:\n")
    faltantes = datos.isna().sum()
    if faltantes.sum() == 0:
        print("✓ No hay valores faltantes en el dataset")
    else:
        print(faltantes[faltantes > 0])
    
    print("\n" + "="*60 + "\n")
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
        estadisticas_descriptivas()
    elif opcion == "6":
        print("\n" + "="*70)
        print("DETECCIÓN DE OUTLIERS (VALORES EXTERNOS)")
        print("="*70)
        
        columnas_numericas = datos.select_dtypes(include=[np.number]).columns
        
        generar_graficos_outliers = input("\n¿Deseas generar gráficos de outliers? (s/n): ").lower()
        
        for col in columnas_numericas:
            outliers_dict = detectar_outliers(datos[col], col)
            if generar_graficos_outliers == 's':
                graficar_outliers(datos[col], col, outliers_dict)
        
        print("\n💡 RECOMENDACIONES GENERALES:")
        print("-"*70)
        print("• Usa IQR para datos NO normales")
        print("• Usa Z-Score para datos aproximadamente normales")
        print("• Usa Modified Z-Score (MAD) para datos muy sesgados")
        print("• Combina múltiples métodos para validar outliers")
        print("• Antes de eliminar outliers, verifica que sean errores reales")
        print("="*70 + "\n")
        
    elif opcion == "7":
        generar_graficos_representativos()
        
    elif opcion == "8":
        print("\nSaliendo del programa.\n")
        break
    else:
        print("\nOpción no válida. Intenta de nuevo.\n")
################################