# Databricks notebook source
# MAGIC %md
# MAGIC # 003 - Silver - Olist
# MAGIC ## Le as tabelas do Bronze, aplica Data Quality e salva no schema Silver
# MAGIC
# MAGIC **Camada Silver:**
# MAGIC - Remocao de duplicatas
# MAGIC - Tratamento de nulos
# MAGIC - Padronizacao de tipos
# MAGIC - Renomeacao de colunas para portugues sem abreviacoes
# MAGIC - Formato Delta Lake

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, col, upper, trim

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1. customers -> clientes

# COMMAND ----------

df_customers = spark.read.format("delta").table("bronze.customers")

df_clientes = df_customers \
    .dropDuplicates(["customer_id"]) \
    .dropna(subset=["customer_id", "customer_state"]) \
    .withColumnRenamed("customer_id",              "ID_CLIENTE") \
    .withColumnRenamed("customer_unique_id",       "ID_CLIENTE_UNICO") \
    .withColumnRenamed("customer_zip_code_prefix", "CEP") \
    .withColumnRenamed("customer_city",            "CIDADE") \
    .withColumnRenamed("customer_state",           "ESTADO") \
    .withColumn("CIDADE", upper(trim(col("CIDADE")))) \
    .withColumn("ESTADO", upper(trim(col("ESTADO")))) \
    .drop("dt_ingestao", "nm_arquivo_origem") \
    .withColumn("dt_ingestao", current_timestamp())

df_clientes.write.format("delta").mode("overwrite").saveAsTable("silver.clientes")
print(f"silver.clientes - {df_clientes.count():,} registros")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2. sellers -> vendedores

# COMMAND ----------

df_sellers = spark.read.format("delta").table("bronze.sellers")

df_vendedores = df_sellers \
    .dropDuplicates(["seller_id"]) \
    .dropna(subset=["seller_id", "seller_state"]) \
    .withColumnRenamed("seller_id",              "ID_VENDEDOR") \
    .withColumnRenamed("seller_zip_code_prefix", "CEP_VENDEDOR") \
    .withColumnRenamed("seller_city",            "CIDADE_VENDEDOR") \
    .withColumnRenamed("seller_state",           "ESTADO_VENDEDOR") \
    .withColumn("CIDADE_VENDEDOR", upper(trim(col("CIDADE_VENDEDOR")))) \
    .withColumn("ESTADO_VENDEDOR", upper(trim(col("ESTADO_VENDEDOR")))) \
    .drop("dt_ingestao", "nm_arquivo_origem") \
    .withColumn("dt_ingestao", current_timestamp())

df_vendedores.write.format("delta").mode("overwrite").saveAsTable("silver.vendedores")
print(f"silver.vendedores - {df_vendedores.count():,} registros")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 3. products + category_translation -> produtos

# COMMAND ----------

df_products = spark.read.format("delta").table("bronze.products")
df_category = spark.read.format("delta").table("bronze.category_translation")

df_produtos = df_products \
    .dropDuplicates(["product_id"]) \
    .dropna(subset=["product_id"]) \
    .join(df_category, on="product_category_name", how="left") \
    .withColumnRenamed("product_id",                    "ID_PRODUTO") \
    .withColumnRenamed("product_category_name",         "CATEGORIA_PT") \
    .withColumnRenamed("product_category_name_english", "CATEGORIA_EN") \
    .withColumnRenamed("product_name_lenght",           "TAMANHO_NOME") \
    .withColumnRenamed("product_description_lenght",    "TAMANHO_DESCRICAO") \
    .withColumnRenamed("product_photos_qty",            "QTD_FOTOS") \
    .withColumnRenamed("product_weight_g",              "PESO_G") \
    .withColumnRenamed("product_length_cm",             "COMPRIMENTO_CM") \
    .withColumnRenamed("product_height_cm",             "ALTURA_CM") \
    .withColumnRenamed("product_width_cm",              "LARGURA_CM") \
    .drop("dt_ingestao", "nm_arquivo_origem") \
    .withColumn("dt_ingestao", current_timestamp())

df_produtos.write.format("delta").mode("overwrite").saveAsTable("silver.produtos")
print(f"silver.produtos - {df_produtos.count():,} registros")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4. orders -> pedidos

# COMMAND ----------

df_orders = spark.read.format("delta").table("bronze.orders")

df_pedidos = df_orders \
    .dropDuplicates(["order_id"]) \
    .dropna(subset=["order_id", "customer_id", "order_status"]) \
    .withColumnRenamed("order_id",                      "ID_PEDIDO") \
    .withColumnRenamed("customer_id",                   "ID_CLIENTE") \
    .withColumnRenamed("order_status",                  "STATUS_PEDIDO") \
    .withColumnRenamed("order_purchase_timestamp",      "DT_COMPRA") \
    .withColumnRenamed("order_approved_at",             "DT_APROVACAO") \
    .withColumnRenamed("order_delivered_carrier_date",  "DT_ENTREGA_TRANSPORTADORA") \
    .withColumnRenamed("order_delivered_customer_date", "DT_ENTREGA_CLIENTE") \
    .withColumnRenamed("order_estimated_delivery_date", "DT_PREVISAO_ENTREGA") \
    .withColumn("STATUS_PEDIDO", upper(trim(col("STATUS_PEDIDO")))) \
    .drop("dt_ingestao", "nm_arquivo_origem") \
    .withColumn("dt_ingestao", current_timestamp())

df_pedidos.write.format("delta").mode("overwrite").saveAsTable("silver.pedidos")
print(f"silver.pedidos - {df_pedidos.count():,} registros")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 5. order_items -> itens_pedido

# COMMAND ----------

df_items = spark.read.format("delta").table("bronze.order_items")

df_itens = df_items \
    .dropDuplicates(["order_id", "order_item_id"]) \
    .dropna(subset=["order_id", "product_id", "seller_id"]) \
    .filter(col("price") > 0) \
    .withColumnRenamed("order_id",            "ID_PEDIDO") \
    .withColumnRenamed("order_item_id",       "NUM_ITEM") \
    .withColumnRenamed("product_id",          "ID_PRODUTO") \
    .withColumnRenamed("seller_id",           "ID_VENDEDOR") \
    .withColumnRenamed("shipping_limit_date", "DT_LIMITE_ENVIO") \
    .withColumnRenamed("price",               "VALOR_ITEM") \
    .withColumnRenamed("freight_value",       "VALOR_FRETE") \
    .drop("dt_ingestao", "nm_arquivo_origem") \
    .withColumn("dt_ingestao", current_timestamp())

df_itens.write.format("delta").mode("overwrite").saveAsTable("silver.itens_pedido")
print(f"silver.itens_pedido - {df_itens.count():,} registros")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 6. order_payments -> pagamentos

# COMMAND ----------

df_payments = spark.read.format("delta").table("bronze.order_payments")

df_pagamentos = df_payments \
    .dropDuplicates(["order_id", "payment_sequential"]) \
    .dropna(subset=["order_id", "payment_type"]) \
    .filter(col("payment_value") >= 0) \
    .withColumnRenamed("order_id",             "ID_PEDIDO") \
    .withColumnRenamed("payment_sequential",   "NUM_PAGAMENTO") \
    .withColumnRenamed("payment_type",         "TIPO_PAGAMENTO") \
    .withColumnRenamed("payment_installments", "NUM_PARCELAS") \
    .withColumnRenamed("payment_value",        "VALOR_PAGAMENTO") \
    .withColumn("TIPO_PAGAMENTO", upper(trim(col("TIPO_PAGAMENTO")))) \
    .drop("dt_ingestao", "nm_arquivo_origem") \
    .withColumn("dt_ingestao", current_timestamp())

df_pagamentos.write.format("delta").mode("overwrite").saveAsTable("silver.pagamentos")
print(f"silver.pagamentos - {df_pagamentos.count():,} registros")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 7. order_reviews -> avaliacoes

# COMMAND ----------

df_reviews = spark.read.format("delta").table("bronze.order_reviews")

df_avaliacoes = df_reviews \
    .dropDuplicates(["review_id"]) \
    .dropna(subset=["review_id", "order_id", "review_score"]) \
    .withColumnRenamed("review_id",               "ID_AVALIACAO") \
    .withColumnRenamed("order_id",                "ID_PEDIDO") \
    .withColumnRenamed("review_score",            "NOTA") \
    .withColumnRenamed("review_comment_title",    "TITULO_COMENTARIO") \
    .withColumnRenamed("review_comment_message",  "COMENTARIO") \
    .withColumnRenamed("review_creation_date",    "DT_CRIACAO") \
    .withColumnRenamed("review_answer_timestamp", "DT_RESPOSTA") \
    .drop("dt_ingestao", "nm_arquivo_origem") \
    .withColumn("dt_ingestao", current_timestamp())

df_avaliacoes.write.format("delta").mode("overwrite").saveAsTable("silver.avaliacoes")
print(f"silver.avaliacoes - {df_avaliacoes.count():,} registros")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 8. geolocation -> geolocalizacao

# COMMAND ----------

df_geo = spark.read.format("delta").table("bronze.geolocation")

df_geolocalizacao = df_geo \
    .dropDuplicates(["geolocation_zip_code_prefix", "geolocation_lat", "geolocation_lng"]) \
    .dropna(subset=["geolocation_zip_code_prefix", "geolocation_state"]) \
    .withColumnRenamed("geolocation_zip_code_prefix", "CEP") \
    .withColumnRenamed("geolocation_lat",             "LATITUDE") \
    .withColumnRenamed("geolocation_lng",             "LONGITUDE") \
    .withColumnRenamed("geolocation_city",            "CIDADE") \
    .withColumnRenamed("geolocation_state",           "ESTADO") \
    .withColumn("CIDADE", upper(trim(col("CIDADE")))) \
    .withColumn("ESTADO", upper(trim(col("ESTADO")))) \
    .drop("dt_ingestao", "nm_arquivo_origem") \
    .withColumn("dt_ingestao", current_timestamp())

df_geolocalizacao.write.format("delta").mode("overwrite").saveAsTable("silver.geolocalizacao")
print(f"silver.geolocalizacao - {df_geolocalizacao.count():,} registros")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Validacao das tabelas Silver

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN silver;
