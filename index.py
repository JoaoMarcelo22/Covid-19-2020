import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd


arquivo = 'brazil_covid19.csv'
colunas_desejadas = ['region', 'date', 'deaths', 'state']
df = pd.read_csv(arquivo, delimiter=',', encoding='latin-1', error_bad_lines=False)

df = df[colunas_desejadas]

df = df.dropna()

df['date'] = pd.to_datetime(df['date'])

df = df[df['date'].dt.year <= 2020]

df['mes'] = df['date'].dt.month

df_obitos = df[df['deaths'] != 0]

df_soma_obitos = df_obitos.groupby(['region', 'mes'])['deaths'].sum().reset_index(name='total_obitos')
df_soma_regiao = df_soma_obitos.groupby('region')['total_obitos'].sum().reset_index()

plt.figure(figsize=(10, 6))
plt.bar(df_soma_regiao['region'], df_soma_regiao['total_obitos'])
plt.xlabel('Região')
plt.title('Covi-19 2020 - Total de Óbitos por Região')
plt.xticks(rotation=45)

for i, valor in enumerate(df_soma_regiao['total_obitos']):
    plt.text(i, valor, str(valor), ha='center', va='bottom')

plt.show()

df_soma_brasil = df_soma_obitos.groupby('mes')['total_obitos'].sum().reset_index()
meses = list(range(1, 13))
df_soma_brasil = df_soma_brasil.merge(pd.DataFrame({'mes': meses}), on='mes', how='right').fillna(0)
df_soma_brasil = df_soma_brasil.sort_values('mes')
plt.plot(df_soma_brasil['mes'], df_soma_brasil['total_obitos'], marker='o')

for x, y in zip(df_soma_brasil['mes'], df_soma_brasil['total_obitos']):
    plt.text(x, y, str(int(y)), ha='center', va='bottom')

plt.title('Covid-19 2020 - Óbitos por Mês (Brasil)')

plt.xlabel('Mês')

plt.xticks(meses)

plt.show()

arquivo_geojson = 'grandes_regioes_json.geojson'
dados_geograficos = gpd.read_file(arquivo_geojson)

dados_completos = dados_geograficos.merge(df_soma_obitos, left_on='NOME1', right_on='region')
fig, ax = plt.subplots(figsize=(12, 8))
dados_completos.plot(column='total_obitos', cmap='Reds', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
plt.title('Quantidade de Novos Óbitos por Região')
plt.show()