# Arquitetura Medalhão e Modelagem

O processamento dos dados foi dividido em camadas lógicas dentro do Databricks, evoluindo a qualidade do dado a cada etapa. Todo o armazenamento a partir da camada Bronze utiliza o formato **Delta Lake**.

## 🥉 Camada Bronze (Raw)
A ingestão lê os arquivos CSV do schema `LANDING/DADOS` e os salva como tabelas Delta Lake no schema `BRONZE`. 
Nesta camada, os dados estão no seu formato bruto, mas com os benefícios de performance e versionamento do Delta. Adicionamos também metadados de auditoria, como `dt_ingestao` e `nm_arquivo_origem`.

## 🥈 Camada Silver (Cleansed / Data Quality)
No *Notebook 003*, lemos os dados do schema BRONZE e aplicamos regras de **Data Quality**. 
As validações e limpezas realizadas incluem:
* Remoção de registros duplicados;
* Tratamento de valores nulos (Nulls);
* Padronização de strings e formatos de data;
* Tipagem correta das colunas (casting).
O resultado é salvo em tabelas confiáveis no schema `SILVER`.

## 🥇 Camada Gold (Dimensional / Ralph Kimball)
Por fim, no *Notebook 004*, lemos os dados do schema SILVER e aplicamos a **Modelagem Dimensional** baseada na metodologia de **Ralph Kimball** (Star Schema).
Criamos o schema `GOLD` contendo as seguintes tabelas otimizadas para consultas analíticas e BI:

### Tabelas Dimensão (Contexto)
* `dim_cliente`: Dados demográficos e de localização dos clientes.
* `dim_produto`: Detalhes do produto, dimensões, peso e categoria traduzida.
* `dim_vendedor`: Dados e localização dos parceiros de venda.
* `dim_data`: Calendário contendo os atributos de tempo dos pedidos.

### Tabela Fato (Métricas)
* `fato_pedido`: Tabela central contendo as chaves estrangeiras (FKs) que ligam às dimensões e as métricas de negócio (valor do produto, valor do frete, valor do pagamento, nota da avaliação).
