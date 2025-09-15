# 📖 **GUIA COMPLETO DE USO - SISTEMA B3**

## 🎯 **PRIMEIROS PASSOS**

### **1. Iniciar o Sistema**
```bash
python main.py
```

### **2. Menu Principal**
```
SISTEMA DE ANALISE B3
========================================
1. Consultar Ativos
2. Histórico de Cotações
3. Relatório de Dividendos
4. Dashboard de Alocação
5. Coletar Dados B3 (D-1)
6. Resumo do Sistema
7. Executar Todos os Relatórios
0. Sair

Escolha uma opção:
```

### **3. Primeira Execução (OBRIGATÓRIO)**
⚠️ **Antes de usar qualquer funcionalidade, execute:**
```
Escolha uma opção: 5
```
Isso baixará os dados da B3 (~2-5 minutos).

---

## 🔍 **OPÇÃO 1: CONSULTAR ATIVOS**

### **Como usar:**
1. Digite `1` no menu principal
2. Escolha filtros (ou pressione Enter para todos)

### **Exemplo prático:**
```
=== CONSULTA DE ATIVOS ===
Filtrar por tipo (ou Enter para todos): ACAO
Filtrar por setor (ou Enter para todos): PETROLEO

Resultado:
Código    Nome                           Tipo    Setor
PETR3     PETROLEO BRASILEIRO SA         ACAO    PETROLEO  
PETR4     PETROLEO BRASILEIRO SA         ACAO    PETROLEO
PRIO3     PETRO RIO SA                   ACAO    PETROLEO
```

### **Filtros disponíveis:**
- **Tipo**: ACAO, FII, ETF, UNIT
- **Setor**: PETROLEO, BANCO, MINERACAO, TECNOLOGIA, etc.

### **Dicas:**
- Deixe em branco para ver todos
- Use maiúsculas para melhor busca
- Combine filtros para busca específica

---

## 📈 **OPÇÃO 2: HISTÓRICO DE COTAÇÕES**

### **Como usar:**
1. Digite `2` no menu principal
2. Digite código do ativo (ex: PETR4)
3. Digite período em dias (padrão: 30)
4. Escolha se quer gerar gráfico

### **Exemplo prático:**
```
=== HISTÓRICO DE COTAÇÕES ===
Código do ativo: PETR4
Período em dias (padrão 30): 60
Gerar gráfico? (s/N): s

Resultado:
- Tabela com histórico de preços
- Gráfico candlestick interativo
- Arquivo salvo: historico_PETR4.html
```

### **Informações exibidas:**
- Data da cotação
- Preços: abertura, fechamento, máximo, mínimo
- Volume financeiro negociado
- Quantidade de negócios
- Variação percentual

### **Códigos populares:**
- **Ações**: PETR4, VALE3, ITUB4, BBDC4, ABEV3
- **FIIs**: HGLG11, XPML11, BTLG11, VISC11
- **ETFs**: BOVA11, IVVB11, SMAL11

---

## 💰 **OPÇÃO 3: RELATÓRIO DE DIVIDENDOS**

### **Como usar:**
1. Digite `3` no menu principal
2. Digite código do ativo (ou Enter para todos)
3. Digite ano (ou Enter para todos)
4. Escolha se quer gerar gráfico

### **Exemplo prático:**
```
=== RELATÓRIO DE DIVIDENDOS ===
Código do ativo (ou Enter para todos): ITUB4
Ano (ou Enter para todos): 2024
Gerar gráfico? (s/N): s

Resultado:
- Histórico de dividendos do ITUB4 em 2024
- Gráfico de distribuição temporal
- Estatísticas de yield
```

### **Informações exibidas:**
- Data de pagamento
- Valor do dividendo/provento
- Tipo: Dividendo, JCP, Bonificação
- Yield sobre preço atual
- Frequência de pagamento

### **Casos de uso:**
- Analisar rentabilidade de FIIs
- Comparar yield de ações
- Planejar recebimento de dividendos
- Avaliar consistência de pagamentos

---

## 🎨 **OPÇÃO 4: DASHBOARD DE ALOCAÇÃO**

### **Como usar:**
1. Digite `4` no menu principal
2. Escolha se quer gerar gráficos (recomendado: S)

### **Exemplo prático:**
```
=== DASHBOARD DE ALOCAÇÃO ===
Gerar gráficos? (S/n): S

Resultado:
- Gráfico de pizza por setor
- Gráfico de barras por tipo
- Análise de concentração
- Arquivos HTML salvos
```

### **Gráficos gerados:**
1. **alocacao_setor.html**: Distribuição por setor
2. **alocacao_tipo.html**: Ações vs FIIs vs ETFs  
3. **rentabilidade_ativos.html**: Performance por ativo

### **Análises fornecidas:**
- Percentual por setor econômico
- Distribuição por tipo de ativo
- Top 10 ativos por volume
- Concentração de risco
- Diversificação da carteira

---

## 📥 **OPÇÃO 5: COLETAR DADOS B3 (D-1)**

### **Como usar:**
1. Digite `5` no menu principal
2. Aguarde o processamento (2-5 minutos)

### **Processo executado:**
```
=== COLETA DE DADOS B3 ===
Iniciando coleta de dados D-1...

1. Download do arquivo COTAHIST (~60MB)
2. Processamento de ~2 milhões de registros
3. Filtro para dia útil anterior
4. Inserção de ~11.500 cotações
5. Cadastro de ~11.500 ativos únicos
```

### **Quando executar:**
- **Primeira vez**: Obrigatório antes de usar o sistema
- **Diariamente**: Para dados atualizados
- **Após feriados**: Para sincronizar com B3

### **Logs importantes:**
```
INFO: Download concluído. Tamanho: 61894684 bytes
INFO: CSV lido com encoding latin1. Linhas: 2092497
INFO: Após filtro D-1: 11539 registros para 2025-09-09
INFO: Inseridas 11539 cotações para 2025-09-09
SUCESSO: Coleta de dados concluída!
```

---

## 📊 **OPÇÃO 6: RESUMO DO SISTEMA**

### **Como usar:**
1. Digite `6` no menu principal
2. Visualize estatísticas gerais

### **Informações exibidas:**
```
=== RESUMO DO SISTEMA ===

Estatísticas do Banco de Dados:
- Ativos cadastrados: 11,481
- Cotações armazenadas: 11,539  
- Período de dados: 2025-09-09
- Última atualização: hoje

Distribuição por tipo:
- Ações: 8,234 (71.7%)
- FIIs: 2,891 (25.2%)
- ETFs: 356 (3.1%)

Status do sistema: ✅ Funcionando
```

---

## 🔄 **OPÇÃO 7: EXECUTAR TODOS OS RELATÓRIOS**

### **Como usar:**
1. Digite `7` no menu principal
2. Aguarde execução automática

### **Relatórios executados:**
1. Consulta geral de ativos
2. Relatório de dividendos (todos os ativos)
3. Dashboard de alocação completo
4. Resumo do sistema

### **Resultado:**
- Todos os gráficos HTML gerados
- Relatórios completos no console
- Visão 360° dos dados

---

## 🎯 **FLUXOS DE TRABALHO RECOMENDADOS**

### **🌅 Rotina Matinal (Trader/Analista)**
```bash
python main.py

# 1. Atualizar dados
Opção 5: Coletar Dados B3 (D-1)

# 2. Visão geral  
Opção 6: Resumo do Sistema

# 3. Análise específica
Opção 2: Histórico de Cotações
Digite: IBOV11 (ou ativo de interesse)
```

### **📊 Análise Semanal (Gestor)**
```bash
python main.py

# 1. Dashboard completo
Opção 4: Dashboard de Alocação

# 2. Relatório de dividendos
Opção 3: Relatório de Dividendos
(Enter para todos os ativos)

# 3. Todos os relatórios
Opção 7: Executar Todos os Relatórios
```

### **🔍 Pesquisa de Ativos (Investidor)**
```bash
python main.py

# 1. Buscar por setor
Opção 1: Consultar Ativos
Tipo: ACAO
Setor: TECNOLOGIA

# 2. Analisar ativo específico
Opção 2: Histórico de Cotações
Código: (escolher da lista anterior)

# 3. Verificar dividendos
Opção 3: Relatório de Dividendos
Código: (mesmo ativo)
```

---

## 📁 **ARQUIVOS GERADOS**

### **Gráficos HTML:**
- `historico_[CODIGO].html` - Gráfico de cotações
- `alocacao_setor.html` - Dashboard por setor
- `alocacao_tipo.html` - Dashboard por tipo
- `rentabilidade_ativos.html` - Performance

### **Como visualizar:**
1. Abrir arquivo HTML no navegador
2. Gráficos são interativos (zoom, hover, filtros)
3. Podem ser compartilhados ou incorporados

### **Localização:**
Todos os arquivos são salvos na pasta raiz do projeto.

---

## 🎨 **PERSONALIZAÇÕES**

### **Alterar período padrão:**
Editar `reports_manager.py`:
```python
# Linha ~45
periodo = int(periodo_input) if periodo_input else 60  # Era 30
```

### **Alterar cores dos gráficos:**
Editar `visualization_manager.py`:
```python
# Personalizar paleta de cores
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', ...]
```

### **Adicionar novos filtros:**
Editar `reports_manager.py` para incluir novos campos de filtro.

---

## ⚠️ **DICAS IMPORTANTES**

### **Performance:**
- Primeira coleta demora mais (dados completos)
- Coletas subsequentes são mais rápidas
- Use períodos menores para análises rápidas

### **Dados:**
- Dados são do dia útil anterior (D-1)
- Finais de semana não têm dados novos
- Feriados podem afetar disponibilidade

### **Gráficos:**
- Sempre gere gráficos para melhor visualização
- Gráficos são salvos automaticamente
- Funcionam offline após geração

### **Códigos de Ativos:**
- Use sempre maiúsculas (PETR4, não petr4)
- Códigos com 4 caracteres são ações ON
- Códigos com 3 caracteres são ações PN
- FIIs terminam em 11 (HGLG11)

---

## 🔧 **SOLUÇÃO DE PROBLEMAS NO USO**

### **"Nenhum ativo encontrado"**
- Execute primeiro a opção 5 (coleta)
- Verifique se digitou o código correto
- Use maiúsculas

### **"Erro ao gerar gráfico"**
- Verifique se plotly está instalado
- Feche outros gráficos abertos
- Reinicie o sistema

### **"Dados não encontrados para D-1"**
- Normal em feriados/finais de semana
- Sistema usa automaticamente data mais recente
- Execute nova coleta no próximo dia útil

---

## 🎉 **APROVEITAMENTO MÁXIMO**

### **Para Estudantes:**
- Use opção 7 para relatórios completos
- Analise diferentes setores (opção 1)
- Compare performance de ativos (opção 2)

### **Para Profissionais:**
- Integre com Power BI para dashboards corporativos
- Use dados para análises quantitativas
- Automatize coleta diária

### **Para Investidores:**
- Monitore carteira com opção 4
- Acompanhe dividendos com opção 3
- Analise tendências com opção 2

---

**Sistema B3 - Guia Completo para Análise Financeira Profissional** 📊
