# Análise Exploratória de Dados – Base de Dados Varejo

Mini projeto de análise exploratória de dados em Python com Pandas aplicada a uma base de dados com registros reais de compras (datas, clientes, produtos, categorias e valores)

# Objetivos

- Realizar a análise exploratória da base de dados.  
- Verificar a qualidade, realizar a limpeza e sumarizar os dados. 
- Identificar problemas nos dados, como valores nulos, tipos incorretos e duplicados.
- Realizar o tratamento dos dados com Pandas. 
- Gerar estatísticas simples e funções de agrupamento para responder às perguntas operacionais. 

---

## Principais perguntas a serem respondidas

1. Qual o perfil dos clientes? 
2. Quem compra mais?
3. Quais categorias de produtos vendem mais?
4. Como as vendas variam ao longo do tempo?

---

## Fonte de dados

Os dados foram obtidos a partir da tabela de vendas `BaseVarejoDadosBrutos.csv` contendo 830 mil registros iniciais.

---

## Dicionário de dados

1. DATA: Data da compra; 
2. CO_ID: Identificação do número de compra (número da nota fiscal); 
3. CL_ID: Identificação do cliente (número do cliente); 
4. CL_GENERO: Sexo biológico informado pelo cliente; 
5. CL_EC: Estado civil do cliente: 1: Casado ou união estával; 2: Divorciado; 3: Separado; 4: Solteiro; 
5: Viúvo. 
6. CL_FHL: Número de filhos do cliente; 
7. CL_SEG: Segmentação econômica do cliente (classe A, B ou C); 
8. PR_ID: Código do produto (SKU) adquirido; 
9. PR_CAT: Categoria do produto adquirido; 
10. PR_NOME: Nome do produto adquirido. 

---

## Ferramentas e tecnologias utilizadas

- **Python**: linguagem utilizada para manipulação e análise dos dados.
- **Pandas**: biblioteca utilizada para tratamento, agrupamento, contagem e sumarização dos dados.
- **Visual Studio Code**: ambiente de desenvolvimento do projeto.

---

## Etapas de desenvolvimento do projeto

A análise foi organizada nas seguintes etapas:

1. Exploração dos dados: identificação das informações disponíveis na base de dados de clientes, pedidos e produtos.
2. Tratamento e validação: verificação da consistência dos dados, identificação de dados nulos e análise de possíveis duplicidades.
3. Análise do perfil dos clientes: distribuição por características demográficas e segmento econômico.
4. Análise dos pedidos: cálculo dos volumes de pedidos e itens vendidos, além da quantidade de pedidos por cliente.
5. Análise de outliers: aplicação do método do intervalo interquartil (IQR) para identificar clientes com quantidades de pedidos acima do limite superior.
6. Análise de produtos: identificação das categorias e dos produtos com maior volume de itens vendidos.
7. Comparação entre grupos: contagem dos pedidos por estado civil, gênero, número de filhos e segmento econômico.
8. Consolidação dos resultados: organização dos principais indicadores e elaboração das conclusões.

---

## Resultados e conclusões

### Visão geral da base

| Indicador | Resultado |
|---|---:|
| Total de clientes | 1.000 |
| Total de pedidos | 17.987 |
| Total de itens vendidos | 807.625 |
| Média de pedidos por cliente | 17,99 |

A base apresenta 1.000 clientes e 17.987 pedidos, com um volume total de 807.625 itens vendidos. Em média, cada cliente realizou aproximadamente 18 pedidos no período analisado.

### Perfil dos clientes

**Distribuição por gênero**

| Gênero | Clientes | Percentual |
|---|---:|---:|
| Feminino | 519 | 51,9% |
| Masculino | 481 | 48,1% |
| **Total** | **1.000** | **100%** |

A distribuição por gênero é relativamente equilibrada, com uma pequena predominância de clientes do gênero feminino.

**Distribuição por estado civil**

| Estado civil | Clientes | Percentual |
|---|---:|---:|
| Solteiro | 251 | 25,1% |
| Separado | 250 | 25,0% |
| Divorciado | 238 | 23,8% |
| Casado ou união estável | 233 | 23,3% |
| Viúvo | 28 | 2,8% |
| **Total** | **1.000** | **100%** |

Os grupos de solteiros, separados, divorciados e casados ou em união estável apresentam participações relativamente próximas. Os clientes viúvos representam a menor parcela da base, com 2,8%.

**Distribuição por número de filhos**

| Indicador | Resultado |
|---|---:|
| Clientes sem filhos | 527 (52,7%) |
| Clientes com filhos | 473 (47,3%) |
| Média de filhos por cliente | 1,136 |
| Mediana de filhos por cliente | 0 |
| Máximo de filhos registrado | 4 |

Mais da metade dos clientes não possui filhos. A média é de aproximadamente 1,14 filho por cliente, enquanto a mediana igual a zero indica que pelo menos metade da base não possui filhos.

**Distribuição por segmento econômico**

| Segmento | Clientes | Percentual |
|---|---:|---:|
| B | 645 | 64,5% |
| C | 271 | 27,1% |
| A | 84 | 8,4% |
| **Total** | **1.000** | **100%** |

O segmento B concentra a maior parte dos clientes, representando 64,5% da base. O segmento C corresponde a 27,1%, enquanto o segmento A representa 8,4%.

### Pedidos por cliente e identificação de outliers

A quantidade de pedidos por cliente apresenta a seguinte distribuição:

| Indicador | Quantidade de pedidos |
|---|---:|
| Média | 17,99 |
| Desvio-padrão | 4,27 |
| Mínimo | 6 |
| Primeiro quartil (Q1) | 15 |
| Mediana | 18 |
| Terceiro quartil (Q3) | 21 |
| Máximo | 34 |

Para identificar possíveis outliers, foi utilizado o método do intervalo interquartil (IQR).

O intervalo interquartil é calculado pela diferença entre o terceiro e o primeiro quartil:

`IQR = Q3 - Q1`

Com base nos dados, o IQR é igual a 6 pedidos. Aplicando o critério de 1,5 vez o IQR, o limite superior é de 30 pedidos:

`Limite superior = Q3 + 1,5 × IQR`

`Limite superior = 21 + 1,5 × 6 = 30`

Foram identificados quatro clientes com mais de 30 pedidos:

| ID do cliente | Quantidade de pedidos |
|---|---:|
| 41 | 34 |
| 822 | 33 |
| 122 | 31 |
| 485 | 31 |

Esses quatro clientes representam 0,4% dos 1.000 clientes analisados. Em conjunto, realizaram 129 pedidos, equivalentes a aproximadamente 0,72% do total de pedidos.
Os resultados indicam que poucos clientes apresentam uma frequência de compra superior ao limite definido pelo IQR. 

### Categorias mais vendidas

As categorias foram comparadas considerando a quantidade de itens vendidos.

| Categoria | Itens vendidos | Participação aproximada |
|---|---:|---:|
| Alimentos | 423.069 | 52,38% |
| Higiene | 151.400 | 18,75% |
| Limpeza | 141.786 | 17,56% |
| Bebidas | 42.119 | 5,21% |
| Pet | 31.527 | 3,90% |
| Acessórios | 14.167 | 1,75% |
| Não informado | 3.557 | 0,44% |
| **Total** | **807.625** | **100%** |

A categoria Alimentos concentra aproximadamente 52,4% dos itens vendidos, destacando-se das demais categorias. Higiene e Limpeza aparecem em seguida, com participações de 18,75% e 17,56%, respectivamente.

Em conjunto, Alimentos, Higiene e Limpeza representam aproximadamente 88,7% dos itens vendidos. Esse resultado evidencia a concentração do volume de vendas nessas três categorias.

A categoria Não Informado representa 0,44% dos itens, que correspondem, exatamente aos registros identificados previamente como nulos, ou seja, que estavam sem a classificação de categoria. Embora essa participação seja pequena, o preenchimento dessas informações pode contribuir para a qualidade e a consistência dos dados.

### Top 10 produtos por quantidade de itens vendidos

| Posição | Produto | Itens vendidos |
|---:|---|---:|
| 1 | Presunto cozido | 13.976 |
| 2 | Sardinha | 7.289 |
| 3 | Banana | 7.196 |
| 4 | Desengordurante | 7.195 |
| 5 | Gel | 7.184 |
| 6 | Bife de coxão mole | 7.171 |
| 7 | Rodo | 7.159 |
| 8 | Removedor | 7.159 |
| 9 | Modelador | 7.158 |
| 10 | Papinha infantil | 7.156 |

O Presunto Cozido lidera o ranking, com 13.976 itens vendidos, quase o dobro do volume do segundo colocado, Sardinha, com 7.289 unidades.

Os demais produtos do ranking apresentam quantidades próximas, variando de 7.156 a 7.196 itens, com exceção dos dois primeiros colocados.

O ranking permite identificar os produtos com maior volume de saída, mas não determina, isoladamente, quais geram maior faturamento ou lucratividade. Para isso, seriam necessários dados de preços, custos e margens.

### Pedidos por características dos clientes

**Por estado civil**

| Estado civil | Total de pedidos |
|---|---:|
| Separado | 4.640 |
| Solteiro | 4.440 |
| Divorciado | 4.266 |
| Casado ou união estável | 4.165 |
| Viúvo | 476 |

O grupo de clientes separados apresenta o maior volume total de pedidos, seguido pelos solteiros, divorciados e casados. O grupo de clientes viúvos é o que apresenta o menor volume, quando comparado com os demais.

Como os grupos possuem quantidades diferentes de clientes, o total de pedidos não deve ser interpretado isoladamente como maior frequência de compra individual. Para uma comparação mais adequada, seria necessário calcular a média de pedidos por cliente em cada estado civil.

**Por gênero**

| Gênero | Total de pedidos |
|---|---:|
| Feminino | 9.368 |
| Masculino | 8.619 |
| **Total** | **17.987** |

Os clientes do gênero feminino realizaram 9.368 pedidos, enquanto os do gênero masculino realizaram 8.619. A diferença corresponde a somente 749 pedidos.

**Por número de filhos**

| Número de filhos | Total de pedidos |
|---:|---:|
| 0 | 9.489 |
| 1 | 2.186 |
| 2 | 2.320 |
| 3 | 2.235 |
| 4 | 1.757 |
| **Total** | **17.987** |

Os clientes sem filhos concentram o maior número de pedidos, com 9.489. Esse grupo também é o maior da base, com 527 clientes.

**Por segmento econômico**

| Segmento | Total de pedidos |
|---|---:|
| B | 11.543 |
| C | 4.984 |
| A | 1.460 |
| **Total** | **17.987** |

O segmento B concentra o maior volume de pedidos, seguido pelos segmentos C e A. Essa distribuição acompanha a composição da base, na qual o segmento B também reúne a maior quantidade de clientes.

---

## Estrutura do repositório

```
├── .gitignore
├── BaseVarejoDadosBrutos.csv
├── Instrucoes.md
├── ProjetoVarejo.py
└── README.md                                               
                                         
```
---



