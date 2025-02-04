
#%%
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
#%%
# Carregar os dados CSV
df_roubos_raw = pd.read_csv(
    r"C:\Users\Vivian - H2R\Downloads\mba\git\mba_arrumado\dados_tratados\dados_tratados\df_drogas_24_recort.csv",
    dtype={0: str}
)

# Filtrar os dados pelo mês desejado
meses = [1,2,3,4,5,6,7,8,9,10,11,12]
df_roubos = df_roubos_raw[df_roubos_raw['MES_ESTATI'].isin(meses)]

# Selecionar apenas as colunas necessárias
df_roubos = df_roubos[['LATITUDE', 'LONGITUDE']]

# Verificar se as colunas de latitude e longitude existem no DataFrame
if not {'LATITUDE', 'LONGITUDE'}.issubset(df_roubos.columns):
    raise KeyError("As colunas 'LATITUDE' e/ou 'LONGITUDE' não foram encontradas no DataFrame.")

# Converter colunas de latitude e longitude para numérico, tratando erros
df_roubos['LATITUDE'] = pd.to_numeric(df_roubos['LATITUDE'], errors='coerce')
df_roubos['LONGITUDE'] = pd.to_numeric(df_roubos['LONGITUDE'], errors='coerce')

# Remover linhas com valores inválidos (NaN)
df_roubos = df_roubos.dropna(subset=['LATITUDE', 'LONGITUDE'])

# Criar geometria dos pontos
geometry = [Point(xy) for xy in zip(df_roubos.LONGITUDE, df_roubos.LATITUDE)]
df_roubos = gpd.GeoDataFrame(df_roubos, geometry=geometry, crs="EPSG:4326")

# Reprojetar para UTM Zona 23S (EPSG:31983)
utm_crs = "EPSG:31983"
df_roubos = df_roubos.to_crs(utm_crs)

# Salvar como shapefile
output_path = "C:/Users/Vivian - H2R/Downloads/mba/git/mba_arrumado/h3df_drogas_h3.shp"
df_roubos.to_file(output_path, driver="ESRI Shapefile")

print(f"Arquivo shapefile salvo em: {output_path}")
