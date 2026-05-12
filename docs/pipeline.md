# Jobs & Pipelines (Automação)

Para garantir que o nosso Data Lakehouse seja atualizado de forma consistente, utilizamos o recurso **Workflows (Jobs & Pipelines)** do Databricks.

Conforme solicitado nos requisitos do projeto, o trabalho não consiste apenas em notebooks soltos, mas sim em um **Pipeline Automatizado** onde as execuções estão encadeadas sequencialmente.

## 🔄 Fluxo de Execução do Job

Criamos um Job no Databricks chamado `pipeline_lakehouse_olist` contendo as seguintes *Tasks* encadeadas:

1. **Task 1 (Setup):** Executa o notebook `001_preparando_ambiente.py` (Garante que os schemas e volumes existam).
2. **Task 2 (Ingestão):** Executa o notebook `002_bronze_olist.py` (Lê de Landing e grava em Bronze). Depende da Task 1.
3. **Task 3 (Data Quality):** Executa o notebook `003_silver_olist.py` (Aplica qualidade e grava em Silver). Depende da Task 2.
4. **Task 4 (Modelagem):** Executa o notebook `004_gold_olist.py` (Gera o Star Schema e grava em Gold). Depende da Task 3.

## 📊 Vantagens da Orquestração
* **Dependência:** Uma etapa só inicia se a anterior tiver sucesso. Se a ingestão falhar, as regras de Data Quality não rodam com dados quebrados.
* **Monitoramento:** O Databricks fornece logs e histórico de duração de cada uma das tasks.
* **Isolamento:** Cada notebook roda em um contexto limpo, utilizando os clusters configurados na Job.
