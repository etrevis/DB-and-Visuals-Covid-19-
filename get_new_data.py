import pandas as pd
import requests as req
import os

file = req.get('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province.json')
file_1 = req.get('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json')
file_2 = req.get('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni.json')

df = pd.read_json(file.content)
df_1 = pd.read_json(file_1.content)
df_2 = pd.read_json(file_2.content)

df.to_csv(os.path.join('Data', 'dpc-covid19-ita-province.csv'), sep=',', index='False')
df_1.to_csv(os.path.join('Data', 'dpc-covid19-ita-andamento-nazionale.csv'), sep=',', index='False')
df_2.to_csv(os.path.join('Data', 'dpc-covid19-ita-regioni.csv'), sep=',', index='False')
