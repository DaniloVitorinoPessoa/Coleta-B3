# GUIA RÁPIDO - Sistema B3 com Interface Gráfica

## Início Imediato

### **Executar Sistema**
```bash
python main.py
```
*Interface gráfica moderna será aberta automaticamente*

### **Primeira Vez (OBRIGATÓRIO)**
1. Clique em **"Coletar Dados B3"**
2. Aguarde a coleta (pode demorar alguns minutos)
3. Dados prontos para análise!

## Interface Gráfica

### **Recursos Modernos**
- **Pop-ups interativos** para entrada de dados
- **Janelas de resultados** com abas organizadas
- **Filtros dinâmicos** de setor baseados no tipo
- **Tabelas navegáveis** para visualização de dados
- **Logs em tempo real** das operações

### **Funcionalidades Disponíveis**
1. **Consultar Ativos** - Lista filtrada por tipo e setor
2. **Histórico de Cotações** - Gráficos candlestick interativos  
3. **Relatório de Dividendos** - Análise de proventos
4. **Dashboard de Alocação** - Visualização de carteira
5. **Coletar Dados B3** - Importação automática (EXECUTE PRIMEIRO!)

## Como Usar

### **Coletar Dados (Primeira vez)**
```
Clique: "Coletar Dados B3"
→ Aguarde: ~14.000 ativos sendo processados
→ Status: Logs aparecem em tempo real
→ Resultado: "Coleta concluída com sucesso!"
```

### **Consultar Ativos**
```
Clique: "Consultar Ativos" 
→ Pop-up: Selecione tipo (AÇÃO, FII, ETF) ou deixe vazio
→ Setor: Carrega automaticamente com base no tipo
→ Resultado: Janela com lista filtrada + estatísticas
```

### **Análise de Cotações**
```
Clique: "Histórico de Cotações"
→ Digite: Código do ativo (ex: PETR4, VALE3)
→ Período: Número de dias (padrão: 30)
→ Resultado: Gráfico candlestick interativo
```

### **Relatório de Dividendos**
```
Clique: "Relatório de Dividendos"
→ Ativo: Digite código ou deixe vazio (todos)
→ Ano: Digite ano ou deixe vazio (todos)
→ Resultado: Lista de proventos + estatísticas
```

## Classificação Inteligente

### **Tipos de Ativos**
- **AÇÃO**: ~13.000 ações (ON, PN, Units)
- **FII**: Fundos de Investimento Imobiliário
- **ETF**: Exchange Traded Funds
- **BDR**: Brazilian Depositary Receipts

### **Setores Identificados**
- **Mineração e Siderurgia** (Vale, CSN, Usiminas)
- **Bancos** (Itaú, Bradesco, Santander)
- **Energia Elétrica** (Eletrobras, Cemig, Copel)
- **Petróleo e Gás** (Petrobras, Ultrapar)
- **Telecomunicações** (Tim, Telefônica)
- **Outros** - Demais setores não classificados

## Banco de Dados

### **Conexão Automática**
- **Host**: localhost:5432
- **Database**: b3
- **User/Pass**: admin/admin
- **Tabelas**: Criadas automaticamente

### **Dados Coletados**
- **~14.000 ativos** com tipo e setor
- **Cotações diárias** (abertura, fechamento, volume)
- **Dividendos históricos** (valor, data, tipo)
- **Sincronização inteligente** (só atualiza diferenças)

## Solução Rápida de Problemas

### **"Nenhum ativo encontrado"**
```
Solução: Clique em "Coletar Dados B3" primeiro
```

### **"Erro de conexão com banco"**
```bash
# Verificar PostgreSQL
docker ps

# Se não aparecer, iniciar:
docker-compose up -d
```

### **"Interface não responde"**
```
Normal: Operações longas rodam em background
Aguarde: Logs mostram o progresso
Não feche: Deixe a operação terminar
```

### **"Módulo não encontrado"**
```bash
pip install -r requirements.txt
```

## Dicas de Uso

### **Filtros Inteligentes**
1. Selecione **tipo** primeiro (AÇÃO, FII, etc.)
2. **Setores** carregam automaticamente
3. Deixe vazio para ver **todos** os resultados

### **Códigos de Ativos**
- **Ações**: PETR4, VALE3, ITUB4, BBDC4
- **FIIs**: HGLG11, XPML11, BCFF11
- **ETFs**: BOVA11, SMAL11, IVVB11

### **Períodos Recomendados**
- **Curto prazo**: 7-30 dias
- **Médio prazo**: 90-180 dias  
- **Longo prazo**: 365-730 dias

## Visualizações Geradas

Os gráficos são salvos automaticamente:
- **`historico_[CODIGO].html`** - Gráficos candlestick
- **`alocacao_setor.html`** - Dashboard por setor
- **`alocacao_tipo.html`** - Dashboard por tipo
- **`rentabilidade_ativos.html`** - Performance

## Integração Externa

### **DBeaver (Recomendado)**
- Download: https://dbeaver.io/
- Conecte: localhost:5432, db=b3, user=admin, pass=admin
- Explore dados com SQL visual

### **Power BI**
- Fonte: PostgreSQL
- Servidor: localhost:5432
- Use queries prontas em `consultas_powerbi.sql`

## Fluxo Completo

```
1. python main.py
2. "Coletar Dados B3" (primeira vez)
3. "Consultar Ativos" (explorar dados)
4. "Histórico" (analisar ativo específico)  
5. "Dividendos" (ver proventos)
6. "Dashboard" (visão geral carteira)
```

---
**Sistema B3 pronto! Interface moderna para análise profissional de dados financeiros**