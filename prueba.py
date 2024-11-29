import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
import seaborn as sns
from IPython import get_ipython
from IPython.display import display
import patoolib
import os
import re

# Extraer archivo RAR automaticamente
os.makedirs("carpeta_de_extraccion", exist_ok=True) 
patoolib.extract_archive("prueba.rar", outdir="carpeta_de_extraccion")

# Leer el archivo JSON en un DataFrame de pandas
df_json = pd.read_json('carpeta_de_extraccion/prueba/harmonized.json', lines=True) 


#################### Graficas y analicis de datos ####################


def transformar_texto(serie): 
    df_json[serie] = df_json[serie].str.upper().str.replace(r'[.,;:]', '', regex=True).str.replace(r' INC ', '', regex=True).str.replace(r' INC', '', regex=True)
    return df_json[serie]

def eliminar_numeros(serie): 
    df_json[serie] = df_json[serie].str.upper().str.replace(r'[0123456789]', '', regex=True)
    df_json[serie] = df_json[serie].replace(r'^\s*$', pd.NA, regex=True)
    df_json[serie] = df_json[serie].dropna()
    return df_json[serie]

eliminar_numeros('application_number')
transformar_texto('generic_name')               #Arreglar
transformar_texto('manufacturer_name')
transformar_texto('dosage_form')

def conteo_de_elementos(serie, delimitadores=None):
    if delimitadores:
        delimitador_regex = '|'.join(map(re.escape, delimitadores))
        nuevas_columnas = serie.str.split(delimitador_regex, expand=True)
        value_counts = nuevas_columnas.apply(pd.Series.value_counts).sum(axis=1).astype(int)
        value_counts = value_counts[value_counts.index.notna()]
        value_counts = value_counts.drop('', errors='ignore')
    else:
        value_counts = serie.value_counts().astype(int)
    return value_counts

def grafica_top_10_barras(serie, titulo): 
    top_10 = serie.dropna().nlargest(10)
    sns.set(style="whitegrid")
    plt.figure(figsize=(14, 6))
    ax = sns.barplot(x=top_10.values, y=top_10.index, palette="viridis") 
    ax.set_title(f'top 10 {titulo}', fontsize=15, pad=20) 
    ax.set_xlabel('Cantidad', fontsize=12) 
    ax.set_ylabel('')
    for i, (value, name) in enumerate(zip(top_10.values, top_10.index)): 
        ax.text(value, i, f' {value}', color='black', va='center')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def grafica_comparativa(serie, titulo):
    sns.set(style="whitegrid")
    plt.figure(figsize=(14, 6))
    ax = sns.barplot(x=serie.values, y=serie.index, palette="viridis")
    ax.set_title(f'Comparación de Series Combinadas - {titulo}', fontsize=15, pad=20)
    ax.set_xlabel('Valores', fontsize=12)
    ax.set_ylabel('Índices Combinados', fontsize=12)
    for i, (value, name) in enumerate(zip(serie.values, serie.index)):
        ax.text(value, i, f' {int(value)}', color='black', va='center')
    plt.tight_layout()
    plt.show()

def grafica_top_10_histograma(serie, titulo): 
    top_10 = serie.nlargest(10)
    sns.set(style="whitegrid") 
    plt.figure(figsize=(14, 8)) 
    colors = sns.color_palette("viridis", len(top_10)) 
    ax = plt.gca() 
    for i, (value, name) in enumerate(zip(top_10.values, top_10.index)): 
        ax.bar(name, value, color=colors[i]) 
        ax.text(i, value, f'{value}', ha='center', color='black')
    ax.set_title(f'Top 10 {titulo}', fontsize=15, pad=20) 
    ax.set_xlabel('Elementos', fontsize=12) 
    ax.set_ylabel('Frecuencia', fontsize=12) 
    plt.xticks(rotation=45) 
    plt.tight_layout() 
    plt.show()

def grafica_top_10_pastel(serie, titulo): 
    serie = serie.dropna()
    top_10 = serie.nlargest(10)
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 10))
    if len(top_10) == 2:
        colors = ['#482173', '#c2df23']
    else:
        colors = sns.color_palette("viridis", len(top_10))
    plt.pie(top_10.values, labels=top_10.index, autopct='%1.1f%%', startangle=140, colors=colors)
    plt.title(f'Top 10 {titulo}', fontsize=15, pad=20)
    plt.axis('equal')
    plt.show()

def combinar_series(serie1, serie2):
    serie1 = serie1.value_counts().nlargest(10)
    serie2 = serie2.value_counts().nlargest(10)
    serie_combinada = pd.concat([serie1, serie2], axis=1, keys=['Serie 1', 'Serie 2']).fillna(0)
    serie_combinada['Combinada'] = serie_combinada['Serie 1'] + serie_combinada['Serie 2']
    serie_final = serie_combinada['Combinada']
    return serie_final


grafica_top_10_histograma(conteo_de_elementos(df_json['application_number']),'application_number')

serie_combinada = combinar_series(df_json['dosage_form'], df_json['product_type'])
grafica_comparativa(serie_combinada, 'Gráfica Comparativa de Series Combinadas')

delimitadores = [', ','/','/ ',' / ']
grafica_top_10_histograma(conteo_de_elementos(df_json['dosage_form'],delimitadores),'dosage_form')

grafica_top_10_barras(conteo_de_elementos(df_json['manufacturer_name']),'Grafica de barras')

grafica_top_10_pastel(conteo_de_elementos(df_json["product_type"]), 'Grafica de histograma')

grafica_top_10_pastel(conteo_de_elementos(df_json['is_original_packager']),'is_original_packager')

delimitadores = ['; ']
grafica_top_10_barras(conteo_de_elementos(df_json['substance_name'], delimitadores),'Grafica de barras')

delimitadores = ['; ']
grafica_top_10_histograma(conteo_de_elementos(df_json['route'],delimitadores), 'route')

delimitadores = [', ', ' - ', ' and ', 'and ', ',', ' AND ','AND ' , '-']
grafica_top_10_pastel(conteo_de_elementos(df_json['generic_name'],delimitadores),'generic_name')


#################### Busqueda de medicamento ####################


df_bus = df_json[['brand_name', 'substance_name']]
df_bus.columns = ['brand_name', 'substance_name']
df_bus = df_bus.drop_duplicates()

def separar_componentes(serie, delimitadores=None):
    if delimitadores:
        delimitador_regex = ' '.join(map(re.escape, delimitadores))
        df_bus_new = serie.str.split(delimitador_regex, expand=True)
    else:
        df_bus_new = serie.str.split(expand=True)
    df_bus_new.columns = [f'Componente_{i+1}' for i in range(df_bus_new.shape[1])]
    return df_bus_new

# Aplicar la función a la columna substance_name
df_bus_new = separar_componentes(df_bus['substance_name'], ['; '])
df_bus_new['brand_name'] = df_bus['brand_name']
df_bus_new = df_bus_new.set_index('brand_name')

### Farmacias Ficticias

df1 = df_bus_new.sample(n=len(df_bus_new)//3, replace=True)
df2 = df_bus_new.sample(n=len(df_bus_new)//3, replace=True)
df3 = df_bus_new.sample(n=len(df_bus_new)//3, replace=True)

list_farms = {'Farmacia1':df1, 'Farmacia2':df2, 'Farmacia3':df3}

# Medicamento a buscar
med = "Clean Force"

# Almacenar datos de los resultados de búsqueda
farm_esta_med = {}
farm_y_comp = {}
farm_no_med = {}
far_med_sml = {}

# Verificar la presencia del medicamento, obtener los componentes y saber en que farmacia no esta
for nom_farm, df_farm in list_farms.items():
    if med in df_farm.index:
        farm_esta_med[nom_farm] = f'Esta el medicamento {med}'
        df_bus_new = df_bus_new.loc[med]
        value_counts = df_bus_new.apply(pd.Series.value_counts).sum(axis=1).astype(int).index.tolist()
        farm_y_comp[nom_farm] = value_counts
    else:
        farm_no_med[nom_farm] = f'No esta el medicamento {med}'

if not farm_esta_med:
    farm_esta_med[nom_farm] = f'No asta el medicamento {med}'
    farm_y_comp[nom_farm] = f'Esta el medicamento {med}'

# Verificar en la farmacia que no se encontro si existe uno similar
if farm_esta_med:
    indices_lista = []
    def encontrar_primera_lista():
        for nombre, df in list_farms.items():
            for nom_far_no in farm_no_med:
                for nom_far, lista in farm_y_comp.items():
                    for i in lista:
                        indices = df.apply(lambda row: row == i, axis=1).any(axis=1)
                        indices_lista = df[indices].index.tolist()[:5]  # Guardar solo los primeros 5 resultados
                        if indices_lista:
                            far_med_sml[nom_far_no] = indices_lista
                            yield indices_lista  # Usar yield para retornar la lista y salir del generador
    indices_lista = next(encontrar_primera_lista(), [])
elif not farm_esta_med:
    print('No se encontro para comparar')

if not farm_no_med:
    farm_no_med[nom_farm] = f'Se encontro en todas las farmacias {med}'
    far_med_sml[nom_farm] = f'Se encontro en todas las farmacias {med}'

## Salida
def print_df_with_title(title, df_dict):
    df = pd.DataFrame(list(df_dict.items()), columns=['Farmacia', 'Estado'])
    print("-"*60)
    print(title)
    print(df.to_string(index=False, header=False))
    
print("Medicamento a buscar:", med)
print_df_with_title("En qua farmacia esta:", farm_esta_med)
print_df_with_title("Componentes por farmacia:", farm_y_comp)
print_df_with_title("En qua farmacia no esta:", farm_no_med)
print_df_with_title("Farmacia donde esta un medicamento similar:", far_med_sml)
