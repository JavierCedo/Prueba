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
print('#'*20,"Archivo .json",'#'*20)
print(df_json.info())

# Division de df_json en pequeños df
df1 = df_json[['spl_product_ndc', 'manufacturer_name', 'application_number', 'brand_name_suffix', 'spl_version','route']]
df2 = df_json[['generic_name']]
df3 = df_json[[ 'brand_name', 'upc','spl_set_id', 'product_ndc','original_packager_product_ndc']]
df4 = df_json[['substance_name']]
df5 = df_json[['unii_indexing']]
df6 = df_json[['package_ndc','product_type']]
df7 = df_json[['rxnorm']]
df8 = df_json[['is_original_packager','id','dosage_form']]

df1.columns = ['spl_product_ndc', 'manufacturer_name', 'application_number', 'brand_name_suffix', 'spl_version','route']
df2.columns = ['generic_name']
df3.columns = [ 'brand_name', 'upc','spl_set_id', 'product_ndc','original_packager_product_ndc']
df4.columns = ['substance_name']
df5.columns = ['unii_indexing']
df6.columns = ['package_ndc','product_type']
df7.columns = ['rxnorm']
df8.columns = ['is_original_packager','id','dosage_form']

# Visualizacion de df pequeños
print('df1');print(tabulate(df1.head(5),headers='keys'))
print('df2');print(tabulate(df2.head(5),headers='keys'))
print('df3');print(tabulate(df3.head(5),headers='keys'))
print('df4');print(tabulate(df4.head(5),headers='keys'))
print('df5');print(tabulate(df5.head(5),headers='keys'))
print('df6');print(tabulate(df6.head(5),headers='keys'))
print('df7');print(tabulate(df7.head(5),headers='keys'))
print('df8');print(tabulate(df8.head(5),headers='keys'))

# Funciones
def separar_columna_en_columnas(serie, delimitadores=None):
    if delimitadores:
        delimitador_regex = '|'.join(map(re.escape, delimitadores))
        nuevas_columnas = df_json[serie].str.split(delimitador_regex, expand=True)
        value_counts = nuevas_columnas.apply(pd.Series.value_counts).sum(axis=1).astype(int)
        value_counts = value_counts[value_counts.index.notna()]
        value_counts = value_counts.drop('', errors='ignore')
        for i,j in value_counts.items():
            print(i,j)
    else:
        value_counts = df_json[serie].value_counts().astype(int)
        for i,j in value_counts.items():
            print(i,j)
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

# Pruebas de separacion y graficas

print('manufacturer_name', '#'*60)
print(grafica_top_10(separar_columna_en_columnas('manufacturer_name'),'manufacturer_name'))

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



'''
# Ya revisado (df en los que funcionana bien las graficas , y no hace falta modificarlos)

df1; route
df8, dosage_form

# Por revisar (df en los que NO funcionana bien las graficas , y hace falta modificarlos)

df1; manufacturer_name,   limpiar bien                     ','.'LLc'INC'Inc'Todo en mayusculas'()'numeros'& por and' '
df2; generic_name,        Separar bien, limpiar bien,      ', 'Todo en mayusculas'    
df3; brand_name,          Separar bien, limpiar bien,      'Todo en mayusculas' '
df4; substance_name,      Separar bien, limpiar bien,      'numeros'.'
'''


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
