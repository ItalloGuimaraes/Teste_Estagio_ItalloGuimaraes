-- DESCRIÇÃO: Estrutura DDL para o Teste 3
-- DATABASE: MySQL 8.0+

CREATE DATABASE IF NOT EXISTS teste_itallo_guimaraes;
USE teste_itallo_guimaraes;

-- ----------------------------------------------------------------------------
-- 1. TABELA DIMENSÃO: OPERADORAS (Origem: CADOP)
-- Justificativa: Normalização (3FN). Dados cadastrais não devem se repetir 
-- na tabela de fatos (despesas) para economizar espaço e facilitar updates.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_operadoras (
    registro_ans VARCHAR(10) PRIMARY KEY, -- Chave Primária Natural
    cnpj VARCHAR(14) NOT NULL UNIQUE,     -- Índice Unique para garantir integridade
    razao_social VARCHAR(255) NOT NULL,
    modalidade VARCHAR(100),
    uf CHAR(2),
    INDEX idx_uf (uf)                     -- Índice para acelerar filtros por Estado
);

-- ----------------------------------------------------------------------------
-- 2. TABELA FATO: DESPESAS (Origem: Consolidado Teste 1)
-- Justificativa Tipos de Dados:
-- DECIMAL(15,2): Float tem problemas de precisão para dinheiro. Decimal é exato.
-- DATE: Melhor que VARCHAR para permitir funções de data (DATEDIFF, MONTH, etc).
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS fato_despesas (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    cnpj_operadora VARCHAR(14),           -- FK para Operadoras (via CNPJ)
    data_evento DATE NOT NULL,
    trimestre INT NOT NULL,
    ano INT NOT NULL,
    valor_despesa DECIMAL(18,2) NOT NULL,
    
    -- Índices de Performance (Trade-off: Insert mais lento, Select muito mais rápido)
    INDEX idx_data (data_evento),
    INDEX idx_cnpj (cnpj_operadora),
    
    -- Constraint (Integridade Referencial)
    CONSTRAINT fk_despesa_operadora 
        FOREIGN KEY (cnpj_operadora) REFERENCES dim_operadoras(cnpj)
        ON DELETE CASCADE
);

-- ----------------------------------------------------------------------------
-- 3. TABELA AGREGADA (Origem: Teste 2)
-- Justificativa: Tabela Desnormalizada (Data Mart) para performance em leitura.
-- Evita refazer o JOIN pesado e o GROUP BY toda vez que precisar do relatório.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS agg_despesas_uf (
    razao_social VARCHAR(255),
    registro_ans VARCHAR(10),
    modalidade VARCHAR(100),
    uf CHAR(2),
    despesa_total DECIMAL(18,2),
    media_trimestral DECIMAL(18,2),
    desvio_padrao DECIMAL(18,2),
    qtd_registros INT,
    
    PRIMARY KEY (registro_ans, uf) -- Chave Composta
);