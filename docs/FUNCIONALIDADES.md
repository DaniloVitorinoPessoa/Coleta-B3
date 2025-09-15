# 🎯 **FUNCIONALIDADES DETALHADAS - SISTEMA B3**

## 📋 **VISÃO GERAL**

O Sistema B3 oferece 5 funcionalidades principais para análise completa de dados financeiros da Bolsa de Valores brasileira.

---

## 🔍 **OPÇÃO 1: CONSULTAR ATIVOS**

### **O que faz:**
Lista todos os ativos disponíveis no banco de dados com opções de filtros avançados.

### **Como usar:**
1. Execute `python main.py`
2. Escolha opção `1`
3. Digite filtros (ou Enter para todos):
   - **Tipo**: Ações, FIIs, ETFs
   - **Setor**: Bancário, Petróleo, Tecnologia, etc.

### **Exemplo de uso:**
```
Filtrar por tipo: ACAO
Filtrar por setor: PETROLEO
```

### **Resultado:**
- Tabela com código, nome, tipo e setor
- Estatísticas de quantidade por categoria
- Informações organizadas e formatadas

### **Casos práticos:**
- Encontrar todas as ações de tecnologia
- Listar todos os FIIs disponíveis
- Verificar ativos de um setor específico

---

## 📈 **OPÇÃO 2: HISTÓRICO DE COTAÇÕES**

### **O que faz:**
Exibe o histórico de preços de um ativo específico com gráficos interativos.

### **Como usar:**
1. Execute `python main.py`
2. Escolha opção `2`
3. Digite o código do ativo (ex: `PETR4`)
4. Informe o período em dias (padrão: 30)
5. Escolha se quer gerar gráfico

### **Exemplo de uso:**
```
Código do ativo: PETR4
Período em dias: 60
Gerar gráfico? s
```

### **Resultado:**
- Tabela com dados históricos
- Gráfico candlestick interativo (Plotly)
- Estatísticas de performance
- Arquivo HTML salvo: `historico_PETR4.html`

### **Informações exibidas:**
- Preço de abertura/fechamento
- Máxima e mínima do dia
- Volume negociado
- Número de negócios
- Variação percentual

### **Casos práticos:**
- Analisar performance de uma ação
- Comparar preços em diferentes períodos
- Identificar tendências de mercado

---

## 💰 **OPÇÃO 3: RELATÓRIO DE DIVIDENDOS**

### **O que faz:**
Analisa os dividendos e proventos distribuídos pelos ativos.

### **Como usar:**
1. Execute `python main.py`
2. Escolha opção `3`
3. Digite código do ativo (ou Enter para todos)
4. Digite ano (ou Enter para todos)
5. Escolha se quer gerar gráfico

### **Exemplo de uso:**
```
Código do ativo: ITUB4
Ano: 2024
Gerar gráfico? s
```

### **Resultado:**
- Tabela com histórico de dividendos
- Gráficos de distribuição temporal
- Estatísticas de yield
- Comparativo entre ativos

### **Informações exibidas:**
- Data de pagamento
- Valor do dividendo
- Tipo de provento
- Yield percentual
- Frequência de pagamento

### **Casos práticos:**
- Avaliar rentabilidade de FIIs
- Comparar yield de diferentes ações
- Planejar recebimento de dividendos

---

## 🎨 **OPÇÃO 4: DASHBOARD DE ALOCAÇÃO**

### **O que faz:**
Cria visualizações da distribuição da carteira por setor e tipo de ativo.

### **Como usar:**
1. Execute `python main.py`
2. Escolha opção `4`
3. Escolha se quer gerar gráficos (recomendado: S)

### **Resultado:**
- Gráfico de pizza por setor
- Gráfico de barras por tipo
- Análise de concentração
- Arquivos HTML salvos:
  - `alocacao_setor.html`
  - `alocacao_tipo.html`
  - `rentabilidade_ativos.html`

### **Visualizações geradas:**
1. **Por Setor**: Distribuição percentual
2. **Por Tipo**: Ações vs FIIs vs ETFs
3. **Rentabilidade**: Performance por ativo
4. **Concentração**: Top 10 ativos

### **Casos práticos:**
- Avaliar diversificação da carteira
- Identificar concentração de risco
- Visualizar distribuição setorial
- Apresentar dados para investidores

---

## 📥 **OPÇÃO 5: COLETAR DADOS B3 (D-1)**

### **O que faz:**
Baixa automaticamente os dados mais recentes da B3 e armazena no banco.

### **Como usar:**
1. Execute `python main.py`
2. Escolha opção `5`
3. Aguarde o processamento (pode levar alguns minutos)

### **Processo executado:**
1. **Download**: Baixa arquivo COTAHIST da B3 (~60MB)
2. **Processamento**: Lê e filtra dados D-1
3. **Validação**: Remove registros inválidos
4. **Armazenamento**: Insere no PostgreSQL
5. **Verificação**: Confirma integridade dos dados

### **Resultado:**
- ~11.500 cotações do dia anterior
- ~11.500 ativos únicos
- Dados prontos para análise
- Log detalhado do processo

### **Informações processadas:**
- Preços de abertura/fechamento
- Máximas e mínimas
- Volume financeiro
- Quantidade de negócios
- Códigos e nomes dos ativos

### **Casos práticos:**
- Atualização diária automática
- Primeira carga de dados
- Sincronização com B3
- Preparação para análises

---

## 📊 **OPÇÃO 6: RESUMO DO SISTEMA**

### **O que faz:**
Exibe estatísticas gerais do banco de dados e status do sistema.

### **Resultado:**
- Quantidade de ativos cadastrados
- Número de cotações armazenadas
- Período de dados disponível
- Status de conectividade
- Estatísticas por tipo de ativo

---

## 🔄 **OPÇÃO 7: EXECUTAR TODOS OS RELATÓRIOS**

### **O que faz:**
Executa automaticamente todas as funcionalidades de relatório.

### **Processo:**
1. Consulta geral de ativos
2. Relatório de dividendos geral
3. Dashboard de alocação completo
4. Resumo do sistema

### **Resultado:**
- Todos os gráficos HTML gerados
- Relatórios completos no console
- Visão 360° dos dados

---

## 🎯 **INTEGRAÇÃO COM POWER BI**

### **Como conectar:**
1. Abrir Power BI Desktop
2. Obter dados → PostgreSQL
3. Servidor: `localhost:5432`
4. Banco: `b3`
5. Usuário: `admin` / Senha: `admin`

### **Tabelas disponíveis:**
- `ativos` - Cadastro de ativos
- `cotacoes` - Histórico de preços
- `dividendos` - Proventos distribuídos
- `carteira` - Posições da carteira
- `indices` - Índices de mercado

### **Consultas prontas:**
Ver arquivo `consultas_powerbi.sql` com queries otimizadas.

---

## 🎓 **FLUXO DE TRABALHO RECOMENDADO**

### **1. Primeira execução:**
```bash
python main.py
# Escolher opção 5 (Coletar Dados)
# Aguardar conclusão
```

### **2. Análise diária:**
```bash
python main.py
# Opção 5: Atualizar dados
# Opção 7: Gerar todos os relatórios
```

### **3. Análise específica:**
```bash
python main.py
# Opção 1: Ver ativos disponíveis
# Opção 2: Analisar ativo específico
# Opção 4: Dashboard de alocação
```

---

**Sistema B3 - Funcionalidades Completas para Análise Financeira** 📈
