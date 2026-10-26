## Decisões técnicas e tratamento dos dados

Com o intuito de melhorar a qualidade, consistência e a organização dos dados foram adotadas as seguintes decisões técnicas:  


### 1. Leitura e definição dos tipos de dados

A leitura do arquivo CSV foi realizada com a biblioteca Pandas, utilizando parâmetros específicos para controlar a interpretação dos dados.

- **Separador (`sep=";"`):** definido conforme a estrutura do arquivo de origem.
- **Tipos de dados (`dtype`):** as colunas `CO_ID`, `CL_ID` e `PR_ID` foram definidas como strings, pois representam identificadores, e não valores numéricos utilizados em cálculos matemáticos.
- **Conversão de datas (`parse_dates` e `pd.to_datetime`):** a coluna `DATA` foi convertida para o tipo datetime, permitindo filtrar períodos e extrair componentes temporais.
- **Tratamento de valores ausentes (`na_values` e `keep_default_na`):** o valor `#N/D` foi reconhecido como ausente, juntamente com outros marcadores padrão identificados pelo Pandas.

Essas decisões permitem interpretar os dados de acordo com sua finalidade e facilitam as operações posteriores de filtragem, agrupamento e análise.

### 2. Seleção do período analisado

A base original apresentava registros incompletos em janeiro de 2019 e dezembro de 2022. Para evitar comparações entre meses com diferentes quantidades de dias registrados, optou-se por excluir esses dois meses e considerar somente os meses completos.

O período selecionado foi de fevereiro de 2019 a novembro de 2022, inclusive.

Essa decisão busca tornar as comparações mensais mais consistentes, reduzindo o risco de interpretar um volume menor de vendas em meses incompletos como uma redução real da atividade comercial.

### 3. Seleção das colunas relevantes

Após a inspeção inicial, foram identificadas 3 colunas sem nome e com 100% dos dados nulos, deste modo, foram mantidas somente as colunas que continham dados relevantes para a análise: data, identificadores de pedidos, clientes e produtos, características dos clientes, categoria e nome dos produtos.

### 4. Investigação e tratamento dos valores ausentes

Foram identificados valores ausentes nas colunas `PR_CAT` (categoria do produto) e `PR_NOME` (nome do produto). Em vez de excluir ou substituir imediatamente todos os valores ausentes por uma classificação genérica, foi adotada uma abordagem baseada na verificação da consistência dos identificadores de produtos.Para tal, inicialmente, foram selecionados os registros que possuíam simultaneamente categoria e nome do produto preenchidos.

Em seguida, foi utilizado o agrupamento por `PR_ID`, com a contagem de valores distintos de `PR_CAT` e `PR_NOME`, para identificar possíveis conflitos.

O objetivo foi verificar se um mesmo identificador estava associado a categorias ou nomes diferentes. Essa verificação é importante porque o preenchimento automático só é confiável quando existe uma associação consistente entre o identificador e as informações do produto.

#### 4.1. Construção de uma tabela de referência

A partir dos registros válidos, foi construída uma tabela de referência contendo `PR_ID`, `PR_CAT` e `PR_NOME`.

A tabela utiliza `PR_ID` como índice, permitindo consultar a categoria e o nome associados a cada produto.

Também foi utilizado `drop_duplicates("PR_ID")` para manter apenas um registro por identificador na tabela de referência. Essa decisão pressupõe que os identificadores sejam consistentes e que não existam conflitos entre os registros selecionados.

#### 4.2. Preenchimento dos valores ausentes

O preenchimento foi realizado em duas etapas:

1. **Recuperação das informações:** os valores ausentes foram preenchidos utilizando o identificador do produto para consultar a tabela de referência.
2. **Classificação dos casos não recuperados:** quando não havia informação correspondente na tabela de referência, foi utilizado o valor `NAO INFORMADO`.

A classificação `NAO INFORMADO`  permite contabilizar os registros separadamente nas análises de categorias e produtos.

### 5. Padronização dos nomes dos produtos

Os nomes dos produtos foram convertidos para letras maiúsculas por meio do método `str.upper()`.

A decisão busca evitar que diferenças exclusivamente relacionadas à capitalização, como `Banana` e `BANANA`, sejam tratadas como nomes distintos.

Essa padronização facilita a contagem, a ordenação e a identificação de produtos repetidos em diferentes registros.

### 6. Decisão sobre registros duplicados

Foram identificados registros duplicados exatos, considerando todas as colunas presentes no DataFrame no momento da verificação.

Optou-se por mantê-los porque representam uma parcela inferior a 0,5% dos registros e porque, em uma base de vendas de supermercado, a repetição de produtos em uma mesma compra pode ser legítima.

### 7. Tradução do código de estado civil

A coluna `CL_EC` contém códigos numéricos para representar o estado civil dos clientes. Para facilitar a interpretação dos resultados, foi criado o dicionário `estado_civil_clientes`, relacionando cada código à sua descrição textual.

Com o método `map()`, foi criada a coluna `CL_EC_DESC`, que apresenta as categorias por extenso.

Essa transformação melhora a legibilidade das tabelas e dos relatórios, tornando os resultados mais fáceis de interpretar sem a necessidade de consultar continuamente uma tabela de códigos.

### 8. Criação de atributos temporais

A partir da coluna `DATA`, foram criadas três novas colunas:

- `DIA`: dia do mês.
- `MES`: mês.
- `ANO`: ano.

A extração foi realizada por meio do acessor `.dt` do Pandas.

Essas variáveis permitem agrupar e comparar os dados por diferentes períodos, apoiando futuras análises de evolução das vendas, sazonalidade e comportamento de compra ao longo do tempo.

### 9. Construção da tabela de clientes

Ao final dessa etapa, foi construída uma tabela agrupada por `CL_ID`, gênero, estado civil, número de filhos e segmento econômico.

Para cada combinação dessas características, foi contabilizada a quantidade de identificadores únicos de pedidos (`CO_ID`), utilizando `nunique()`.

A contagem de pedidos únicos evita que um mesmo pedido seja contado várias vezes quando possui diferentes produtos ou itens registrados em múltiplas linhas da base.

O resultado permite analisar o volume de pedidos associado a cada perfil de cliente.

### 10. Bibliotecas utilizadas

O projeto utiliza as seguintes bibliotecas:

- **Pandas:** leitura de arquivos, seleção e transformação de colunas, tratamento de valores ausentes, agrupamentos, contagens e criação de variáveis.
- **Matplotlib:** importado para a construção de gráfico de análise temporal.

### Considerações finais sobre as decisões técnicas (pontos de melhoria)

Algumas decisões dependem ainda de validações adicionais, especialmente:
 - A interpretação dos registros duplicados; 
 - A consistência das informações associadas a cada identificador de produto;
 - E a unicidade das características cadastrais de cada cliente. 