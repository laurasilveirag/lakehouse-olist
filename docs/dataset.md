# Dataset: Brazilian E-Commerce (Olist)

Para o desenvolvimento deste trabalho, optamos por utilizar o dataset público **Brazilian E-Commerce Public Dataset by Olist**, disponibilizado na plataforma Kaggle.

Ele simula perfeitamente um banco de dados relacional de e-commerce real, contendo informações de mais de 100 mil pedidos realizados entre 2016 e 2018 em múltiplos marketplaces do Brasil.

🔗 **Link Oficial:** [Kaggle - Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

## 📁 Extração e Landing Zone

Simulando a extração de um banco de dados relacional, os dados foram extraídos no formato **CSV** e carregados no Databricks, especificamente no *Volume* do schema `LANDING/DADOS`.

Abaixo estão os arquivos extraídos e o volume de registros:

| Arquivo Origem (CSV) | Tabela Alvo | Registros |
|---|---|---|
| `olist_customers_dataset.csv` | customers | 99.441 |
| `olist_geolocation_dataset.csv` | geolocation | 1.000.163 |
| `olist_order_items_dataset.csv` | order_items | 112.650 |
| `olist_order_payments_dataset.csv` | order_payments | 103.886 |
| `olist_order_reviews_dataset.csv` | order_reviews | 104.719 |
| `olist_orders_dataset.csv` | orders | 99.441 |
| `olist_products_dataset.csv` | products | 32.951 |
| `olist_sellers_dataset.csv` | sellers | 3.095 |
| `product_category_name_translation.csv`| category_translation| 70 |

> **Nota:** Estes arquivos formam a base para o início do nosso processamento em direção à camada Bronze.
