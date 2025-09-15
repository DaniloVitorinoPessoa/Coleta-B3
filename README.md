# 📊 Sistema de Análise B3 - Interface Gráfica

Sistema completo para análise de dados da B3 (Bolsa de Valores brasileira) com **interface gráfica moderna** e coleta automática de dados.

## 🚀 Início Rápido

### Execução (Interface Gráfica - Padrão)
```bash
python main.py
```

### Execução (Terminal - Opcional)
```bash
python main.py --terminal
```

## ✨ Principais Funcionalidades

### 🎯 **Interface Gráfica Moderna**
- **Pop-ups interativos** para entrada de dados
- **Janelas de resultados** com abas organizadas
- **Filtros dinâmicos** de setor baseados no tipo de ativo
- **Visualização em tabelas** para dados estruturados
- **Logs em tempo real** das operações

### 📈 **Análises Disponíveis**
1. **Consulta de Ativos** - Lista filtrada por tipo e setor
2. **Histórico de Cotações** - Gráficos candlestick interativos
3. **Relatório de Dividendos** - Análise de proventos
4. **Dashboard de Alocação** - Visualização de carteira
5. **Coleta de Dados B3** - Importação automática D-1

### 🔧 **Recursos Técnicos**
- **Classificação automática** de ativos por tipo e setor
- **Sincronização inteligente** - atualiza apenas diferenças
- **Tratamento robusto de erros** com logs detalhados
- **Interface responsiva** que não trava durante operações longas

## 📋 Pré-requisitos

- **Python 3.8+**
- **Docker e Docker Compose** (para PostgreSQL)
- **Conexão com internet** (para coleta B3)

## ⚙️ Instalação

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Iniciar Banco de Dados
```bash
docker-compose up -d
```

### 3. Executar Sistema
```bash
python main.py
```

## 🗂️ Estrutura do Projeto

```
Projeto_Facul/
├── main.py                      # 🚀 Ponto de entrada principal
├── gui_interface.py             # 🎨 Interface gráfica moderna
├── config.py                    # ⚙️ Configurações centralizadas
├── database_manager.py          # 🗃️ Operações de banco
├── data_collector.py            # 📥 Coleta de dados B3
├── data_ingestion_workflow.py   # 🔄 Workflow de importação
├── reports_manager.py           # 📊 Relatórios e consultas
├── reports_workflow.py          # 📈 Workflow de relatórios
├── visualization_manager.py     # 📉 Gráficos interativos
├── requirements.txt             # 📦 Dependências Python
├── schema.sql                   # 🗄️ Estrutura do banco
├── docker-compose.yml           # 🐳 PostgreSQL containerizado
└── docs/                        # 📚 Documentação completa
```

## 🎮 Como Usar

### 1️⃣ **Primeira Execução**
1. Execute `python main.py`
2. Clique em **"⭐ Coletar Dados B3"** para importar dados iniciais
3. Aguarde a conclusão (pode demorar alguns minutos)

### 2️⃣ **Consultas e Relatórios**
1. **Consultar Ativos**: Filtre por tipo (AÇÃO, FII, ETF) e setor
2. **Histórico**: Visualize gráficos de cotações
3. **Dividendos**: Analise proventos distribuídos
4. **Dashboard**: Veja alocação da carteira

### 3️⃣ **Filtros Inteligentes**
- Selecione o **tipo de ativo** primeiro
- Os **setores disponíveis** são carregados automaticamente
- Deixe vazio para ver todos os resultados

## 🏗️ Arquitetura Modular

### **Módulos Principais**
- **`gui_interface.py`**: Interface gráfica com tkinter
- **`database_manager.py`**: Operações de banco com sincronização
- **`data_collector.py`**: Coleta e classificação de ativos B3
- **`visualization_manager.py`**: Gráficos interativos com Plotly
- **`reports_manager.py`**: Consultas e relatórios estruturados

### **Workflows**
- **`data_ingestion_workflow.py`**: Orquestra coleta completa
- **`reports_workflow.py`**: Executa relatórios com visualizações

## 🗃️ Banco de Dados

### **Configuração PostgreSQL**
- **Host**: localhost:5432
- **Database**: b3
- **User**: admin / **Password**: admin

### **Tabelas Principais**
- **`ativos`**: Códigos, nomes, tipos e setores
- **`cotacoes`**: Histórico de preços diários
- **`dividendos`**: Proventos distribuídos
- **`carteira`**: Posições da carteira (opcional)

## 📊 Classificação de Ativos

### **Tipos Identificados**
- **ACAO**: Ações ordinárias e preferenciais
- **FII**: Fundos de Investimento Imobiliário
- **ETF**: Exchange Traded Funds
- **BDR**: Brazilian Depositary Receipts

### **Setores Principais**
- Bancos, Energia Elétrica, Petróleo e Gás
- Mineração e Siderurgia, Telecomunicações
- Alimentos e Bebidas, Construção Civil
- Transporte, Varejo, Saúde, Seguros
- **Outros**: Demais setores não classificados

## 🔧 Solução de Problemas

### **Erro: "Nenhum ativo encontrado"**
✅ Execute **"Coletar Dados B3"** primeiro

### **Erro: "Conexão com banco falhou"**
```bash
# Verificar PostgreSQL
docker ps

# Se não estiver rodando:
docker-compose up -d
```

### **Interface não responde**
✅ Aguarde - operações longas rodam em background

### **Erro de módulos Python**
```bash
pip install -r requirements.txt
```

## 📈 Visualizações Geradas

- **`historico_[CODIGO].html`**: Gráficos candlestick
- **`alocacao_setor.html`**: Dashboard por setor
- **`alocacao_tipo.html`**: Dashboard por tipo
- **`rentabilidade_ativos.html`**: Análise de performance

## 🔗 Integração Externa

### **Power BI**
- Conecte diretamente ao PostgreSQL (localhost:5432)
- Use as consultas em `consultas_powerbi.sql`

### **DBeaver (Recomendado)**
- Download: https://dbeaver.io/
- Conecte com as credenciais do banco
- Explore dados com interface SQL amigável

## 🛠️ Tecnologias

- **Python 3.8+** - Linguagem principal
- **tkinter** - Interface gráfica nativa
- **Pandas** - Manipulação de dados
- **SQLAlchemy** - ORM para banco
- **Plotly** - Gráficos interativos
- **PostgreSQL** - Banco de dados robusto
- **Docker** - Containerização do banco

## 📚 Documentação Completa

Consulte a pasta **`docs/`** para documentação detalhada:
- **Guia de Instalação** - Setup passo a passo
- **Manual de Uso** - Funcionalidades detalhadas  
- **Troubleshooting** - Solução de problemas
- **Arquivos do Sistema** - Explicação técnica

## 🎯 Objetivo do Projeto

Sistema educacional para análise de dados financeiros da B3, desenvolvido com foco em:
- **Usabilidade** - Interface intuitiva e moderna
- **Performance** - Operações otimizadas e não-bloqueantes  
- **Confiabilidade** - Tratamento robusto de erros
- **Escalabilidade** - Arquitetura modular e extensível

---
*Desenvolvido para análise educacional de dados da B3 • Versão com Interface Gráfica*