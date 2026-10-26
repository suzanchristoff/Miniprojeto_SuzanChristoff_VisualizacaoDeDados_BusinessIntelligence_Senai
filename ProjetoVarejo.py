# Importação das bibliotecas necessárias
import pandas as pd
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

# Exibição da lista com os nomes de todas as colunas, para analisar os nomes e possíveis inconsistências
#print("Nome das colunas:" , df.columns.tolist())

# Exibição das 3 primeiras linhas do dataframe
df.head(3)

# Verificação do tamanho do conjunto de dados
#print("Total de linhas:", df.shape[0])
#print("Total de colunas:", df.shape[1])

# Inspeção dos tipos dos dados de cada coluna e nulos presentes em cada uma delas
#df.info()

# Conversão do tipo da coluna DATA de string para datetime
#print("Tipo da coluna DATA antes da transformação:" , df["DATA"].dtype)
df["DATA"] = pd.to_datetime(df["DATA"], format = "%d/%m/%Y")
#print("Tipo da coluna DATA após a transformação:" , df["DATA"].dtype)

# Identificação da data inicial e final do registro dos dados
#print("Período compreendido entre:")
#print(df["DATA"].min().strftime("%d/%m/%Y"), "e", df["DATA"].max().strftime("%d/%m/%Y"))

# Filtro de período, com o intuito de considerar somente os meses completos
# Janeiro/2019 e dezembro/2022 estão incompletos: a base começa no dia 4 e termina no dia 8, por isso esses dois meses foram deixados de fora.
df = df[(df["DATA"] >= "2019-02-01") & (df["DATA"] < "2022-12-01")]

# Verificação de presença de nulos e respectiva contagem 
#print("Total de nulos por coluna:")
#print(df.isnull().sum())

# Percentual de nulos em cada coluna - o quanto representam em relação ao todo
#print(df.isnull().mean()*100)

# Seleção das colunas válidas: selecionadas somentes as colunas contendo dados válidos
df = df[['DATA', 'CO_ID', 'CL_ID', 'CL_GENERO', 'CL_EC', 'CL_FHL', 'CL_SEG', 'PR_ID', 'PR_CAT', 'PR_NOME']]

# Tratamento dos dados nulos

# Foram identificados dados nulos em PR_CAT (Categoria do produto) e PR_NOME(Nome do produto)

# Antes do tratamento dos dados nulos, buscou-se analisar a consistência dos dados, verificando se um 
# PR_ID (identificador do produtp) não está associado a mais de um valor diferente de PR_CAT ou de PR_NOME.

# Deste modo, foram seguidos os seguintes passos:
# 1 - Levantamento de somente valores válidos através da exclusão dos
#  valores que eventualmente estejam simultaneamente nulos em PR_CAT e PR_NOME
validos = df.dropna(subset=["PR_CAT", "PR_NOME"])


# 2 Verificar se um mesmo PR_ID não está associado a mais de um valor diferente de PR_CAT ou de PR_NOME 
#Para cada PR_ID, contamos quantos valores distintos existem em PR_CAT e em PR_NOME. Se um ID tem sempre 
#a mesma categoria e o mesmo nome, o resultado será 1 em ambas as colunas — o esperado.
conflitos = (validos.groupby("PR_ID")[["PR_CAT", "PR_NOME"]].nunique().query("PR_CAT >1 or PR_NOME > 1"))
#print(f"IDs com conflito: {len(conflitos)}")
conflitos.head()

# 3. Construção da tabela de referência dos produtos
# Após a verificação da consistência, foi construída uma tabela de referência
# contendo o identificador, a categoria e o nome de cada produto.
# A tabela utiliza PR_ID como índice, facilitando a consulta das informações
# válidas para posterior preenchimento dos valores nulos.
tabela_ref_produtos = (validos
               .drop_duplicates("PR_ID")[["PR_ID", "PR_CAT", "PR_NOME"]]
               .set_index("PR_ID"))

#print("Tabela contendo os ids de todos os produtos vendidos pela empresa")
#print(tabela_ref_produtos.head())

# Contabilização dos ids únicos de produtos do df principal (vendas)
# Observação: O set() transforma uma coleção de valores em um conjunto de elementos únicos
ids_vendas = set(df["PR_ID"].dropna().unique()) 

# Contabilização dos ids únicos de produtos da tabela de referência criada
ids_referencia = set(tabela_ref_produtos.index)

# Número total de ids de produtos regitrados na tabela de vendas, mas não presente na tabela de referência
ids_nao_encontrados = ids_vendas - ids_referencia
'''
print(
    f"Total de IDs de produtos não encontrados "
    f"na tabela de referência: {len(ids_nao_encontrados)}"
)
'''

# Contagem dos nulos antes do preenchimento
nulos_antes = df[["PR_CAT", "PR_NOME"]].isnull().sum()
#print("Total de nulos antes do preenchimento:")
#print(nulos_antes)

# Preenchimento dos nulos como "NAO INFORMADO" (Que, portanto, não existem na tabela de referência)
df["PR_CAT"]  = (df["PR_CAT"]
                 .fillna(df["PR_ID"].map(tabela_ref_produtos["PR_CAT"]))
                 .fillna("NAO INFORMADO"))

df["PR_NOME"] = (df["PR_NOME"]
                 .fillna(df["PR_ID"].map(tabela_ref_produtos["PR_NOME"]))
                 .fillna("NAO INFORMADO"))

# Contagem dos nulos após o preenchimento
nulos_apos = df[["PR_CAT", "PR_NOME"]].isnull().sum()
#print("Total de nulos após o preenchimento:")
#print(nulos_apos)

# Verificando inconsistências nos nomes de produtos e categorias
nomes_produtos = df["PR_NOME"].unique()
#print(sorted(nomes_produtos, key=str.lower))

nomes_categorias = df["PR_CAT"].unique()
#print(sorted(nomes_categorias, key=str.lower))

# Tratamento dos nomes dos produtos - padronização para CAIXA ALTA
df['PR_NOME'] = df['PR_NOME'].str.upper()

# Identificação de duplicados
# Decisão: optou-se por manter os duplicados, pois representam um percentual muito pequeno, menor que 0,5%
# e por representar as vendas de um supermercado, é esperado que em uma mesma compra, um item apareça repetido.
#print("Total de duplicados exatos encontrados:", df.duplicated().sum())
percentual_duplicados = (df.duplicated().sum()) / (len(df))
#print(f"Percentual de duplicados: {percentual_duplicados:.2f}%")

# Visualizar os duplicados
duplicados = df[df.duplicated()]

# Visualizar todos os duplicados
df_duplic = df[df.duplicated(keep=False)]
df_duplic.sort_values(by=["CL_ID","PR_NOME"])

# Criação coluna CL_EC_EXTENSO

estado_civil_clientes = {
    1: "CASADO OU UNIAO ESTAVEL",
    2: "DIVORCIADO",
    3: "SEPARADO",
    4: "SOLTEIRO",
    5: "VIUVO"
}

df["CL_EC_DESC"] = df["CL_EC"].map(estado_civil_clientes)
df.head()

# Colunas DIA, MES E ANO
df["DIA"] = df.DATA.dt.day
df["MES"] = df.DATA.dt.month
df["ANO"] = df.DATA.dt.year

# Contagem de valores das colunas criadas e possíveis nulos 

# Coluna CL_EC_DESC
df["CL_EC_DESC"].value_counts(dropna=False)

# Coluna ANO
df["ANO"].value_counts(dropna=False)

# Coluna MES
df["MES"].value_counts(dropna=False)

# Primeiras 2 linhas do df com as novas colunas 
df.head(2)

# Tabela de clientes com dados referentes a gênero, estado civil, nº de filhos, segmento social e total de compras
clientes = df.groupby(["CL_ID","CL_GENERO", "CL_EC_DESC", "CL_FHL","CL_SEG"])["CO_ID"].nunique().reset_index()
clientes.head()

print( "---------- PERFIL DOS CLIENTES ----------")
print("Total de clientes:", df["CL_ID"].nunique())

print("\nClientes por gênero:")
print(clientes["CL_GENERO"].value_counts())

print("\nClientes por estado civil:")
print(clientes["CL_EC_DESC"].value_counts())

print("\nNúmero de filhos:")
print(clientes["CL_FHL"].describe())
print("Clientes com filhos:", (clientes["CL_FHL"] > 0).sum())
print("Clientes sem filhos:", (clientes["CL_FHL"] == 0).sum())

print("\nClientes por segmento econômico:")
print(clientes["CL_SEG"].value_counts())

print("\n ---------- PEDIDOS E ITENS ----------")
total_pedidos = df["CO_ID"].nunique()
total_itens = len(df)  
print("\nTotal de pedidos:", total_pedidos)
print("Total de itens vendidos:", total_itens)

print("\n---------- PEDIDOS POR CLIENTE E OUTLIERS ----------")
pedidos_cliente = df.groupby("CL_ID")["CO_ID"].nunique()

print("\nMédia de pedidos por cliente:", round(pedidos_cliente.mean(), 2))
print(pedidos_cliente.describe())

# Outliers pelo método IQR
q1, q3 = pedidos_cliente.quantile([0.25, 0.75])
limite = q3 + 1.5 * (q3 - q1)
outliers = pedidos_cliente[pedidos_cliente > limite].sort_values(ascending=False)

print(f"\nLimite superior (IQR): {limite:.1f} pedidos")
print("Clientes outliers:", len(outliers))
print(outliers.head(10))

# Peso dos outliers no total de pedidos
print(f"Outliers concentram {outliers.sum() / total_pedidos:.1%} dos pedidos")

print("\n---------- CATEGORIAS E PRODUTOS ----------")
print("\nCategorias mais vendidas (quantidade de itens):")
print(df["PR_CAT"].value_counts())

print("\nTop 10 produtos (quantidade de itens):")
print(df["PR_NOME"].value_counts().head(10))

print("\n---------- QUEM COMPRA MAIS ----------")
compras_por_estado_civil = df.groupby("CL_EC_DESC")["CO_ID"].nunique().reset_index().sort_values(by="CO_ID", ascending=False)
print("\nTotal de pedidos por estado civil:") 
print(compras_por_estado_civil)

compras_por_genero = df.groupby("CL_GENERO")["CO_ID"].nunique().reset_index().sort_values(by="CO_ID", ascending=False)
print("\nTotal de pedidos por gênero:") 
print(compras_por_genero)

compras_por_compos_familiar = df.groupby("CL_FHL")["CO_ID"].nunique().reset_index().sort_values(by="CO_ID", ascending=False)
print("\nTotal de pedidos de acordo com o número de filhos:")
print(compras_por_compos_familiar)

compras_por_seg_economico = df.groupby("CL_SEG")["CO_ID"].nunique().reset_index().sort_values(by="CO_ID", ascending=False)
print("\nTotal de pedidos de acordo com o número de filhos:")
print(compras_por_seg_economico)

print("\n---------- COMO VARIAM AS VENDAS AO LONGO DO TEMPO ----------")

vendas_por_mes_e_ano = (
    df.groupby(["MES","ANO"])["CO_ID"]
           .nunique()
           .unstack()
)

fig, ax = plt.subplots(figsize=(10, 4))
vendas_por_mes_e_ano.plot(ax=ax, marker="o")
ax.set_title("Pedidos por mês, comparando anos")
ax.set_xlabel("Mês")
ax.set_ylabel("Pedidos")
ax.set_xticks(range(1, 13))
ax.legend(title="Ano")
ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()
