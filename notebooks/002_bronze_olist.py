# Databricks notebook source
# MAGIC %md
# MAGIC # 002 - Bronze - Olist
# MAGIC ## Le os CSVs do volume landing/dados e salva em Delta Lake no schema Bronze
# MAGIC
# MAGIC **Camada Bronze:**
# MAGIC - Copia fiel dos dados brutos do landing
# MAGIC - Formato Delta Lake
# MAGIC - Adiciona metadados: data de ingestao e nome do arquivo de origem

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit

# COMMAND ----------

# MAGIC %md
# MAGIC ### Definicao dos arquivos CSV e tabelas de destino

# COMMAND ----------

tabelas = [
    ("olist_customers_dataset.csv",           "customers"),
    ("olist_geolocation_dataset.csv",         "geolocation"),
    ("olist_order_items_dataset.csv",         "order_items"),
    ("olist_order_payments_dataset.csv",      "order_payments"),
    ("olist_order_reviews_dataset.csv",       "order_reviews"),
    ("olist_orders_dataset.csv",              "orders"),
    ("olist_products_dataset.csv",            "products"),
    ("olist_sellers_dataset.csv",             "sellers"),
    ("product_category_name_translation.csv", "category_translation"),
]

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ingestao: Landing -> Bronze

# COMMAND ----------

for arquivo, tabela in tabelas:
    caminho = f"/Volumes/workspace/landing/dados/{arquivo}"

    print(f"Lendo: {arquivo}")

    df = spark.read.csv(
        caminho,
        header=True,
        inferSchema=True,
        sep=","
    )

    df = df.withColumn("dt_ingestao", current_timestamp())
    df = df.withColumn("nm_arquivo_origem", lit(arquivo))

    df.write \
      .format("delta") \
      .mode("overwrite") \
      .saveAsTable(f"bronze.{tabela}")

    print(f"bronze.{tabela} salva com {df.count():,} registros")

print("Bronze concluido com sucesso!")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Validacao das tabelas criadas

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN bronze;
