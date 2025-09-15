# 🗄️ **TUTORIAL COMPLETO: ANÁLISE DE DADOS COM DBEAVER**

## 🎯 **SISTEMA B3 → DBEAVER**

Este tutorial mostra como usar o DBeaver para analisar os dados coletados do Sistema B3 de forma simples e eficiente.

---

## 🚀 **PASSO 1: PREPARAR OS DADOS**

### **1.1 Executar Coleta de Dados**
```bash
# No terminal do projeto
python main.py
# Escolher: 5 - Executar coleta de dados
```

**Aguarde a coleta finalizar** - serão coletados ~11.500 ativos e cotações da B3.

### **1.2 Verificar se Docker está rodando**
```bash
docker ps
```
**Deve mostrar:** Container PostgreSQL ativo na porta 5432.

---

## 📥 **PASSO 2: INSTALAR E CONFIGURAR DBEAVER**

### **2.1 Download DBeaver**
- **Site oficial**: https://dbeaver.io/download/
- **Versão recomendada**: DBeaver Community Edition (gratuita)
- **Instalar** e executar

### **2.2 Criar Nova Conexão**
1. Abrir **DBeaver**
2. Clicar em **"Nova Conexão"** (ícone de plugue + ou Ctrl+Shift+N)
3. Selecionar **"PostgreSQL"**
4. Clicar **"Avançar"**

### **2.3 Configurar Conexão**
```
Host: localhost
Port: 5432
Database: b3
Username: admin
Password: admin
```

### **2.4 Testar Conexão**
1. Clicar em **"Test Connection"**
2. **Se aparecer erro**: Baixar driver PostgreSQL automaticamente
3. **Se OK**: Clicar **"Finish"**

### **2.5 Verificar Conexão**
Na árvore à esquerda, você deve ver:
```
PostgreSQL - b3
├── Databases
│   └── b3
│       └── Schemas
│           └── public
│               └── Tables
│                   ├── ativos (11.500+ registros)
│                   ├── cotacoes (11.500+ registros)
│                   └── dividendos (50+ registros)
```

---

## 📊 **PASSO 3: CONSULTAS BÁSICAS DE EXPLORAÇÃO**

### **3.1 Visão Geral do Sistema**
```sql
-- Contar registros por tabela
SELECT 'ativos' as tabela, COUNT(*) as registros FROM ativos
UNION ALL
SELECT 'cotacoes' as tabela, COUNT(*) as registros FROM cotacoes
UNION ALL
SELECT 'dividendos' as tabela, COUNT(*) as registros FROM dividendos
ORDER BY registros DESC;
```

**Como executar:**
1. **Botão direito** na conexão → **"SQL Editor"** → **"New SQL Script"**
2. **Colar** a consulta
3. **Ctrl+Enter** ou clicar no ícone ▶️

### **3.2 Explorar Estrutura das Tabelas**
```sql
-- Ver estrutura da tabela ativos
SELECT 
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'ativos'
ORDER BY ordinal_position;
```

### **3.3 Primeiros Registros**
```sql
-- Ver primeiros 10 ativos
SELECT * FROM ativos LIMIT 10;

-- Ver primeiras 10 cotações
SELECT * FROM cotacoes LIMIT 10;

-- Ver primeiros dividendos
SELECT * FROM dividendos LIMIT 10;
```

---

## 📈 **PASSO 4: ANÁLISES ESSENCIAIS**

### **📊 ANÁLISE 1: TOP 20 ATIVOS MAIS NEGOCIADOS**
```sql
SELECT 
    a.codigo,
    a.nome,
    a.tipo,
    a.setor,
    SUM(c.volume_financeiro) as volume_total,
    COUNT(*) as dias_negociados,
    AVG(c.preco_fechamento) as preco_medio
FROM cotacoes c
JOIN ativos a ON c.id_ativo = a.id
GROUP BY a.codigo, a.nome, a.tipo, a.setor
ORDER BY volume_total DESC
LIMIT 20;
```

**Resultado esperado:** Lista das 20 ações mais negociadas (PETR4, VALE3, ITUB4, etc.)

### **📈 ANÁLISE 2: COTAÇÕES MAIS RECENTES**
```sql
SELECT 
    a.codigo,
    a.nome,
    a.tipo,
    c.data,
    c.preco_fechamento,
    c.volume_financeiro,
    c.negocios,
    CASE 
        WHEN c.volume_financeiro > 1000000 THEN 'Alto Volume'
        WHEN c.volume_financeiro > 100000 THEN 'Médio Volume'
        ELSE 'Baixo Volume'
    END as classificacao_volume
FROM cotacoes c
JOIN ativos a ON c.id_ativo = a.id
WHERE c.data = (SELECT MAX(data) FROM cotacoes)
ORDER BY c.volume_financeiro DESC
LIMIT 50;
```

### **🏭 ANÁLISE 3: PERFORMANCE POR SETOR**
```sql
SELECT 
    a.setor,
    COUNT(DISTINCT a.id) as total_ativos,
    ROUND(AVG(c.preco_fechamento), 2) as preco_medio,
    ROUND(SUM(c.volume_financeiro)/1000000, 2) as volume_milhoes,
    ROUND(AVG(c.volume_financeiro), 0) as volume_medio_por_ativo
FROM cotacoes c
JOIN ativos a ON c.id_ativo = a.id
WHERE c.data = (SELECT MAX(data) FROM cotacoes)
    AND a.setor IS NOT NULL
GROUP BY a.setor
HAVING COUNT(DISTINCT a.id) >= 5  -- Setores com pelo menos 5 ativos
ORDER BY volume_milhoes DESC;
```

### **💰 ANÁLISE 4: DIVIDENDOS COM YIELD**
```sql
SELECT 
    a.codigo,
    a.nome,
    a.tipo,
    d.data as data_pagamento,
    d.valor as dividendo,
    d.tipo as tipo_provento,
    c.preco_fechamento,
    ROUND((d.valor / c.preco_fechamento * 100), 2) as yield_percent,
    CASE 
        WHEN (d.valor / c.preco_fechamento * 100) > 2 THEN '🔥 Alto Yield'
        WHEN (d.valor / c.preco_fechamento * 100) > 1 THEN '📈 Médio Yield'
        ELSE '📊 Baixo Yield'
    END as classificacao_yield
FROM dividendos d
JOIN ativos a ON d.id_ativo = a.id
LEFT JOIN cotacoes c ON c.id_ativo = a.id 
    AND c.data = (SELECT MAX(data) FROM cotacoes WHERE id_ativo = a.id)
ORDER BY yield_percent DESC NULLS LAST;
```

---

## 🎯 **PASSO 5: ANÁLISES AVANÇADAS**

### **📊 ANÁLISE 5: TOP FIIs POR RENDIMENTO**
```sql
SELECT 
    a.codigo,
    a.nome,
    COUNT(d.id) as total_pagamentos,
    ROUND(SUM(d.valor), 2) as total_dividendos,
    ROUND(AVG(d.valor), 4) as media_dividendo,
    MAX(d.data) as ultimo_pagamento,
    c.preco_fechamento as preco_atual,
    ROUND((SUM(d.valor) / c.preco_fechamento * 100), 2) as yield_acumulado
FROM ativos a
JOIN dividendos d ON a.id = d.id_ativo
LEFT JOIN cotacoes c ON c.id_ativo = a.id 
    AND c.data = (SELECT MAX(data) FROM cotacoes WHERE id_ativo = a.id)
WHERE a.tipo = 'FII'
GROUP BY a.codigo, a.nome, c.preco_fechamento
HAVING COUNT(d.id) > 0
ORDER BY yield_acumulado DESC
LIMIT 15;
```

### **📈 ANÁLISE 6: EVOLUÇÃO DE PREÇOS (ÚLTIMOS 30 DIAS)**
```sql
SELECT 
    a.codigo,
    a.nome,
    c.data,
    c.preco_fechamento,
    LAG(c.preco_fechamento) OVER (PARTITION BY a.codigo ORDER BY c.data) as preco_anterior,
    ROUND(
        ((c.preco_fechamento - LAG(c.preco_fechamento) OVER (PARTITION BY a.codigo ORDER BY c.data)) 
         / LAG(c.preco_fechamento) OVER (PARTITION BY a.codigo ORDER BY c.data) * 100), 2
    ) as variacao_percent,
    c.volume_financeiro
FROM cotacoes c
JOIN ativos a ON c.id_ativo = a.id
WHERE c.data >= CURRENT_DATE - INTERVAL '30 days'
    AND a.codigo IN ('PETR4', 'VALE3', 'ITUB4', 'BBDC4', 'ABEV3')
ORDER BY a.codigo, c.data DESC;
```

### **🏆 ANÁLISE 7: RANKING COMPLETO DE ATIVOS**
```sql
WITH ranking_ativos AS (
    SELECT 
        a.codigo,
        a.nome,
        a.tipo,
        a.setor,
        c.preco_fechamento,
        c.volume_financeiro,
        c.negocios,
        COALESCE(d.total_dividendos, 0) as total_dividendos,
        COALESCE(d.yield_percent, 0) as yield_percent,
        ROW_NUMBER() OVER (ORDER BY c.volume_financeiro DESC) as rank_volume,
        ROW_NUMBER() OVER (ORDER BY COALESCE(d.yield_percent, 0) DESC) as rank_yield
    FROM cotacoes c
    JOIN ativos a ON c.id_ativo = a.id
    LEFT JOIN (
        SELECT 
            id_ativo,
            SUM(valor) as total_dividendos,
            AVG(valor) as yield_percent
        FROM dividendos 
        GROUP BY id_ativo
    ) d ON a.id = d.id_ativo
    WHERE c.data = (SELECT MAX(data) FROM cotacoes)
)
SELECT 
    codigo,
    nome,
    tipo,
    setor,
    ROUND(preco_fechamento, 2) as preco,
    ROUND(volume_financeiro/1000000, 2) as volume_milhoes,
    negocios,
    ROUND(total_dividendos, 4) as dividendos,
    ROUND(yield_percent, 2) as yield_pct,
    rank_volume,
    rank_yield,
    CASE 
        WHEN rank_volume <= 50 AND rank_yield <= 50 THEN '⭐ Top Volume + Yield'
        WHEN rank_volume <= 100 THEN '📊 Alto Volume'
        WHEN rank_yield <= 100 THEN '💰 Bom Yield'
        ELSE '📈 Outros'
    END as classificacao
FROM ranking_ativos
ORDER BY volume_financeiro DESC
LIMIT 100;
```

---

## 📊 **PASSO 6: VISUALIZAÇÕES NO DBEAVER**

### **6.1 Gráficos Básicos**
1. **Executar consulta** (ex: TOP 20 ativos)
2. **Botão direito** no resultado → **"View/Format"** → **"Charts"**
3. **Escolher tipo**: Barras, Pizza, Linha
4. **Configurar eixos**: X (código), Y (volume)

### **6.2 Exportar Resultados**
1. **Executar consulta**
2. **Botão direito** no resultado → **"Export Data"**
3. **Formatos disponíveis**: CSV, Excel, JSON, XML
4. **Configurar** colunas e filtros

### **6.3 Salvar Consultas Favoritas**
1. **Criar pasta**: Botão direito → **"Create Folder"** → "Análises B3"
2. **Salvar script**: Ctrl+S → Nomear (ex: "TOP_ATIVOS_VOLUME")
3. **Organizar** por categoria (Dividendos, Performance, etc.)

---

## 🎨 **PASSO 7: DASHBOARDS PERSONALIZADOS**

### **7.1 Criar Dashboard Simples**
```sql
-- DASHBOARD B3 - VISÃO GERAL
-- =============================

-- 1. RESUMO GERAL
SELECT 
    'RESUMO DO SISTEMA B3' as titulo,
    (SELECT COUNT(*) FROM ativos) as total_ativos,
    (SELECT COUNT(*) FROM cotacoes) as total_cotacoes,
    (SELECT COUNT(*) FROM dividendos) as total_dividendos,
    (SELECT MAX(data) FROM cotacoes) as ultima_atualizacao;

-- 2. TOP 10 VOLUMES
SELECT 
    '📊 TOP 10 VOLUMES' as secao,
    a.codigo,
    a.nome,
    ROUND(c.volume_financeiro/1000000, 2) as volume_milhoes
FROM cotacoes c
JOIN ativos a ON c.id_ativo = a.id
WHERE c.data = (SELECT MAX(data) FROM cotacoes)
ORDER BY c.volume_financeiro DESC
LIMIT 10;

-- 3. DISTRIBUIÇÃO POR TIPO
SELECT 
    '🥧 DISTRIBUIÇÃO POR TIPO' as secao,
    tipo,
    COUNT(*) as quantidade,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM ativos), 2) as percentual
FROM ativos
WHERE tipo IS NOT NULL
GROUP BY tipo
ORDER BY quantidade DESC;

-- 4. TOP 5 SETORES
SELECT 
    '🏭 TOP 5 SETORES' as secao,
    a.setor,
    COUNT(*) as total_ativos,
    ROUND(SUM(c.volume_financeiro)/1000000, 2) as volume_total_milhoes
FROM cotacoes c
JOIN ativos a ON c.id_ativo = a.id
WHERE c.data = (SELECT MAX(data) FROM cotacoes)
    AND a.setor IS NOT NULL
GROUP BY a.setor
ORDER BY volume_total_milhoes DESC
LIMIT 5;
```

### **7.2 Dashboard de Dividendos**
```sql
-- DASHBOARD DIVIDENDOS
-- ====================

-- 1. ESTATÍSTICAS GERAIS
SELECT 
    'DIVIDENDOS - ESTATÍSTICAS' as titulo,
    COUNT(*) as total_pagamentos,
    COUNT(DISTINCT id_ativo) as ativos_pagadores,
    ROUND(SUM(valor), 2) as total_distribuido,
    ROUND(AVG(valor), 4) as media_pagamento,
    MAX(data) as ultimo_pagamento;

-- 2. TOP PAGADORES
SELECT 
    '💰 TOP PAGADORES' as secao,
    a.codigo,
    a.nome,
    COUNT(d.id) as qtd_pagamentos,
    ROUND(SUM(d.valor), 4) as total_pago,
    MAX(d.data) as ultimo_pagamento
FROM dividendos d
JOIN ativos a ON d.id_ativo = a.id
GROUP BY a.codigo, a.nome
ORDER BY total_pago DESC
LIMIT 10;

-- 3. DIVIDENDOS POR TIPO
SELECT 
    '📊 POR TIPO DE ATIVO' as secao,
    a.tipo,
    COUNT(d.id) as total_pagamentos,
    ROUND(AVG(d.valor), 4) as media_valor
FROM dividendos d
JOIN ativos a ON d.id_ativo = a.id
GROUP BY a.tipo
ORDER BY total_pagamentos DESC;
```

---

## 🔍 **PASSO 8: CONSULTAS PARA ANÁLISE ESPECÍFICA**

### **8.1 Análise de Liquidez**
```sql
-- ANÁLISE DE LIQUIDEZ
SELECT 
    a.codigo,
    a.nome,
    a.tipo,
    COUNT(*) as dias_negociados,
    AVG(c.negocios) as media_negocios_dia,
    AVG(c.volume_financeiro) as volume_medio,
    CASE 
        WHEN AVG(c.negocios) > 1000 THEN 'Alta Liquidez'
        WHEN AVG(c.negocios) > 100 THEN 'Média Liquidez'
        ELSE 'Baixa Liquidez'
    END as classificacao_liquidez
FROM cotacoes c
JOIN ativos a ON c.id_ativo = a.id
GROUP BY a.codigo, a.nome, a.tipo
HAVING COUNT(*) >= 1  -- Pelo menos 1 dia de negociação
ORDER BY volume_medio DESC
LIMIT 50;
```

### **8.2 Análise de Volatilidade**
```sql
-- ANÁLISE DE VOLATILIDADE (Desvio Padrão dos Preços)
SELECT 
    a.codigo,
    a.nome,
    COUNT(*) as dias_cotacao,
    ROUND(AVG(c.preco_fechamento), 2) as preco_medio,
    ROUND(MIN(c.preco_fechamento), 2) as preco_minimo,
    ROUND(MAX(c.preco_fechamento), 2) as preco_maximo,
    ROUND(STDDEV(c.preco_fechamento), 2) as desvio_padrao,
    ROUND((STDDEV(c.preco_fechamento) / AVG(c.preco_fechamento) * 100), 2) as coef_variacao,
    CASE 
        WHEN (STDDEV(c.preco_fechamento) / AVG(c.preco_fechamento) * 100) > 10 THEN 'Alta Volatilidade'
        WHEN (STDDEV(c.preco_fechamento) / AVG(c.preco_fechamento) * 100) > 5 THEN 'Média Volatilidade'
        ELSE 'Baixa Volatilidade'
    END as classificacao_volatilidade
FROM cotacoes c
JOIN ativos a ON c.id_ativo = a.id
GROUP BY a.codigo, a.nome
HAVING COUNT(*) > 1
ORDER BY coef_variacao DESC
LIMIT 30;
```

### **8.3 Comparativo Setorial**
```sql
-- COMPARATIVO DETALHADO POR SETOR
WITH estatisticas_setor AS (
    SELECT 
        a.setor,
        COUNT(DISTINCT a.id) as total_ativos,
        AVG(c.preco_fechamento) as preco_medio_setor,
        SUM(c.volume_financeiro) as volume_total_setor,
        AVG(c.volume_financeiro) as volume_medio_setor,
        STDDEV(c.preco_fechamento) as volatilidade_setor
    FROM cotacoes c
    JOIN ativos a ON c.id_ativo = a.id
    WHERE c.data = (SELECT MAX(data) FROM cotacoes)
        AND a.setor IS NOT NULL
    GROUP BY a.setor
)
SELECT 
    setor,
    total_ativos,
    ROUND(preco_medio_setor, 2) as preco_medio,
    ROUND(volume_total_setor/1000000, 2) as volume_milhoes,
    ROUND(volume_medio_setor/1000, 2) as volume_medio_mil,
    ROUND(volatilidade_setor, 2) as volatilidade,
    RANK() OVER (ORDER BY volume_total_setor DESC) as rank_volume,
    RANK() OVER (ORDER BY total_ativos DESC) as rank_quantidade
FROM estatisticas_setor
WHERE total_ativos >= 3  -- Setores com pelo menos 3 ativos
ORDER BY volume_milhoes DESC;
```

---

## 🚀 **PASSO 9: AUTOMAÇÃO E PRODUTIVIDADE**

### **9.1 Scripts Salvos**
Criar uma pasta "**Scripts B3**" no DBeaver com:
- `01_Resumo_Sistema.sql`
- `02_Top_Ativos.sql`
- `03_Analise_Setorial.sql`
- `04_Dividendos.sql`
- `05_Dashboard_Completo.sql`

### **9.2 Atalhos Úteis**
- **Ctrl+Enter**: Executar consulta
- **Ctrl+Shift+Enter**: Executar consulta atual
- **F4**: Abrir editor de dados da tabela
- **Ctrl+S**: Salvar script
- **Ctrl+T**: Nova aba SQL
- **F5**: Atualizar conexão

### **9.3 Configurações Recomendadas**
1. **Window → Preferences**
2. **SQL Editor**:
   - ✅ Auto-completion enabled
   - ✅ Auto-format SQL
   - ✅ Highlight SQL syntax
3. **Result Sets**:
   - ✅ Show row numbers
   - ✅ Show column descriptions

---

## 📊 **RESULTADO FINAL**

### **Com o DBeaver você terá:**
- ✅ **Interface intuitiva** para consultas SQL
- ✅ **Visualização completa** dos dados B3
- ✅ **Gráficos básicos** integrados
- ✅ **Export** para Excel/CSV
- ✅ **Scripts organizados** por categoria
- ✅ **Análises avançadas** com SQL
- ✅ **Dashboards personalizados**

### **Vantagens sobre Power BI:**
- 🆓 **Totalmente gratuito**
- 🚀 **Mais rápido** para análises ad-hoc
- 💻 **Multiplataforma** (Windows, Mac, Linux)
- 🔧 **Controle total** sobre consultas
- 📊 **Ideal para análises exploratórias**

---

## 🔧 **TROUBLESHOOTING**

### **Erro de Conexão:**
```
Soluções:
1. Verificar Docker: docker ps
2. Verificar dados: python main.py → opção 1
3. Testar porta: telnet localhost 5432
4. Verificar firewall
```

### **Consultas Lentas:**
```
Soluções:
1. Adicionar LIMIT nas consultas
2. Filtrar por data específica
3. Usar índices nas colunas frequentes
4. Evitar JOINs desnecessários
```

### **Sem Dados:**
```
Soluções:
1. Executar coleta: python main.py → opção 5
2. Verificar logs do sistema
3. Verificar conexão com B3
4. Aguardar coleta finalizar
```

---

## 🎯 **PRÓXIMOS PASSOS**

1. **Executar coleta** de dados (python main.py → opção 5)
2. **Instalar DBeaver** e conectar
3. **Testar consultas** básicas
4. **Criar dashboards** personalizados
5. **Exportar análises** para Excel
6. **Automatizar** consultas frequentes

---

**🎉 PARABÉNS! Você tem uma ferramenta completa para análise dos dados B3!** 📊

**DBeaver + Sistema B3 = Análise Profissional de Investimentos** 🚀
