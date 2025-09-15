# 📁 **EXPLICAÇÃO DETALHADA DOS ARQUIVOS - SISTEMA B3**

## 🎯 **ARQUIVOS PRINCIPAIS DO SISTEMA**

---

## 🚀 **main.py** (7.7KB)
**Sistema principal com menu interativo**

### **Função:**
- Ponto de entrada do sistema
- Menu interativo com 8 opções
- Coordena todos os workflows
- Gerencia entrada do usuário

### **Classes principais:**
- `B3System`: Classe principal do sistema
- Métodos para cada opção do menu

### **Como funciona:**
1. Inicializa workflows de dados e relatórios
2. Testa conexão com banco
3. Exibe menu interativo
4. Executa opção escolhida pelo usuário

### **Exemplo de uso:**
```bash
python main.py
```

---

## ⚙️ **config.py** (2.2KB)
**Configurações centralizadas do sistema**

### **Função:**
- Centraliza todas as configurações
- Define conexão com banco
- URLs da B3 e parâmetros
- Funções utilitárias

### **Principais configurações:**
```python
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'b3',
    'username': 'admin',
    'password': 'admin'
}

B3_CONFIG = {
    'cotahist_url': 'https://bvmf.bmfbovespa.com.br/...',
    'user_agent': 'Mozilla/5.0...',
    'timeout': 30
}
```

### **Funções importantes:**
- `calcular_d1()`: Calcula dia útil anterior
- `get_cotahist_url()`: Retorna URL baseada no ano

---

## 🗄️ **database_manager.py** (9.7KB)
**Gerenciador de operações do banco de dados**

### **Função:**
- Todas as operações com PostgreSQL
- CRUD de ativos e cotações
- Queries personalizadas
- Tratamento de duplicatas

### **Classe principal:**
- `DatabaseManager`: Gerencia conexões e operações

### **Métodos importantes:**
- `test_connection()`: Testa conexão
- `insert_new_ativos()`: Insere novos ativos
- `insert_cotacoes()`: Insere cotações (com UPSERT)
- `execute_query()`: Executa queries customizadas
- `check_and_create_tables()`: Cria tabelas automaticamente

### **Características especiais:**
- **UPSERT**: Evita duplicatas automaticamente
- **Inserção em lotes**: Processa 1000 registros por vez
- **Tratamento robusto de erros**

---

## 📊 **data_collector.py** (13KB)
**Coletor de dados da B3**

### **Função:**
- Download de arquivos COTAHIST
- Processamento de dados CSV
- Filtros D-1
- Transformação de dados

### **Classe principal:**
- `B3DataCollector`: Coleta e processa dados

### **Métodos importantes:**
- `download_cotahist()`: Baixa arquivo ZIP da B3
- `parse_csv_data()`: Lê arquivo com posições fixas
- `filter_d1_data()`: Filtra dados do dia anterior
- `transform_data()`: Converte e limpa dados
- `prepare_cotacoes()`: Prepara para inserção

### **Características especiais:**
- **Múltiplos encodings**: Tenta latin1, utf-8, cp1252
- **Posições fixas**: Layout oficial COTAHIST
- **Fallback inteligente**: Usa data mais recente se D-1 não disponível
- **Validação robusta**: Remove registros inválidos

---

## 📈 **reports_manager.py** (9.7KB)
**Gerenciador de relatórios e consultas**

### **Função:**
- Executa consultas no banco
- Gera relatórios formatados
- Estatísticas e análises
- Interface com visualizações

### **Classe principal:**
- `ReportsManager`: Gerencia relatórios

### **Métodos importantes:**
- `consultar_ativos()`: Lista ativos com filtros
- `historico_cotacoes()`: Histórico de preços
- `relatorio_dividendos()`: Análise de proventos
- `dashboard_alocacao()`: Distribuição da carteira
- `resumo_sistema()`: Estatísticas gerais

### **Características especiais:**
- **Filtros avançados**: Por tipo, setor, período
- **Estatísticas automáticas**: Cálculos de performance
- **Formatação elegante**: Saída organizada no console

---

## 📊 **visualization_manager.py** (8.2KB)
**Gerenciador de gráficos e visualizações**

### **Função:**
- Cria gráficos interativos
- Exporta para HTML
- Dashboards visuais
- Integração com Plotly

### **Classe principal:**
- `VisualizationManager`: Gerencia visualizações

### **Métodos importantes:**
- `create_candlestick_chart()`: Gráfico de velas
- `create_pie_chart()`: Gráfico de pizza
- `create_bar_chart()`: Gráfico de barras
- `create_allocation_dashboard()`: Dashboard completo

### **Tipos de gráficos:**
- **Candlestick**: Preços OHLC
- **Pizza**: Distribuição percentual
- **Barras**: Comparativos
- **Linhas**: Evolução temporal

### **Características especiais:**
- **Interativos**: Zoom, hover, filtros
- **Responsivos**: Adaptam ao tamanho da tela
- **Exportação**: Salva em HTML

---

## 🔄 **data_ingestion_workflow.py** (5.0KB)
**Workflow de ingestão de dados**

### **Função:**
- Orquestra processo completo de coleta
- Coordena módulos
- Tratamento de erros
- Logs detalhados

### **Classe principal:**
- `DataIngestionWorkflow`: Workflow completo

### **Fluxo de execução:**
1. Verifica conexão com banco
2. Coleta dados da B3
3. Processa novos ativos
4. Insere cotações
5. Valida resultados

### **Características especiais:**
- **Transacional**: Rollback em caso de erro
- **Logs detalhados**: Rastreamento completo
- **Validações**: Verifica integridade

---

## 📋 **reports_workflow.py** (4.8KB)
**Workflow de relatórios**

### **Função:**
- Orquestra geração de relatórios
- Coordena visualizações
- Execução em batch
- Controle de fluxo

### **Classe principal:**
- `ReportsWorkflow`: Workflow de relatórios

### **Métodos importantes:**
- `execute_consulta_ativos()`: Executa consulta
- `execute_historico_cotacoes()`: Gera histórico
- `execute_dashboard_alocacao()`: Cria dashboard
- `execute_all_reports()`: Executa todos

---

## 🛠️ **ARQUIVOS DE INFRAESTRUTURA**

### **docker-compose.yml** (415B)
**Configuração do PostgreSQL containerizado**

```yaml
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: b3
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin
    ports:
      - "5432:5432"
```

### **schema.sql** (1KB)
**Estrutura do banco de dados**

Define tabelas:
- `ativos`: Cadastro de ativos
- `cotacoes`: Histórico de preços
- `dividendos`: Proventos
- `carteira`: Posições
- `indices`: Índices de mercado

### **requirements.txt** (403B)
**Dependências Python**

Principais bibliotecas:
- pandas>=1.5.0
- sqlalchemy>=1.4.0
- psycopg2-binary>=2.9.0
- plotly>=5.0.0
- requests>=2.28.0

---

## 🤖 **ARQUIVOS DE AUTOMAÇÃO**

### **setup.py** (4.4KB)
**Configuração automática do sistema**

Funções:
- Verifica Python e Docker
- Instala dependências
- Inicia banco de dados
- Testa conexões
- Configura tabelas

### **diagnostico.py** (6.2KB)
**Verificação de problemas**

Testa:
- Módulos Python
- Conexão Docker
- Banco de dados
- Conexão com B3
- Integridade dos arquivos

### **iniciar.bat / iniciar.sh**
**Scripts de inicialização**

- **Windows**: `iniciar.bat`
- **Linux/Mac**: `iniciar.sh`

Executam automaticamente:
1. Setup do sistema
2. Inicialização do main.py

---

## 📚 **ARQUIVOS DE DADOS**

### **consultas_powerbi.sql** (6.1KB)
**Consultas otimizadas para Power BI**

Queries prontas para:
- Análise de performance
- Distribuição setorial
- Histórico de dividendos
- Comparativos de mercado

### **dados_exemplo.sql** (3.9KB)
**Dados de teste e exemplo**

Inserts de exemplo para:
- Ativos fictícios
- Cotações de teste
- Dividendos simulados
- Dados de carteira

---

## 📖 **ARQUIVOS DE DOCUMENTAÇÃO**

### **README.md** (7.7KB)
**Documentação principal**

Contém:
- Visão geral do projeto
- Instruções de instalação
- Como usar o sistema
- Solução de problemas

### **AVALIACAO_PROJETO.md** (4.9KB)
**Critérios de avaliação acadêmica**

Para apresentação:
- Objetivos do projeto
- Funcionalidades implementadas
- Tecnologias utilizadas
- Resultados obtidos

### **POWER_BI_SETUP.md** (4.9KB)
**Guia de integração Power BI**

Instruções para:
- Conectar Power BI ao PostgreSQL
- Importar tabelas
- Criar relatórios
- Configurar dashboards

### **GUIA_RAPIDO.md** (3.8KB)
**Instruções simplificadas**

Guia resumido:
- Instalação rápida
- Primeiros passos
- Funcionalidades principais
- Solução de problemas comuns

---

## 🎯 **FLUXO DE EXECUÇÃO**

### **Inicialização:**
```
iniciar.bat → setup.py → main.py
```

### **Coleta de dados:**
```
main.py → data_ingestion_workflow.py → data_collector.py → database_manager.py
```

### **Relatórios:**
```
main.py → reports_workflow.py → reports_manager.py → visualization_manager.py
```

---

**Sistema B3 - Arquitetura Modular e Documentada** 🏗️
