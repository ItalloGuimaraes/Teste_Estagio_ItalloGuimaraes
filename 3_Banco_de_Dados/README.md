# Teste 3: Banco de Dados e Análise SQL

Este módulo é responsável pela estruturação do armazenamento de dados, implementação de pipelines de carga (ETL) via SQL e desenvolvimento de consultas analíticas para responder a perguntas estratégicas de negócio.

## 📋 Funcionalidades Implementadas

1.  **Modelagem de Dados:** Definição de esquema relacional (DDL) otimizado para integridade transacional e performance de leitura.
2.  **ETL via SQL:** Scripts de importação (`LOAD DATA`) que tratam inconsistências de formatação (datas, pontuação decimal e encoding) durante a carga.
3.  **Análise de Negócio:** Queries complexas utilizando *Window Functions* e *CTEs* para métricas de crescimento e distribuição geográfica.

---

## ⚖️ Decisões Técnicas e Trade-offs (Análise Crítica)

Conforme solicitado no desafio, abaixo estão as justificativas para as escolhas de arquitetura e implementação no banco de dados.

### 1. Modelagem: Normalização vs Desnormalização
**Cenário:** Armazenar dados cadastrais de operadoras e milhões de registros de despesas.
* **Estratégia Escolhida:** Modelo Híbrido (*Snowflake Schema* simplificado).
* **Justificativa:**
    * **Normalização (Tabelas `fato_despesas` e `dim_operadoras`):** Separei os dados cadastrais (Razão Social, UF) dos financeiros. Como a Razão Social se repete milhões de vezes, normalizar economiza espaço e facilita atualizações cadastrais (3FN).
    * **Desnormalização (Tabela `agg_despesas_uf`):** Mantive a tabela agregada (gerada no Teste 2) separada. Isso evita recálculos custosos de `SUM/AVG` em relatórios de acesso frequente, priorizando a velocidade de leitura.

### 2. Tipos de Dados (Precisão e Performance)
**Cenário:** Definir tipos para valores monetários e datas.
* **Estratégia Escolhida:** `DECIMAL(18,2)` e `DATE`.
* **Justificativa:**
    * **Dinheiro:** Preterido o uso de `FLOAT` ou `DOUBLE` para evitar erros de arredondamento binário. O `DECIMAL` garante a precisão exata dos centavos exigida em auditorias financeiras.
    * **Datas:** Preterido o uso de `VARCHAR`. O tipo `DATE` ocupa menos espaço (3 bytes) e permite indexação temporal e funções nativas (`DATEDIFF`, `YEAR`), essenciais para a performance da Query 1.

### 3. Estratégia de Importação (ETL)
**Cenário:** Arquivos CSV com formatação brasileira (DD/MM/AAAA, vírgula decimal) incompatível com o padrão SQL.
* **Estratégia Escolhida:** `LOAD DATA LOCAL INFILE` com variáveis de sessão (`@variavel`).
* **Justificativa:**
    * **Performance:** A inserção em lote (*bulk insert*) é ordens de magnitude mais rápida que `INSERT` linha a linha.
    * **Sanitização:** Tratamos as inconsistências (conversão de data e troca de vírgula por ponto) *on-the-fly* durante a carga, garantindo que o dado só entre no banco se estiver limpo.

### 4. Lógica de Queries Analíticas
**Cenário:** Calcular crescimento percentual ignorando trimestres sem dados ("buracos" no histórico).
* **Estratégia Escolhida:** *Window Functions* (`FIRST_VALUE` ordenado por data).
* **Justificativa:**
    * **Robustez:** Identificamos dinamicamente o primeiro e o último registro real de cada operadora em uma única passagem (scan), sem a necessidade de *Self-Joins* complexos e lentos.

---

## 🚀 Como Executar

Este módulo requer um servidor **MySQL 8.0+** e depende dos arquivos gerados nos Testes 1 e 2.

1.  **Pré-requisitos:**
    * Habilite a carga de arquivos locais no seu cliente MySQL: `local_infile=1`.
    * Certifique-se de que os Testes 1 e 2 foram executados (os CSVs são dependências).

2.  **Execute os scripts na ordem:**
    ```sql
    source 1_create_tables.sql;      -- Cria a estrutura
    source 2_import_data.sql;        -- Carrega e limpa os dados
    source 3_queries_analiticas.sql; -- Executa os relatórios
    ```

3.  **Resultado:**
    O console exibirá o status da importação e os resultados tabulares das 3 queries solicitadas.

---

## 📂 Estrutura do Módulo

Os scripts SQL foram numerados sequencialmente para garantir a ordem lógica de execução (DDL -> DML -> DQL).

```text
3_Banco_de_Dados/
│
├── 1_create_tables.sql      # DDL: Definição do Schema, Tabelas e Índices
├── 2_import_data.sql        # DML: Script de Carga e Tratamento de Dados (ETL)
├── 3_queries_analiticas.sql # DQL: Consultas Analíticas (Respostas do Teste)
└── README.md                # Documentação técnica e justificativas de arquitetura
```

## 👤 Autor: Ítallo de Santana Guimarães