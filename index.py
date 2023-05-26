import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

# Ler o arquivo de dados
arquivo = 'brazil_covid19.csv'
colunas_desejadas = ['region', 'date', 'deaths', 'state']
df = pd.read_csv(arquivo)

# Selecionar as colunas desejadas
df = df[colunas_desejadas]

# Remover linhas com valores ausentes
df = df.dropna()

# Converter a coluna 'date' para o formato de data
df['date'] = pd.to_datetime(df['date'])

# Filtrar os dados do ano de 2020
df = df[df['date'].dt.year == 2020]

# Selecionar o último registro de óbitos por estado
df_last_deaths = df.groupby('state').apply(lambda x: x.loc[x['date'].idxmax()])

# Calcular a soma de óbitos por região
df_sum_region = df_last_deaths.groupby('region')['deaths'].sum().reset_index()

# Calcular a soma total de óbitos por região
df_total_sum = df_sum_region.groupby('region')['deaths'].sum().reset_index()

# Plotar o gráfico de barras
plt.figure(figsize=(10, 6))
plt.bar(df_total_sum['region'], df_total_sum['deaths'])
plt.title('Covid-19 2020 - Total de Óbitos por Região')
plt.xticks(rotation=45)

# Adicionar rótulos aos valores das barras
for i, valor in enumerate(df_total_sum['deaths']):
    plt.text(i, valor, str(valor), ha='center', va='bottom')

plt.show()

# Ler o arquivo geojson
arquivo_geojson = 'grandes_regioes_json.geojson'
dados_geograficos = gpd.read_file(arquivo_geojson)

# Mesclar dados geográficos com dados de óbitos por região
dados_completos = dados_geograficos.merge(df_total_sum, left_on='NOME1', right_on='region')

# Plotar o mapa choropleth
fig, ax = plt.subplots(figsize=(12, 8))
dados_completos.plot(column='deaths', cmap='Reds', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
plt.title('Covid-19 2020 - Óbitos no Brasil por Regiões')
plt.show()

# Calcular a soma de óbitos por mês
df['date'] = pd.to_datetime(df['date'])
df['mes'] = df['date'].dt.month
df['ultimo_dia_mes'] = df['date'].dt.is_month_end

df_ultimo_dia = df[df['ultimo_dia_mes']].groupby('mes')['deaths'].sum().reset_index()

meses = list(range(1, 13))

# Mesclar dados de óbitos por mês com todos os meses
df_soma_brasil = df_ultimo_dia.merge(pd.DataFrame({'mes': meses}), on='mes', how='right').fillna(0)
df_soma_brasil = df_soma_brasil.sort_values('mes')

# Plotar o gráfico de linha
plt.plot(df_soma_brasil['mes'], df_soma_brasil['deaths'], marker='o')

# Adicionar rótulos aos pontos do gráfico
for x, y in zip(df_soma_brasil['mes'], df_soma_brasil['deaths']):
    plt.text(x, y, str(int(y)), ha='center', va='bottom')

plt.title('Covid-19 2020 - Óbitos no Brasil')
plt.xlabel('Mês')
plt.xticks(meses)

plt.show()