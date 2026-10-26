# Importação das bibliotecas necessárias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt   

# Definição do caminho dos dados
caminho_dados = "BaseVarejoDadosBrutos.csv"

# Leitura dos dados com a utilização dos parâmetros abaixo:
# dtype - para que as colunas que devem ser do tipo string, não sejam lidas como do tipo inteiro
# parse_dates - para instruir o pandas a interpretar a coluna DATA como data/datetime
# na_values - para definir que o valor "#N/D" seja tratado como valor ausente (NaN).
# keep_default_na=True - para que além de "#N/D", outros valores padrão, reconhecidos como ausentes, também sejam convertidos para NaN
df = pd.read_csv(caminho_dados, sep= ";", dtype= {"CO_ID": "string", 
                                                  "CL_ID": "string", 
                                                  "PR_ID": "string"},
                                                  parse_dates=["DATA"],na_values=["#N/D"], keep_default_na=True)
