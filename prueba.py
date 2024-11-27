
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

# Funciones

def transformar_texto(serie): 
    df_json[serie] = df_json[serie].str.upper().str.replace(r'[.,;:]', '', regex=True).str.replace(r' INC ', '', regex=True).str.replace(r' INC', '', regex=True)
    return df_json[serie]

# Asi se tiene que buscar la funcion
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

def grafica_top_10(serie, titulo): 
    top_10 = serie.nlargest(10) 
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

## Pruebas de separacion y graficas
print('manufacturer_name', '#'*60)
print(grafica_top_10(conteo_de_elementos(df_json['manufacturer_name']),'Nombre de la grafica'))

print('route', '#'*60)
delimitadores = ['; ']
print(grafica_top_10(conteo_de_elementos(df_json['route'],delimitadores), 'route'))

print('generic_name', '#'*60)
delimitadores = [', ', ' - ', ' and ', 'and ', ',', ' AND ','AND ' , '-']
print(grafica_top_10(conteo_de_elementos(df_json['generic_name'],delimitadores),'generic_name'))

print('brand_name', '#'*60)
delimitadores = [' and ', ' AND ', ' - ']
print(grafica_top_10(conteo_de_elementos(df_json['brand_name'],delimitadores),'brand_name'))

print('substance_name', '#'*60)
delimitadores = ['; ']
print(grafica_top_10(conteo_de_elementos(df_json['substance_name'],delimitadores),'substance_name'))

print('dosage_form', '#'*60)
delimitadores = [', ','/','/ ',' / ']
print(grafica_top_10(conteo_de_elementos(df_json['dosage_form'],delimitadores),'dosage_form'))


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

    # Renombrar las nuevas columnas para mejor visualización
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
        #print('Esta en', nom_farm)
        farm_esta_med[nom_farm] = f'Esta el medicamento {med}'
        df_bus_new = df_bus_new.loc[med]
        value_counts = df_bus_new.apply(pd.Series.value_counts).sum(axis=1).astype(int).index.tolist()
        #print(value_counts)
        farm_y_comp[nom_farm] = value_counts
    else:
        farm_no_med[nom_farm] = f'No esta el medicamento {med}'

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


print("Medicamento a buscar:", med)
print("En que farmacia esta:")
df_farm_esta_med = pd.DataFrame(list(farm_esta_med.items()), columns=['Farmacia', 'Estado'])
df_farm_esta_med = df_farm_esta_med.set_index('Farmacia')
print(df_farm_esta_med)
print("Componentes por farmacia:")
df_farm_y_comp = pd.DataFrame(list(farm_y_comp.items()), columns=['Farmacia', 'Estado'])
df_farm_y_comp = df_farm_y_comp.set_index('Farmacia')
print(df_farm_y_comp)
print("En que farmacia no esta:")
df_farm_no_med = pd.DataFrame(list(farm_no_med.items()), columns=['Farmacia', 'Estado'])
df_farm_no_med = df_farm_no_med.set_index('Farmacia')
print(df_farm_no_med)
print("Farmacia donde esta un medicamento similar:")
df_far_med_sml = pd.DataFrame(list(far_med_sml.items()), columns=['Farmacia', 'Estado'])
df_far_med_sml = df_far_med_sml.set_index('Farmacia')
print(df_far_med_sml)
