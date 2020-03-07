import pandas as pd
import requests as req
import os

file = req.get('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province.json')

df = pd.read_json(file.content)

df.to_csv(os.path.join('Data', 'dpc-covid19-ita-province.csv'), sep=',', index='False')
