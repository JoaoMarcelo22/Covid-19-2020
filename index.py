import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

arquivo = 'brazil_covid19.csv'
colunas_desejadas = ['region', 'date', 'deaths', 'state']
df = pd.read_csv(arquivo)

df = df[colunas_desejadas]

df = df.dropna()

df['date'] = pd.to_datetime(df['date'])

df = df[df['date'].dt.year == 2020]

df_last_deaths = df.groupby('state').apply(lambda x: x.loc[x['date'].idxmax()])

df_sum_region = df_last_deaths.groupby('region')['deaths'].sum().reset_index()


df_total_sum = df_sum_region.groupby('region')['deaths'].sum().reset_index()

plt.figure(figsize=(10, 6))
plt.bar(df_total_sum['region'], df_total_sum['deaths'])
plt.xlabel('Região')
plt.title('Covid-19 2020 - Total de Óbitos por Região')
plt.xticks(rotation=45)

for i, valor in enumerate(df_total_sum['deaths']):
    plt.text(i, valor, str(valor), ha='center', va='bottom')

plt.show()

arquivo_geojson = 'grandes_regioes_json.geojson'
dados_geograficos = gpd.read_file(arquivo_geojson)

dados_completos = dados_geograficos.merge(df_total_sum, left_on='NOME1', right_on='region')
fig, ax = plt.subplots(figsize=(12, 8))
dados_completos.plot(column='deaths', cmap='Reds', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
plt.title('Quantidade de Novos Óbitos por Região')
plt.show()

df['date'] = pd.to_datetime(df['date'])
df['mes'] = df['date'].dt.month
df['ultimo_dia_mes'] = df['date'].dt.is_month_end

df_ultimo_dia = df[df['ultimo_dia_mes']].groupby('mes')['deaths'].sum().reset_index()

meses = list(range(1, 13))

df_soma_brasil = df_ultimo_dia.merge(pd.DataFrame({'mes': meses}), on='mes', how='right').fillna(0)
df_soma_brasil = df_soma_brasil.sort_values('mes')

plt.plot(df_soma_brasil['mes'], df_soma_brasil['deaths'], marker='o')

for x, y in zip(df_soma_brasil['mes'], df_soma_brasil['deaths']):
    plt.text(x, y, str(int(y)), ha='center', va='bottom')

plt.title('Covid-19 2020 - Óbitos no Último Dia de Cada Mês (Brasil)')
plt.xlabel('Mês')
plt.xticks(meses)

plt.show()
