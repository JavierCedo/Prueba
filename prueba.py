import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
import seaborn as sns

# Leer el archivo JSON en un DataFrame de pandas
df_json = pd.read_json('prueba\\harmonized.json', lines=True)

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

print('df1');print(tabulate(df1.head(5),headers='keys'))
print('df2');print(tabulate(df2.head(5),headers='keys'))
print('df3');print(tabulate(df3.head(5),headers='keys'))
print('df4');print(tabulate(df4.head(5),headers='keys'))
print('df5');print(tabulate(df5.head(5),headers='keys'))
print('df6');print(tabulate(df6.head(5),headers='keys'))
print('df7');print(tabulate(df7.head(5),headers='keys'))
print('df8');print(tabulate(df8.head(5),headers='keys'))


def separar_columna_en_columnas(serie):   # Arreglar los puntos y comas para que aparescan mas parecidos
    df1 = df_json[[serie]]
    nuevas_columnas = df_json[serie].str.split('; ', expand=True)
    value_counts = nuevas_columnas.apply(pd.Series.value_counts).sum(axis=1).astype(int)
    value_counts = value_counts[value_counts.index.notna()]
    value_counts = value_counts.drop('', errors='ignore')
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

print(grafica_top_10(separar_columna_en_columnas('manufacturer_name'),'manufacturer_name'))
print(grafica_top_10(separar_columna_en_columnas('route'), 'route'))
print(grafica_top_10(separar_columna_en_columnas('generic_name'),'generic_name'))
print(grafica_top_10(separar_columna_en_columnas('brand_name'),'brand_name'))
print(grafica_top_10(separar_columna_en_columnas('substance_name'),'substance_name'))



'''
# Lo que se tiene ya revisado
df1; manufacturer_name, route
df2; generic_name, separarlos y ver cuales son los mas comunes.

# Por revisar
df3; brand_name, ver si se repiten
df4; substance_name, principal activo ,separar las sustancias y ver cuales son las mas usadas
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
