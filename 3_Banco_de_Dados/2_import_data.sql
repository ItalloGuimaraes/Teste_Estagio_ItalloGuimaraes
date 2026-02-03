-- DESCRIÇÃO: Scripts de Importação (ETL via SQL)

USE teste_itallo_guimaraes;

-- ----------------------------------------------------------------------------
-- 1. IMPORTAÇÃO OPERADORAS
-- Fonte: Arquivo processado no Teste 2 (operadoras_ativas.csv)
-- ----------------------------------------------------------------------------
LOAD DATA LOCAL INFILE '../2_Transformacao_Validacao/data/operadoras_ativas.csv' 
INTO TABLE dim_operadoras
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(cnpj, registro_ans, razao_social, @col_uf, modalidade) 
SET 

    uf = NULLIF(@col_uf, '');

-- ----------------------------------------------------------------------------
-- 2. IMPORTAÇÃO DESPESAS 
-- Fonte: Consolidado do Teste 1
-- ----------------------------------------------------------------------------
LOAD DATA LOCAL INFILE '../1_Leitura_Transformacao_Dados/consolidado_despesas.csv'
INTO TABLE fato_despesas
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@col_cnpj, @col_razao, @col_trim, @col_ano, @col_valor, @col_data)
SET 
    cnpj_operadora = REPLACE(REPLACE(REPLACE(@col_cnpj, '.', ''), '/', ''), '-', ''),
    data_evento = STR_TO_DATE(@col_data, '%d/%m/%Y'),
    valor_despesa = CAST(REPLACE(REPLACE(@col_valor, '.', ''), ',', '.') AS DECIMAL(18,2)),
    trimestre = @col_trim,
    ano = @col_ano;

-- ----------------------------------------------------------------------------
-- 3. IMPORTAÇÃO AGREGADA
-- Fonte: Resultado do Teste 2
-- ----------------------------------------------------------------------------
LOAD DATA LOCAL INFILE '../2_Transformacao_Validacao/despesas_agregadas.csv'
INTO TABLE agg_despesas_uf
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(razao_social, registro_ans, modalidade, uf, @col_total, @col_media, @col_std, qtd_registros)
SET 
    despesa_total = CAST(@col_total AS DECIMAL(18,2)),
    media_trimestral = CAST(@col_media AS DECIMAL(18,2)),
    desvio_padrao = CAST(@col_std AS DECIMAL(18,2));

-- AUDITORIA
SELECT 'Operadoras Importadas' AS status, COUNT(*) FROM dim_operadoras;