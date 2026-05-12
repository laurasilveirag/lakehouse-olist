# Lakehouse Olist - Arquitetura Medalhao

![build](https://img.shields.io/badge/build-passing-brightgreen)
![docs](https://img.shields.io/badge/docs-mkdocs-blue)
![license](https://img.shields.io/badge/license-MIT-green)

Estudo pratico de engenharia de dados implementando a **Arquitetura Medalhao** (Landing -> Bronze -> Silver -> Gold) sobre o dataset publico brasileiro de e-commerce da **Olist**, utilizando o **Databricks** como plataforma de processamento e **Delta Lake** como formato de armazenamento.

## Desenho de Arquitetura

```
Olist (Kaggle)
      |
      v
[ LANDING/DADOS ]
  CSVs brutos no Volume do Unity Catalog
      |
      v
[    BRONZE    ]
  Delta Lake - dados brutos com metadados
  (dt_ingestao, nm_arquivo_origem)
      |
      v
[    SILVER    ]
  Delta Lake - Data Quality aplicado
  (remocao de duplicatas, nulos, padronizacao)
      |
      v
[     GOLD     ]
  Modelo Dimensional - Ralph Kimball
  (dim_cliente, dim_produto, dim_vendedor, dim_data, fato_pedido)
      |
      v
[ JOBS & PIPELINES ]
  Execucao encadeada e automatizada no Databricks
```

## Dataset

O dataset utilizado e o **Brazilian E-Commerce Public Dataset by Olist**, disponivel publicamente no Kaggle:

> https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Contem informacoes reais de pedidos realizados entre 2016 e 2018 em multiplos marketplaces do Brasil. Os arquivos CSV estao disponiveis na pasta `data/` deste repositorio, com excecao do arquivo `olist_geolocation_dataset.csv` (58 MB), que deve ser baixado diretamente pelo link acima e colocado na pasta `data/` antes de executar o pipeline.

| Arquivo | Tabela | Registros |
|---|---|---|
| olist_customers_dataset.csv | customers | 99.441 |
| olist_geolocation_dataset.csv | geolocation | 1.000.163 |
| olist_order_items_dataset.csv | order_items | 112.650 |
| olist_order_payments_dataset.csv | order_payments | 103.886 |
| olist_order_reviews_dataset.csv | order_reviews | 104.719 |
| olist_orders_dataset.csv | orders | 99.441 |
| olist_products_dataset.csv | products | 32.951 |
| olist_sellers_dataset.csv | sellers | 3.095 |
| product_category_name_translation.csv | category_translation | 70 |

## Ferramentas utilizadas

- **Plataforma:** Databricks
- **Armazenamento:** Delta Lake (formato ACID com versionamento)
- **Linguagem:** Python 3 / PySpark
- **Orquestracao:** Databricks Jobs & Pipelines
- **Versionamento:** Git + GitHub
- **Documentacao:** MkDocs Material + GitHub Pages

## Estrutura do Projeto

```
lakehouse-olist/
├── notebooks/
│   ├── 001_preparando_ambiente.py     # Cria schemas e volumes no Unity Catalog
│   ├── 002_bronze_olist.py            # Ingestao: Landing -> Bronze (Delta Lake)
│   ├── 003_silver_olist.py            # Data Quality: Bronze -> Silver
│   └── 004_gold_olist.py             # Modelagem Dimensional: Silver -> Gold
├── data/
│   ├── olist_customers_dataset.csv
│   ├── olist_order_items_dataset.csv
│   ├── olist_order_payments_dataset.csv
│   ├── olist_order_reviews_dataset.csv
│   ├── olist_orders_dataset.csv
│   ├── olist_products_dataset.csv
│   ├── olist_sellers_dataset.csv
│   ├── product_category_name_translation.csv
│   └── olist_geolocation_dataset.csv 
├── docs/
│   ├── index.md
│   ├── dataset.md
│   ├── arquitetura.md
│   └── pipeline.md
├── assets/
├── .gitignore
├── .python-version
├── LICENSE
├── README.md
└── mkdocs.yml
```

## Como executar

### 1. Clonar o repositorio

```bash
git clone https://github.com/laurasilveirag/lakehouse-olist.git
cd lakehouse-olist
```

### 2. Configurar o Databricks

Crie uma conta em [databricks.com](https://www.databricks.com) e acesse o workspace.

### 3. Importar os notebooks

No Databricks, acesse **Workspace > seu usuario > Import** e importe os arquivos `.py` da pasta `notebooks/` na seguinte ordem:

| Ordem | Notebook | Descricao |
|---|---|---|
| 1 | 001_preparando_ambiente.py | Cria os schemas landing, bronze, silver e gold e o volume landing/dados |
| 2 | 002_bronze_olist.py | Le os CSVs do volume e grava em Delta Lake no schema bronze |
| 3 | 003_silver_olist.py | Aplica Data Quality e grava no schema silver |
| 4 | 004_gold_olist.py | Cria o modelo dimensional e grava no schema gold |

### 4. Fazer upload dos CSVs

No Databricks, acesse **Catalog > workspace > landing > dados** e faca o upload de todos os arquivos da pasta `data/`.

### 5. Executar o pipeline

Execute os notebooks na ordem indicada, ou utilize o **Job** configurado no Databricks para execucao encadeada automatica:

- Workflow: `pipeline_lakehouse_olist`
- Tasks: Bronze -> Silver -> Gold (execucao sequencial)

## Modelo Dimensional (Gold)

O schema Gold implementa o modelo estrela seguindo a metodologia de **Ralph Kimball**:

| Tabela | Tipo | Descricao |
|---|---|---|
| dim_cliente | Dimensao | Dados dos clientes (cidade, estado, CEP) |
| dim_produto | Dimensao | Dados dos produtos (categoria PT/EN, dimensoes, peso) |
| dim_vendedor | Dimensao | Dados dos vendedores (cidade, estado, CEP) |
| dim_data | Dimensao | Calendario gerado a partir das datas de compra |
| fato_pedido | Fato | Metricas dos pedidos (valor, frete, pagamento, nota) |

## Documentacao

A documentacao completa esta publicada via MkDocs Material no GitHub Pages:

> https://laurasilveirag.github.io/lakehouse-olist/

## Autores

- **Laura Silveira** - [github.com/laurasilveirag](https://github.com/laurasilveirag)
- **Ana Santinoni** - [github.com/anasantinoni](https://github.com/anasantinoni)
- **Janaína Carlos** - [github.com/janainacarlos](https://github.com/janainacarlos)

## Licenca

Este projeto esta sob a licenca MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Referencias

- [Databricks](https://www.databricks.com)
- [Arquitetura Medalhao](https://www.databricks.com/br/glossary/medallion-architecture)
- [Delta Lake](https://delta.io/)
- [Jobs & Pipelines no Databricks](https://docs.databricks.com/workflows/index.html)
- [Dataset Olist - Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)