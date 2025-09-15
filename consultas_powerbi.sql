-- ====================================
-- CONSULTAS ÚTEIS PARA POWER BI E DBEAVER
-- ====================================

-- ====================================
-- CONSULTAS BÁSICAS PARA DBEAVER
-- ====================================

-- 1. VISÃO GERAL DAS TABELAS
SELECT 'ativos' as tabela, COUNT(*) as registros FROM ativos
UNION ALL
SELECT 'cotacoes' as tabela, COUNT(*) as registros FROM cotacoes
UNION ALL
SELECT 'dividendos' as tabela, COUNT(*) as registros FROM dividendos;

-- 2. ATIVOS MAIS NEGOCIADOS (TOP 20)
SELECT 
    a.codigo,
    a.nome,
    a.tipo,
    a.setor,
    SUM(c.volume_financeiro) as volume_total,
    COUNT(*) as dias_negociados
FROM cotacoes c
JOIN ativos a ON c.id_ativo = a.id
GROUP BY a.codigo, a.nome, a.tipo, a.setor
ORDER BY volume_total DESC
LIMIT 20;

-- 3. ANÁLISE DE DIVIDENDOS COM YIELD
SELECT 
    a.codigo,
    a.nome,
    d.data,
    d.valor,
    d.tipo,
    c.preco_fechamento,
    ROUND((d.valor / c.preco_fechamento * 100), 2) as yield_percent
FROM dividendos d
JOIN ativos a ON d.id_ativo = a.id
LEFT JOIN cotacoes c ON c.id_ativo = a.id 
    AND c.data = (SELECT MAX(data) FROM cotacoes WHERE id_ativo = a.id)
ORDER BY d.data DESC, yield_percent DESC;

-- ====================================
-- CONSULTAS PARA POWER BI
-- ====================================

-- 1. VERIFICAR DADOS DISPONÍVEIS
-- ====================================

-- Contar registros por tabela
    SELECT 'ativos' as tabela, COUNT(*) as registros
    FROM ativos
UNION ALL
    SELECT 'cotacoes' as tabela, COUNT(*) as registros
    FROM cotacoes
UNION ALL
    SELECT 'dividendos' as tabela, COUNT(*) as registros
    FROM dividendos
UNION ALL
    SELECT 'carteira' as tabela, COUNT(*) as registros
    FROM carteira
UNION ALL
    SELECT 'indices' as tabela, COUNT(*) as registros
    FROM indices;

-- 2. VISÃO GERAL DA CARTEIRA
-- ====================================

-- Carteira com preços atuais
SELECT
    a.codigo,
    a.nome,
    a.tipo,
    a.setor,
    c.qtd,
    c.preco_medio,
    c.qtd * c.preco_medio as valor_investido,
    cot.preco_fechamento as preco_atual,
    c.qtd * cot.preco_fechamento as valor_atual,
    (c.qtd * cot.preco_fechamento) - (c.qtd * c.preco_medio) as ganho_perda,
    ((cot.preco_fechamento - c.preco_medio) / c.preco_medio) * 100 as rentabilidade_pct
FROM carteira c
    JOIN ativos a ON c.id_ativo = a.id
    LEFT JOIN (
    SELECT DISTINCT ON (id_ativo) 
        id_ativo ,
    preco_fechamento,
    data
FROM cotacoes
    ORDER BY id_ativo, data DESC
) cot ON c.id_ativo = cot.id_ativo
ORDER BY valor_atual DESC;

-- 3. HISTÓRICO DE COTAÇÕES (ÚLTIMOS 30 DIAS)
-- ====================================

SELECT
    a.codigo,
    a.nome,
    c.data,
    c.preco_abertura,
    c.preco_fechamento,
    c.maximo,
    c.minimo,
    c.volume_financeiro,
    c.negocios
FROM cotacoes c
    JOIN ativos a ON c.id_ativo = a.id
WHERE c.data >= CURRENT_DATE - INTERVAL
'30 days'
ORDER BY a.codigo, c.data;

-- 4. DIVIDENDOS POR ATIVO (ÚLTIMO ANO)
-- ====================================

SELECT
    a.codigo,
    a.nome,
    d.data,
    d.valor,
    d.tipo,
    SUM(d.valor) OVER (PARTITION BY a.codigo ORDER BY d.data) as acumulado
FROM dividendos d
    JOIN ativos a ON d.id_ativo = a.id
WHERE d.data >= CURRENT_DATE - INTERVAL
'1 year'
ORDER BY a.codigo, d.data DESC;

-- 5. PERFORMANCE POR SETOR
-- ====================================

SELECT
    a.setor,
    COUNT(DISTINCT a.id) as qtd_ativos,
    AVG(((cot.preco_fechamento - c.preco_medio) / c.preco_medio) * 100) as rentabilidade_media,
    SUM(c.qtd * c.preco_medio) as valor_investido_setor,
    SUM(c.qtd * cot.preco_fechamento) as valor_atual_setor
FROM carteira c
    JOIN ativos a ON c.id_ativo = a.id
    LEFT JOIN (
    SELECT DISTINCT ON (id_ativo) 
        id_ativo ,
    preco_fechamento
FROM cotacoes
    ORDER BY id_ativo, data DESC
) cot ON c.id_ativo = cot.id_ativo
WHERE a.setor IS NOT NULL
GROUP BY a.setor
ORDER BY valor_atual_setor DESC;

-- 6. TOP 10 MAIORES POSIÇÕES
-- ====================================

SELECT
    a.codigo,
    a.nome,
    c.qtd * cot.preco_fechamento as valor_posicao,
    ((cot.preco_fechamento - c.preco_medio) / c.preco_medio) * 100 as rentabilidade
FROM carteira c
    JOIN ativos a ON c.id_ativo = a.id
    LEFT JOIN (
    SELECT DISTINCT ON (id_ativo) 
        id_ativo ,
    preco_fechamento
FROM cotacoes
    ORDER BY id_ativo, data DESC
) cot ON c.id_ativo = cot.id_ativo
ORDER BY valor_posicao DESC
LIMIT 10;

-- 7. EVOLUÇÃO MENSAL DA CARTEIRA
-- ====================================

SELECT
    DATE_TRUNC('month', c.data) as mes,
    AVG(c.preco_fechamento) as preco_medio_mes,
    SUM(c.volume_financeiro) as volume_total_mes
FROM cotacoes c
    JOIN carteira cart ON c.id_ativo = cart.id_ativo
WHERE c.data >= CURRENT_DATE - INTERVAL
'12 months'
GROUP BY DATE_TRUNC
('month', c.data)
ORDER BY mes;

-- 8. ATIVOS MAIS NEGOCIADOS
-- ====================================

SELECT
    a.codigo,
    a.nome,
    AVG(c.volume_financeiro) as volume_medio_diario,
    AVG(c.negocios) as negocios_medio_diario,
    COUNT(*) as dias_negociacao
FROM cotacoes c
    JOIN ativos a ON c.id_ativo = a.id
WHERE c.data >= CURRENT_DATE - INTERVAL
'30 days'
GROUP BY a.codigo, a.nome
HAVING COUNT
(*) >= 10  -- Pelo menos 10 dias de negociação
ORDER BY volume_medio_diario DESC
LIMIT 20;

-- 9. DIVIDEND YIELD POR ATIVO
-- ====================================

SELECT
    a.codigo,
    a.nome,
    SUM(d.valor) as dividendos_12m,
    cot.preco_fechamento as preco_atual,
    (SUM(d.valor) / cot.preco_fechamento) * 100 as dividend_yield
FROM dividendos d
    JOIN ativos a ON d.id_ativo = a.id
    LEFT JOIN (
    SELECT DISTINCT ON (id_ativo) 
        id_ativo ,
    preco_fechamento
    FROM cotacoes
ORDER BY id_ativo, data DESC
) cot ON d.id_ativo = cot.id_ativo
WHERE d.data >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY a.codigo, a.nome, cot.preco_fechamento
HAVING SUM
(d.valor) > 0
ORDER BY dividend_yield DESC;

-- 10. RESUMO EXECUTIVO
-- ====================================

    SELECT
        'Valor Total Investido' as metrica,
        'R$ ' || TO_CHAR(SUM(c.qtd * c.preco_medio), 'FM999,999,999.00') as valor
    FROM carteira c
UNION ALL
    SELECT
        'Valor Atual da Carteira' as metrica,
        'R$ ' || TO_CHAR(SUM(c.qtd * cot.preco_fechamento), 'FM999,999,999.00') as valor
    FROM carteira c
        LEFT JOIN (
    SELECT DISTINCT ON (id_ativo) 
        id_ativo ,
        preco_fechamento
FROM cotacoes
    ORDER BY id_ativo, data DESC
) cot ON c.id_ativo = cot.id_ativo
UNION ALL
SELECT
    'Rentabilidade Total' as metrica,
    TO_CHAR(
        ((SUM(c.qtd * cot.preco_fechamento) - SUM(c.qtd * c.preco_medio)) / 
         SUM(c.qtd * c.preco_medio)) * 100, 
        'FM999.00'
    ) || '%' as valor
FROM carteira c
    LEFT JOIN (
    SELECT DISTINCT ON (id_ativo) 
        id_ativo ,
    preco_fechamento
FROM cotacoes
    ORDER BY id_ativo, data DESC
) cot ON c.id_ativo = cot.id_ativo
UNION ALL
SELECT
    'Total de Ativos' as metrica,
    COUNT(*)
::text as valor
FROM ativos
UNION ALL
SELECT
    'Dias com Cotações' as metrica,
    COUNT(DISTINCT data)
::text as valor
FROM cotacoes;
