# Bem-vindo(a) ao Lakehouse Olist

Projeto prático da disciplina demonstrando a implementação de um pipeline de dados ponta a ponta no **Databricks Free Edition**, utilizando a **Arquitetura Medalhão** (Medallion Architecture) e o formato **Delta Lake**.

## 🎯 Objetivo do Trabalho

Conforme os requisitos da disciplina, o objetivo deste projeto é construir um pipeline automatizado que:

1. **Extrai** dados e os armazena no formato CSV no schema `LANDING/DADOS`.
2. **Ingere** esses dados no formato Delta Lake criando a camada **BRONZE** (Raw).
3. **Trata** e aplica regras de *Data Quality* criando a camada **SILVER** (Trusted).
4. **Modela** os dados no formato Estrela (Ralph Kimball) criando tabelas Fato e Dimensão na camada **GOLD**.
5. **Automatiza** todo o processo através do recurso de **Jobs & Pipelines** do Databricks de forma sequencial.

## ⚙️ Tecnologias Utilizadas

* **Databricks:** Plataforma unificada de Analytics baseada em Apache Spark.
* **Delta Lake:** Formato de armazenamento open-source que traz transações ACID para Data Lakes.
* **PySpark:** API em Python para processamento distribuído no Apache Spark.
* **MkDocs:** Gerador de sites estáticos voltado para documentação de projetos de software.
