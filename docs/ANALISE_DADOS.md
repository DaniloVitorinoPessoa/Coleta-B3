# 🗄️ **ANÁLISE DE DADOS B3 - DBEAVER + POWER BI**

## 🎯 **VISÃO GERAL**

O Sistema B3 oferece múltiplas opções para análise de dados da Bolsa de Valores. **DBeaver é a ferramenta recomendada** para análise exploratória e consultas SQL, enquanto Power BI é ideal para dashboards corporativos.

---

## 📋 **PRÉ-REQUISITOS**

### **Software necessário:**
- ✅ **Sistema B3** funcionando
- ✅ **PostgreSQL** rodando (via Docker)
- ✅ **Dados coletados** (opção 5 do sistema)
- ✅ **DBeaver** (recomendado) OU **Power BI Desktop** (alternativo)

### **🥇 OPÇÃO RECOMENDADA: DBEAVER**

#### **DBeaver Community (GRATUITO) ⭐**
- **Site oficial**: https://dbeaver.io/download/
- **Tutorial completo**: [`TUTORIAL_DBEAVER.md`](TUTORIAL_DBEAVER.md)
- **Ideal para**: Consultas SQL, exploração de dados, análises ad-hoc
- **Vantagens**: Gratuito, multiplataforma, controle total sobre consultas

### **🥈 OPÇÃO ALTERNATIVA: POWER BI**

#### **Power BI Desktop (Dashboards Corporativos)**
- **Site oficial**: https://powerbi.microsoft.com/desktop/
- **Windows Store**: "Power BI Desktop"
- **Ideal para**: Dashboards corporativos, relatórios profissionais
- **Limitações**: Apenas Windows, licenças pagas para publicação

---

## 🔌 **CONEXÃO COM BANCO DE DADOS**

### **🗄️ DBEAVER (RECOMENDADO)**

#### **Passo 1: Nova Conexão**
1. Abrir **DBeaver**
2. Clicar em **"Nova Conexão"** (ícone de plugue)
3. Selecionar **"PostgreSQL"**

#### **Passo 2: Configurações de Conexão**
```
Host: localhost
Port: 5432
Database: b3
Username: admin
Password: admin
```

#### **Passo 3: Testar e Conectar**
1. Clicar em **"Test Connection"**
2. Se OK, clicar em **"Finish"**

#### **Passo 4: Verificar Dados**
Após conectar, você verá:
```
b3 (Database)
├── public (Schema)
│   ├── ativos (Table)          # ~11.500 ativos
│   ├── cotacoes (Table)        # ~11.500+ cotações
│   └── dividendos (Table)      # Dividendos/Proventos
```

#### **Vantagens do DBeaver:**
- ✅ **Gratuito** e open-source
- ✅ **Multiplataforma** (Windows, Mac, Linux)
- ✅ **Interface intuitiva** para SQL
- ✅ **Visualização de dados** em tabelas
- ✅ **Export** para CSV, Excel, etc.
- ✅ **Gráficos básicos** integrados

---

### **📊 POWER BI DESKTOP (ALTERNATIVO)**

#### **Passo 1: Obter Dados**
1. Abrir **Power BI Desktop**
2. Clicar em **"Obter Dados"**
3. Selecionar **"Banco de Dados"** → **"PostgreSQL"**

#### **Passo 2: Configurar Conexão**
```
Servidor: localhost:5432
Banco de dados: b3
```

#### **Passo 3: Credenciais**
```
Usuário: admin
Senha: admin
```

#### **Passo 4: Modo de Conectividade**
- Escolher **"DirectQuery"** para dados em tempo real
- Ou **"Importar"** para melhor performance

---

## 🚀 **PRIMEIROS PASSOS NO DBEAVER**

### **1. Executar Primeira Consulta**
Após conectar no DBeaver, teste com esta consulta:
```sql
-- Visão geral do sistema
SELECT 'ativos' as tabela, COUNT(*) as registros FROM ativos
UNION ALL
SELECT 'cotacoes' as tabela, COUNT(*) as registros FROM cotacoes
UNION ALL
SELECT 'dividendos' as tabela, COUNT(*) as registros FROM dividendos;
```

### **2. Explorar Top Ativos**
```sql
-- Top 10 ativos mais negociados
SELECT 
    a.codigo,
    a.nome,
    a.tipo,
    SUM(c.volume_financeiro) as volume_total
FROM cotacoes c
JOIN ativos a ON c.id_ativo = a.id
GROUP BY a.codigo, a.nome, a.tipo
ORDER BY volume_total DESC
LIMIT 10;
```

### **3. Ver Dados Mais Recentes**
```sql
-- Cotações da última data disponível
SELECT 
    a.codigo,
    a.nome,
    c.data,
    c.preco_fechamento,
    c.volume_financeiro
FROM cotacoes c
JOIN ativos a ON c.id_ativo = a.id
WHERE c.data = (SELECT MAX(data) FROM cotacoes)
ORDER BY c.volume_financeiro DESC
LIMIT 20;
```

### **📚 Tutorial Completo**
Para análises mais avançadas, consulte: [`TUTORIAL_DBEAVER.md`](TUTORIAL_DBEAVER.md)

---

## 🗄️ **ESTRUTURA DO BANCO DE DADOS**

### **Tabelas Principais:**

#### **1. ativos**
```sql
Colunas:
- id (int) - Chave primária
- codigo (varchar) - Código do ativo (PETR4, VALE3)
- nome (varchar) - Nome completo
- tipo (varchar) - ACAO, FII, ETF
- setor (varchar) - Setor econômico
```

#### **2. cotacoes**
```sql
Colunas:
- id (bigint) - Chave primária
- id_ativo (int) - FK para ativos
- data (date) - Data da cotação
- preco_abertura (decimal) - Preço de abertura
- preco_fechamento (decimal) - Preço de fechamento
- maximo (decimal) - Máximo do dia
- minimo (decimal) - Mínimo do dia
- negocios (int) - Quantidade de negócios
- volume_financeiro (decimal) - Volume em R$
```

#### **3. dividendos**
```sql
Colunas:
- id (bigint) - Chave primária
- id_ativo (int) - FK para ativos
- data (date) - Data do pagamento
- valor (decimal) - Valor do dividendo
- tipo (varchar) - Tipo do provento
```

---

## 🔗 **RELACIONAMENTOS**

### **Configurar no Power BI:**

```
ativos (1) ←→ (N) cotacoes
  ↑ id          ↑ id_ativo

ativos (1) ←→ (N) dividendos  
  ↑ id          ↑ id_ativo
```

### **Cardinalidade:**
- **ativos → cotacoes**: 1 para muitos
- **ativos → dividendos**: 1 para muitos

---

## 📊 **CONSULTAS ÚTEIS PARA DBEAVER**

### **🔍 Consultas Básicas de Exploração**

#### **1. Visão Geral das Tabelas**
```sql
-- Contar registros por tabela
SELECT 'ativos' as tabela, COUNT(*) as registros FROM ativos
UNION ALL
SELECT 'cotacoes' as tabela, COUNT(*) as registros FROM cotacoes
UNION ALL
SELECT 'dividendos' as tabela, COUNT(*) as registros FROM dividendos;
```

#### **2. Ativos Mais Negociados**
```sql
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
```

#### **3. Cotações Mais Recentes**
```sql
SELECT 
    a.codigo,
    a.nome,
    a.tipo,
    c.data,
    c.preco_fechamento,
    c.volume_financeiro,
    c.negocios
FROM cotacoes c
JOIN ativos a ON c.id_ativo = a.id
WHERE c.data = (SELECT MAX(data) FROM cotacoes)
ORDER BY c.volume_financeiro DESC
LIMIT 50;
```

#### **4. Análise de Dividendos**
```sql
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
```

#### **5. Performance por Setor**
```sql
SELECT 
    a.setor,
    COUNT(DISTINCT a.id) as total_ativos,
    AVG(c.preco_fechamento) as preco_medio,
    SUM(c.volume_financeiro) as volume_total,
    AVG(c.volume_financeiro) as volume_medio
FROM cotacoes c
JOIN ativos a ON c.id_ativo = a.id
WHERE c.data = (SELECT MAX(data) FROM cotacoes)
    AND a.setor IS NOT NULL
GROUP BY a.setor
ORDER BY volume_total DESC;
```

### **📈 Consultas Avançadas para Análise**

#### **6. Top FIIs por Rendimento**
```sql
SELECT 
    a.codigo,
    a.nome,
    COUNT(d.id) as total_pagamentos,
    SUM(d.valor) as total_dividendos,
    AVG(d.valor) as media_dividendo,
    MAX(d.data) as ultimo_pagamento
FROM ativos a
JOIN dividendos d ON a.id = d.id_ativo
WHERE a.tipo = 'FII'
GROUP BY a.codigo, a.nome
HAVING COUNT(d.id) > 0
ORDER BY total_dividendos DESC
LIMIT 15;
```

#### **7. Evolução de Preços (Últimos 30 dias)**
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
    ) as variacao_percent
FROM cotacoes c
JOIN ativos a ON c.id_ativo = a.id
WHERE c.data >= CURRENT_DATE - INTERVAL '30 days'
    AND a.codigo IN ('PETR4', 'VALE3', 'ITUB4', 'BBDC4')
ORDER BY a.codigo, c.data DESC;
```

## 📊 **CONSULTAS OTIMIZADAS PARA POWER BI**

### **1. Cotações com Informações do Ativo**
```sql
SELECT 
    a.codigo,
    a.nome,
    a.tipo,
    a.setor,
    c.data,
    c.preco_fechamento,
    c.volume_financeiro
FROM cotacoes c
JOIN ativos a ON c.id_ativo = a.id
ORDER BY c.data DESC, c.volume_financeiro DESC
```

### **2. Performance por Setor**
```sql
SELECT 
    a.setor,
    COUNT(*) as total_ativos,
    AVG(c.preco_fechamento) as preco_medio,
    SUM(c.volume_financeiro) as volume_total
FROM cotacoes c
JOIN ativos a ON c.id_ativo = a.id
WHERE c.data = (SELECT MAX(data) FROM cotacoes)
GROUP BY a.setor
ORDER BY volume_total DESC
```

### **3. Top 10 Ativos por Volume**
```sql
SELECT TOP 10
    a.codigo,
    a.nome,
    c.preco_fechamento,
    c.volume_financeiro
FROM cotacoes c
JOIN ativos a ON c.id_ativo = a.id
WHERE c.data = (SELECT MAX(data) FROM cotacoes)
ORDER BY c.volume_financeiro DESC
```

### **4. Histórico de Dividendos**
```sql
SELECT 
    a.codigo,
    a.nome,
    d.data,
    d.valor,
    d.tipo,
    c.preco_fechamento,
    (d.valor / c.preco_fechamento * 100) as yield_percentual
FROM dividendos d
JOIN ativos a ON d.id_ativo = a.id
LEFT JOIN cotacoes c ON c.id_ativo = a.id AND c.data = d.data
ORDER BY d.data DESC
```

---

## 🎨 **DASHBOARDS SUGERIDOS**

### **Dashboard 1: Visão Geral do Mercado**

#### **Visuais:**
1. **Cartão**: Total de ativos
2. **Cartão**: Volume total negociado
3. **Gráfico de Pizza**: Distribuição por tipo (Ações, FIIs, ETFs)
4. **Gráfico de Barras**: Top 10 setores por volume
5. **Tabela**: Maiores altas/baixas do dia

#### **Filtros:**
- Data
- Tipo de ativo
- Setor

### **Dashboard 2: Análise Setorial**

#### **Visuais:**
1. **Treemap**: Ativos por setor e volume
2. **Gráfico de Linhas**: Evolução por setor
3. **Scatter Plot**: Preço vs Volume por setor
4. **Tabela**: Estatísticas por setor

#### **Métricas calculadas:**
```dax
Volume Médio = AVERAGE(cotacoes[volume_financeiro])
Variação % = DIVIDE([Preço Atual] - [Preço Anterior], [Preço Anterior], 0)
```

### **Dashboard 3: Análise de Dividendos**

#### **Visuais:**
1. **Gráfico de Barras**: Dividendos por mês
2. **Gráfico de Linhas**: Yield ao longo do tempo
3. **Tabela**: Ranking de yield
4. **Cartão**: Total de dividendos distribuídos

#### **Métricas calculadas:**
```dax
Yield Médio = AVERAGE(dividendos[valor]) / AVERAGE(cotacoes[preco_fechamento])
Total Dividendos = SUM(dividendos[valor])
```

---

## 🔄 **ATUALIZAÇÃO AUTOMÁTICA**

### **Configurar Refresh:**
1. **Arquivo** → **Opções e configurações** → **Configurações**
2. **Atualização de dados** → **Atualização agendada**
3. Definir frequência (diária recomendada)

### **Script de automação:**
```batch
@echo off
echo Atualizando dados B3...
cd "C:\Caminho\Para\Projeto_Facul"
python main.py
echo 5 | python main.py
echo Dados atualizados!
```

---

## 📈 **MEDIDAS DAX ÚTEIS**

### **Preço Atual:**
```dax
Preço Atual = 
CALCULATE(
    MAX(cotacoes[preco_fechamento]),
    FILTER(cotacoes, cotacoes[data] = MAX(cotacoes[data]))
)
```

### **Variação Percentual:**
```dax
Variação % = 
VAR PrecoAnterior = 
    CALCULATE(
        MAX(cotacoes[preco_fechamento]),
        DATEADD(cotacoes[data], -1, DAY)
    )
VAR PrecoAtual = [Preço Atual]
RETURN
    DIVIDE(PrecoAtual - PrecoAnterior, PrecoAnterior, 0)
```

### **Volume Médio (30 dias):**
```dax
Volume Médio 30d = 
CALCULATE(
    AVERAGE(cotacoes[volume_financeiro]),
    DATESINPERIOD(cotacoes[data], MAX(cotacoes[data]), -30, DAY)
)
```

### **Yield Acumulado:**
```dax
Yield Acumulado = 
SUMX(
    dividendos,
    DIVIDE(dividendos[valor], RELATED(cotacoes[preco_fechamento]), 0)
)
```

---

## 🎯 **EXEMPLOS DE RELATÓRIOS**

### **Relatório 1: Daily Market Summary**
- Principais altas e baixas
- Volume por setor
- Indicadores de mercado
- Atualização: Diária

### **Relatório 2: Dividend Analysis**
- Ranking de yield
- Histórico de pagamentos
- Projeções de recebimento
- Atualização: Semanal

### **Relatório 3: Portfolio Performance**
- Performance individual
- Alocação atual
- Rebalanceamento sugerido
- Atualização: Diária

---

## 🔧 **CONFIGURAÇÕES AVANÇADAS**

### **Performance Query:**
```sql
-- Otimizar para grandes volumes
CREATE INDEX idx_cotacoes_data_volume 
ON cotacoes(data, volume_financeiro DESC);

CREATE INDEX idx_ativos_tipo_setor 
ON ativos(tipo, setor);
```

### **Parâmetros Power BI:**
```
Servidor = localhost:5432
Timeout = 300
CommandTimeout = 600
```

### **Configuração de Memória:**
- Aumentar memória disponível no Power BI
- Usar agregações quando possível
- Implementar incremental refresh

---

## 📱 **PUBLICAÇÃO E COMPARTILHAMENTO**

### **Power BI Service:**
1. **Publicar** relatório no Power BI Service
2. Configurar **Gateway** para dados on-premises
3. Agendar **refresh automático**
4. Compartilhar com equipe

### **Power BI Mobile:**
- Dashboards responsivos
- Alertas em tempo real
- Acesso offline limitado

---

## 🛠️ **TROUBLESHOOTING**

### **Erro de Conexão:**
```
Verificar:
- PostgreSQL rodando (docker ps)
- Firewall liberado na porta 5432
- Credenciais corretas (admin/admin)
```

### **Dados não aparecem:**
```
Verificar:
- Dados coletados (opção 5 do sistema)
- Relacionamentos configurados
- Filtros aplicados
```

### **Performance lenta:**
```
Soluções:
- Usar DirectQuery para dados grandes
- Criar índices no PostgreSQL
- Otimizar consultas DAX
```

---

## 📚 **RECURSOS ADICIONAIS**

### **Consultas Prontas:**
Ver arquivo `consultas_powerbi.sql` com 20+ queries otimizadas.

### **Documentação Oficial:**
- Power BI: https://docs.microsoft.com/power-bi/
- PostgreSQL Connector: https://docs.microsoft.com/power-bi/connect-data/

---

## 🎉 **RESULTADO FINAL**

### **🗄️ Com DBeaver (Recomendado):**
- ✅ **Análise exploratória** completa dos dados B3
- ✅ **Consultas SQL** personalizadas
- ✅ **Visualizações** e gráficos básicos
- ✅ **Export** para Excel/CSV
- ✅ **Totalmente gratuito** e multiplataforma
- ✅ **Controle total** sobre os dados

### **📊 Com Power BI (Alternativo):**
- ✅ **Dashboards profissionais** corporativos
- ✅ **Atualização automática** diária
- ✅ **Análises avançadas** com DAX
- ✅ **Compartilhamento** com equipe
- ✅ **Acesso mobile** aos relatórios

---

## 🚀 **RECOMENDAÇÃO FINAL**

### **Para começar: Use DBeaver**
1. **Mais simples** de configurar
2. **Gratuito** e sem limitações
3. **Ideal** para exploração inicial
4. **Tutorial completo**: [`TUTORIAL_DBEAVER.md`](TUTORIAL_DBEAVER.md)

### **Para dashboards corporativos: Power BI**
1. **Após dominar** os dados no DBeaver
2. **Para apresentações** profissionais
3. **Quando precisar** de compartilhamento

**🎯 Sistema B3 + DBeaver = Análise Completa e Gratuita de Investimentos** 📊

---

**DBeaver + Power BI Integration - Complete Financial Analysis Solution** 💼
