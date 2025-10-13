# FUNCIONALIDADES DETALHADAS - SISTEMA B3

## VISAO GERAL

O Sistema B3 oferece funcionalidades principais para analise completa de dados financeiros da Bolsa de Valores brasileira através de uma interface grafica moderna.

---

## CONSULTAR ATIVOS

### O que faz:
Lista todos os ativos disponíveis no banco de dados com opcoes de filtros avancados através de interface grafica intuitiva.

### Como usar:
1. Execute `python main.py`
2. Clique em "Consultar Ativos"
3. Selecione filtros no pop-up:
   - **Tipo**: Acoes, FIIs, ETFs, BDRs
   - **Setor**: Bancario, Petroleo, Tecnologia, etc.
4. Visualize resultados em tabela navegavel

### Exemplo de uso:
```
Filtrar por tipo: ACAO
Filtrar por setor: PETROLEO
```

### Resultado:
- Tabela interativa com scroll
- Codigo, nome, tipo e setor
- Estatisticas de quantidade por categoria
- Informacoes organizadas e formatadas

### Casos praticos:
- Encontrar todas as acoes de tecnologia
- Listar todos os FIIs disponiveis
- Verificar ativos de um setor especifico

---

## HISTORICO DE COTACOES

### O que faz:
Exibe o historico de precos de um ativo especifico com graficos candlestick profissionais estilo TradingView.

### Como usar:
1. Execute `python main.py`
2. Clique em "Historico de Cotacoes"
3. Digite o codigo do ativo (ex: `PETR4`)
4. Informe o periodo em dias (padrao: 30)
5. Clique em "Buscar Historico" ou "Gerar Grafico"

### Exemplo de uso:
```
Codigo do ativo: PETR4
Periodo em dias: 60
Gerar grafico: Sim
```

### Resultado:
- Tabela com dados historicos OHLC
- Grafico candlestick interativo profissional
- Linhas de suporte e resistencia automaticas
- Cores profissionais (verde/vermelho)
- Arquivo HTML salvo: `historico_PETR4.html`
- Abre automaticamente no navegador

### Informacoes exibidas:
- Preco de abertura/fechamento
- Maxima e minima do dia
- Volume negociado
- Variacao percentual
- Suporte e resistencia calculados

### Casos praticos:
- Analisar performance de uma acao
- Comparar precos em diferentes periodos
- Identificar tendencias de mercado
- Apresentacoes profissionais

---

## RELATORIO DE DIVIDENDOS

### O que faz:
Analisa os dividendos e proventos distribuidos pelos ativos com visualizacoes interativas.

### Como usar:
1. Execute `python main.py`
2. Clique em "Relatorio de Dividendos"
3. Selecione filtros no pop-up:
   - Codigo do ativo (ou todos)
   - Ano especifico
   - Trimestre
4. Escolha se quer gerar grafico

### Exemplo de uso:
```
Codigo do ativo: ITUB4
Ano: 2024
Gerar grafico: Sim
```

### Resultado:
- Tabela com historico de dividendos
- Graficos de distribuicao temporal
- Estatisticas de yield
- Comparativo entre ativos

### Informacoes exibidas:
- Data de pagamento
- Valor do dividendo
- Tipo de provento
- Yield percentual
- Frequencia de pagamento

### Casos praticos:
- Avaliar rentabilidade de FIIs
- Comparar yield de diferentes acoes
- Planejar recebimento de dividendos

---

## DADOS HISTORICOS (30d)

### O que faz:
Gera dados historicos simulados para os ultimos 30 dias baseados nos precos atuais, permitindo graficos mais completos.

### Como usar:
1. Execute `python main.py`
2. Clique em "Dados Historicos (30d)"
3. Confirme a geracao de dados simulados
4. Aguarde processamento (alguns minutos)

### Processo executado:
1. **Coleta atual**: Obtem precos mais recentes
2. **Simulacao**: Gera 30 dias de dados com variacoes realistas
3. **Validacao**: Mantem logica OHLC correta
4. **Armazenamento**: Insere no PostgreSQL
5. **Mapeamento**: Associa IDs dos ativos corretamente

### Resultado:
- 30 dias de cotacoes historicas simuladas
- Dados realistas baseados em precos atuais
- Graficos de candlestick mais completos
- Pula fins de semana automaticamente

### Casos praticos:
- Testar graficos com mais dados
- Analises de tendencia de longo prazo
- Demonstracoes e apresentacoes
- Desenvolvimento e testes

---

## RESUMO DO SISTEMA

### O que faz:
Exibe estatisticas gerais do banco de dados e status do sistema.

### Como usar:
1. Execute `python main.py`
2. Clique em "Resumo do Sistema"

### Resultado:
- Quantidade de ativos cadastrados
- Numero de cotacoes armazenadas
- Periodo de dados disponivel
- Status de conectividade
- Estatisticas por tipo de ativo

---

## EXECUTAR TODOS OS RELATORIOS

### O que faz:
Executa automaticamente todas as funcionalidades de relatorio de uma vez.

### Processo:
1. Consulta geral de ativos
2. Relatorio de dividendos geral
3. Dashboard de alocacao completo
4. Resumo do sistema

### Resultado:
- Todos os graficos HTML gerados
- Relatorios completos no console
- Visao 360° dos dados

---

## COLETAR DADOS B3 (D-1)

### O que faz:
Baixa automaticamente os dados mais recentes da B3 e armazena no banco.

### Como usar:
1. Execute `python main.py`
2. Clique em "Coletar Dados B3 (D-1)"
3. Aguarde o processamento (pode levar alguns minutos)

### Processo executado:
1. **Download**: Baixa arquivo COTAHIST da B3 (~60MB)
2. **Processamento**: Le e filtra dados D-1
3. **Validacao**: Remove registros invalidos
4. **Classificacao**: Identifica tipos e setores
5. **Armazenamento**: Insere no PostgreSQL
6. **Verificacao**: Confirma integridade dos dados

### Resultado:
- ~11.500 cotacoes do dia anterior
- ~11.500 ativos unicos
- Dados prontos para analise
- Log detalhado do processo

### Informacoes processadas:
- Precos de abertura/fechamento
- Maximas e minimas
- Volume financeiro
- Quantidade de negocios
- Codigos e nomes dos ativos
- Classificacao por tipo e setor

### Casos praticos:
- Atualizacao diaria automatica
- Primeira carga de dados
- Sincronizacao com B3
- Preparacao para analises

---

## INTEGRACAO COM POWER BI

### Como conectar:
1. Abrir Power BI Desktop
2. Obter dados → PostgreSQL
3. Servidor: `localhost:5432`
4. Banco: `b3`
5. Usuario: `admin` / Senha: `admin`

### Tabelas disponiveis:
- `ativos` - Cadastro de ativos
- `cotacoes` - Historico de precos
- `dividendos` - Proventos distribuidos

### Consultas prontas:
Ver arquivo `consultas_powerbi.sql` com queries otimizadas.

---

## INTEGRACAO COM DBEAVER

### Como conectar:
1. Abrir DBeaver
2. Nova conexao PostgreSQL
3. Host: `localhost:5432`
4. Database: `b3`
5. Usuario: `admin` / Senha: `admin`

### Recursos disponiveis:
- Consultas SQL personalizadas
- Visualizacao de dados em tabelas
- Export para Excel/CSV
- Graficos basicos integrados

---

## FLUXO DE TRABALHO RECOMENDADO

### 1. Primeira execucao:
```bash
python main.py
# Clicar em "Coletar Dados B3 (D-1)"
# Clicar em "Dados Historicos (30d)" (RECOMENDADO)
# Aguardar conclusao
```

### 2. Analise diaria:
```bash
python main.py
# "Coletar Dados B3": Atualizar dados
# "Executar Todos os Relatorios": Visao completa
```

### 3. Analise especifica:
```bash
python main.py
# "Consultar Ativos": Ver ativos disponiveis
# "Historico de Cotacoes": Analisar ativo especifico
# "Dados Historicos": Para graficos completos
```

---

**Sistema B3 - Funcionalidades Completas para Analise Financeira**