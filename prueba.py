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

# Asi se tiene que buscar la funcion    transformar_texto
transformar_texto('manufacturer_name')
transformar_texto('generic_name')               #Arreglar
transformar_texto('manufacturer_name')
transformar_texto('brand_name')                 #Arreglar
transformar_texto('substance_name')             #Arreglar
transformar_texto('dosage_form')



def separar_columna_en_columnas(serie, delimitadores=None):
    if delimitadores:
        delimitador_regex = '|'.join(map(re.escape, delimitadores))
        nuevas_columnas = df_json[serie].str.split(delimitador_regex, expand=True)
        value_counts = nuevas_columnas.apply(pd.Series.value_counts).sum(axis=1).astype(int)
        value_counts = value_counts[value_counts.index.notna()]
        value_counts = value_counts.drop('', errors='ignore')
        for i, j in value_counts.items():
            print(i,j)
    else:
        value_counts = df_json[serie].value_counts().astype(int)
        for i, j in value_counts.items():
            print(i,j)
    return value_counts.head(50)

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
print(grafica_top_10(separar_columna_en_columnas('manufacturer_name'),'Nombre de la grafica'))

print('route', '#'*60)
delimitadores = ['; ']
print(grafica_top_10(separar_columna_en_columnas('route',delimitadores), 'route'))

print('generic_name', '#'*60)
delimitadores = [', ', ' - ', ' and ', 'and ', ',', ' AND ','AND ' , '-']
print(grafica_top_10(separar_columna_en_columnas('generic_name',delimitadores),'generic_name'))

print('brand_name', '#'*60)
delimitadores = [' and ', ' AND ', ' - ']
print(grafica_top_10(separar_columna_en_columnas('brand_name',delimitadores),'brand_name'))

print('substance_name', '#'*60)
delimitadores = ['; ']
print(grafica_top_10(separar_columna_en_columnas('substance_name',delimitadores),'substance_name'))

print('dosage_form', '#'*60)
delimitadores = [', ','/','/ ',' / ']
print(grafica_top_10(separar_columna_en_columnas('dosage_form',delimitadores),'dosage_form'))




''' ## Ideas pendientes

# Leer el archivo de texto en un DataFrame de pandas
df_txt = pd.read_csv('prueba\\Products.txt', sep='\t', on_bad_lines='skip')
print('#'*20,"Archivo .txt",'#'*20)
print(df_txt.info())
df1 = df_txt[['ApplNo','ProductNo','Form','Strength','ReferenceDrug', 'DrugName']]
df2 = df_txt[['ActiveIngredient','ReferenceStandard']]
print('df1');print(tabulate(df1.head(5),headers='keys'))
print('df2');print(tabulate(df2.head(5),headers='keys'))
'''
