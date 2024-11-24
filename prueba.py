import pandas as pd
from tabulate import tabulate

# Leer el archivo de texto en un DataFrame de pandas
df_txt = pd.read_csv('prueba\\Products.txt', sep='\t', on_bad_lines='skip')
print('#'*20,"Archivo .txt",'#'*20)
print(df_txt.info())
df1 = df_txt[['ApplNo','ProductNo','Form','Strength','ReferenceDrug', 'DrugName']]
df2 = df_txt[['ActiveIngredient','ReferenceStandard']]
print('df1');print(tabulate(df1.head(5),headers='keys'))
print('df2');print(tabulate(df2.head(5),headers='keys'))



# Leer el archivo JSON en un DataFrame de pandas
df_json = pd.read_json('prueba\\harmonized.json', lines=True)
print('#'*20,"Archivo .json",'#'*20)
print(df_json.info())

df1 = df_json[['spl_product_ndc', 'manufacturer_name', 'application_number', 'brand_name_suffix', 'spl_version','route']]
df1.columns = ['spl_product_ndc', 'manufacturer_name', 'application_number', 'brand_name_suffix', 'spl_version','route']
df2 = df_json[['generic_name']]
df2.columns = ['generic_name']
df3 = df_json[[ 'brand_name', 'upc','spl_set_id', 'product_ndc','original_packager_product_ndc']]
df3.columns = [ 'brand_name', 'upc','spl_set_id', 'product_ndc','original_packager_product_ndc']
df4 = df_json[['substance_name']]
df4.columns = ['substance_name']
df5 = df_json[['unii_indexing']]
df5.columns = ['unii_indexing']
df6 = df_json[['package_ndc','product_type']]
df6.columns = ['package_ndc','product_type']
df7 = df_json[['rxnorm']]
df7.columns = ['rxnorm']
df8 = df_json[['is_original_packager','id','dosage_form']]
df8.columns = ['is_original_packager','id','dosage_form']
print('df1');print(tabulate(df1.head(5),headers='keys'))
print('df2');print(tabulate(df2.head(5),headers='keys'))
print('df3');print(tabulate(df3.head(5),headers='keys'))
print('df4');print(tabulate(df4.head(5),headers='keys'))
print('df5');print(tabulate(df5.head(5),headers='keys'))
print('df6');print(tabulate(df6.head(5),headers='keys'))
print('df7');print(tabulate(df7.head(5),headers='keys'))
print('df8');print(tabulate(df8.head(5),headers='keys'))
