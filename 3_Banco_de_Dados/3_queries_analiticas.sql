-- DESCRIÇÃO: Respostas para as perguntas de negócio (Queries 1, 2 e 3)

USE teste_itallo_guimaraes;

-- ----------------------------------------------------------------------------
-- QUERY 1: Top 5 operadoras com maior crescimento percentual de despesas
-- (Último Trimestre vs Primeiro Trimestre)
--
-- Desafio: Operadoras sem dados em todos os trimestres.
-- Solução: Window Functions para pegar a PRIMEIRA e a ÚLTIMA data disponível
-- para cada operadora, independente de buracos no meio. Filtra quem só tem 1 data.
-- ----------------------------------------------------------------------------
WITH limites_operadora AS (
    -- Passo 1: Identificar valor do primeiro e último registro de cada operadora
    SELECT 
        d.cnpj_operadora,
        o.razao_social,
        -- Pega o valor da data mais antiga
        FIRST_VALUE(d.valor_despesa) OVER (PARTITION BY d.cnpj_operadora ORDER BY d.data_evento ASC) as valor_inicial,
        -- Pega o valor da data mais recente
        FIRST_VALUE(d.valor_despesa) OVER (PARTITION BY d.cnpj_operadora ORDER BY d.data_evento DESC) as valor_final,
        -- Conta quantos trimestres distintos existem (para evitar cálculo com 1 só ponto)
        COUNT(DISTINCT d.trimestre) OVER (PARTITION BY d.cnpj_operadora) as qtd_trimestres
    FROM fato_despesas d
    JOIN dim_operadoras o ON d.cnpj_operadora = o.cnpj
)
SELECT DISTINCT
    razao_social,
    valor_inicial,
    valor_final,
    -- Fórmula de Crescimento: ((Final - Inicial) / Inicial) * 100
    ROUND(((valor_final - valor_inicial) / valor_inicial) * 100, 2) as crescimento_pct
FROM limites_operadora
WHERE qtd_trimestres > 1         -- Garante que tem começo e fim
  AND valor_inicial > 0          -- Evita divisão por zero
ORDER BY crescimento_pct DESC
LIMIT 5;

-- ----------------------------------------------------------------------------
-- QUERY 2: Top 5 UFs com maiores despesas totais + Média por operadora
--
-- Desafio Adicional: Média de despesas por operadora em cada UF.
-- ----------------------------------------------------------------------------
SELECT 
    o.uf,
    SUM(d.valor_despesa) as despesa_total_estado,
    COUNT(DISTINCT d.cnpj_operadora) as qtd_operadoras_atuantes,
    -- Média = Total do Estado / Número de Operadoras naquele Estado
    ROUND(SUM(d.valor_despesa) / NULLIF(COUNT(DISTINCT d.cnpj_operadora), 0), 2) as media_por_operadora
FROM fato_despesas d
JOIN dim_operadoras o ON d.cnpj_operadora = o.cnpj
WHERE o.uf IS NOT NULL
GROUP BY o.uf
ORDER BY despesa_total_estado DESC
LIMIT 5;

-- ----------------------------------------------------------------------------
-- QUERY 3: Operadoras com despesas acima da média geral em >= 2 trimestres
--
-- Trade-off Técnico: Utilizei CTE + Função de Janela (AVG OVER) em vez de Subquery simples.
-- Justificativa: Window Functions calculam a média geral uma única vez.
-- ----------------------------------------------------------------------------
WITH medias_trimestrais AS (
    -- Calcula a média do mercado para cada trimestre/ano
    SELECT 
        ano, 
        trimestre, 
        AVG(valor_despesa) as media_mercado
    FROM fato_despesas
    GROUP BY ano, trimestre
),
performance_operadora AS (
    -- Compara cada despesa da operadora com a média do mercado daquele trimestre
    SELECT 
        d.cnpj_operadora,
        d.ano,
        d.trimestre,
        CASE WHEN d.valor_despesa > m.media_mercado THEN 1 ELSE 0 END as acima_da_media
    FROM fato_despesas d
    JOIN medias_trimestrais m ON d.ano = m.ano AND d.trimestre = m.trimestre
)
SELECT 
    o.razao_social,
    SUM(p.acima_da_media) as trimestres_acima_media
FROM performance_operadora p
JOIN dim_operadoras o ON p.cnpj_operadora = o.cnpj
GROUP BY o.razao_social
HAVING trimestres_acima_media >= 2
ORDER BY trimestres_acima_media DESC;