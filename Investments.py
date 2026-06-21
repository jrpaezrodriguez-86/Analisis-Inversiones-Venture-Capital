import pandas as pd
import matplotlib.pyplot as plt

# 1. CARGA DE DATOS
print("Cargando el dataset de Venture Capital...")
df = pd.read_csv('investments_VC.csv')

# 2. LIMPIEZA DE DATOS AVANZADA
# Limpiamos los espacios en blanco ocultos en los nombres de las columnas
df.columns = df.columns.str.strip()

# Aseguramos que los textos de la columna de mercado no tengan espacios extra
df['market'] = df['market'].str.strip()

# Limpiamos la columna de dinero: quitamos comas, espacios y convertimos a número
df['funding_total_usd'] = df['funding_total_usd'].str.replace(',', '').str.strip()
df['funding_total_usd'] = pd.to_numeric(df['funding_total_usd'], errors='coerce')

# Eliminamos filas que se quedaron sin datos válidos tras la limpieza
df = df.dropna(subset=['funding_total_usd', 'market'])
df = df[df['funding_total_usd'] > 0]

# 3. PROCESAMIENTO Y AGRUPACIÓN (Métricas clave)
# Agrupamos por sector económico para calcular Totales, Promedios y Cantidad de empresas
analisis_sectores = df.groupby('market').agg(
    Total_USD=('funding_total_usd', 'sum'),
    Promedio_USD=('funding_total_usd', 'mean'),
    Cantidad_Empresas=('funding_total_usd', 'count')
).reset_index()

# Seleccionamos los 5 sectores con mayor financiamiento acumulado en el mundo
top_5_financiamiento = analisis_sectores.sort_values(by='Total_USD', ascending=False).head(5).copy()

# Convertimos los totales a "Mil Millones de USD" (Billions) para que el gráfico sea legible
top_5_financiamiento['Total_Billions'] = top_5_financiamiento['Total_USD'] / 1e9

print("\n--- TOP 5 SECTORES CON MAYOR FINANCIAMIENTO ---")
print(top_5_financiamiento[['market', 'Total_Billions', 'Cantidad_Empresas', 'Promedio_USD']])

# 4. CREACIÓN DEL GRÁFICO (Gráfico de Barras Horizontales)
print("\nGenerando gráfico de barras horizontales...")
plt.figure(figsize=(10, 6))

# Usamos un color verde esmeralda muy corporativo
barras = plt.barh(top_5_financiamiento['market'], 
                  top_5_financiamiento['Total_Billions'], 
                  color='#2ecc71', edgecolor='black', alpha=0.8)

# Invertimos el eje vertical para que el sector #1 aparezca arriba del todo
plt.gca().invert_yaxis()

# Añadimos los valores en texto al final de cada barra
for barra in barras:
    ancho_barra = barra.get_width()
    plt.text(ancho_barra + 1, barra.get_y() + barra.get_height()/2, 
             f"${ancho_barra:.1f}B", 
             va='center', ha='left', fontsize=11, weight='bold', color='#2c3e50')

# Personalización del gráfico
plt.title('¿Dónde se invierte el Capital de Riesgo?\nTop 5 Sectores con Mayor Financiamiento Acumulado Global', fontsize=14, weight='bold', pad=20)
plt.xlabel('Financiamiento Total (En Miles de Millones de USD - Billions)', fontsize=11, labelpad=10)
plt.ylabel('Sector de Mercado', fontsize=11, labelpad=10)
plt.xlim(0, 75) # Damos margen a la derecha para que quepan los textos
plt.grid(axis='x', linestyle='--', alpha=0.5)

plt.tight_layout()
# Guardamos la imagen para el portafolio
plt.savefig('top_sectores_inversion.png', dpi=300)
print("¡Gráfico guardado con éxito como 'top_sectores_inversion.png'!")