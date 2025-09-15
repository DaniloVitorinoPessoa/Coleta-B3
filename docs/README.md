# 📚 **DOCUMENTAÇÃO - Sistema B3 com Interface Gráfica**

## 📋 **ÍNDICE DA DOCUMENTAÇÃO**

### **🎨 Interface e Uso**
- [`INTERFACE_GRAFICA.md`](INTERFACE_GRAFICA.md) - **Guia da interface moderna** ⭐
- [`GUIA_USO.md`](GUIA_USO.md) - Como usar o sistema passo a passo
- [`FUNCIONALIDADES.md`](FUNCIONALIDADES.md) - Detalhes de cada funcionalidade

### **⚙️ Instalação e Configuração**
- [`GUIA_INSTALACAO.md`](GUIA_INSTALACAO.md) - Guia completo de instalação
- [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) - Solução de problemas

### **🔧 Documentação Técnica**
- [`ARQUIVOS_SISTEMA.md`](ARQUIVOS_SISTEMA.md) - Explicação de cada arquivo
- [`ESTRUTURA_PROJETO.md`](ESTRUTURA_PROJETO.md) - Arquitetura do sistema

### **📊 Análise e Visualização**
- [`TUTORIAL_DBEAVER.md`](TUTORIAL_DBEAVER.md) - **Tutorial completo DBeaver** ⭐
- [`ANALISE_DADOS.md`](ANALISE_DADOS.md) - DBeaver + Power BI (guia completo)

### **📋 Avaliação**
- [`AVALIACAO_PROJETO.md`](AVALIACAO_PROJETO.md) - Critérios e documentação para avaliação

## 🎯 **VISÃO GERAL DO SISTEMA**

### **O que é o Sistema B3?**
Sistema completo para análise de dados da B3 (Bolsa de Valores brasileira) com **interface gráfica moderna** que:

- ✅ **Interface intuitiva** com pop-ups e janelas organizadas
- ✅ **Coleta automática** de ~14.000 ativos da B3
- ✅ **Classificação inteligente** por tipo e setor
- ✅ **Gráficos interativos** com Plotly
- ✅ **Sincronização robusta** de dados
- ✅ **Integração Power BI** e DBeaver

### **Principais Características**
- **🎨 Interface Moderna**: tkinter com design responsivo
- **🔄 Operações Assíncronas**: Não trava durante operações longas
- **🎯 Filtros Dinâmicos**: Setores carregam baseados no tipo
- **📊 Visualização Rica**: Tabelas navegáveis + gráficos
- **🛡️ Tratamento de Erros**: Logs detalhados e recuperação

### **Tecnologias Utilizadas**
- **Python 3.8+** - Linguagem principal
- **tkinter** - Interface gráfica nativa
- **PostgreSQL** - Banco de dados robusto
- **Pandas** - Manipulação de dados
- **SQLAlchemy** - ORM para banco
- **Plotly** - Gráficos interativos
- **Docker** - Containerização do banco

## 🚀 **INÍCIO RÁPIDO**

### **1. Execução Imediata**
```bash
python main.py
```
*Interface gráfica abre automaticamente*

### **2. Primeira Vez (OBRIGATÓRIO)**
1. Clique em **"⭐ Coletar Dados B3"**
2. Aguarde coleta (~14.000 ativos)
3. Dados prontos para análise!

### **3. Explorar Funcionalidades**
- **📋 Consultar Ativos** - Lista filtrada
- **📈 Histórico** - Gráficos de cotações
- **💰 Dividendos** - Análise de proventos
- **🎯 Dashboard** - Visão geral carteira

## 📊 **FUNCIONALIDADES PRINCIPAIS**

| Interface | Funcionalidade | Descrição |
|-----------|---------------|-----------|
| 🎨 **Pop-ups** | Entrada de dados | Formulários interativos |
| 📋 **Tabelas** | Visualização | Dados organizados em abas |
| 🎯 **Filtros** | Consultas | Filtros dinâmicos inteligentes |
| 📈 **Gráficos** | Análise visual | Candlestick + dashboards |
| 🔄 **Background** | Operações longas | Interface não trava |

## 🗃️ **DADOS DO SISTEMA**

### **Volume de Dados**
- **~14.000 ativos** únicos (ações, FIIs, ETFs, BDRs)
- **Cotações diárias** com preços e volumes
- **Dividendos históricos** com datas e valores
- **Classificação automática** em tipos e setores

### **Tipos de Ativos**
- **AÇÃO** (~13.000): Ações ordinárias e preferenciais
- **FII**: Fundos de Investimento Imobiliário  
- **ETF**: Exchange Traded Funds
- **BDR**: Brazilian Depositary Receipts

### **Setores Identificados**
- **Mineração e Siderurgia** (Vale, CSN)
- **Bancos** (Itaú, Bradesco, Santander)
- **Energia Elétrica** (Eletrobras, Cemig)
- **Petróleo e Gás** (Petrobras)
- **Telecomunicações** (Tim, Telefônica)
- **Outros** (Demais setores)

## 🎓 **PARA DESENVOLVEDORES**

### **Arquitetura Modular**
```
Sistema B3/
├── main.py                    # 🚀 Ponto de entrada
├── gui_interface.py           # 🎨 Interface gráfica
├── database_manager.py        # 🗃️ Operações de banco
├── data_collector.py          # 📥 Coleta e classificação
├── reports_manager.py         # 📊 Relatórios e consultas
├── visualization_manager.py   # 📈 Gráficos interativos
├── workflows/                 # 🔄 Fluxos de trabalho
└── docs/                     # 📚 Documentação
```

### **Fluxo de Dados**
```
B3 API → Coleta → Classificação → PostgreSQL → Interface → Visualização
```

### **Padrões Utilizados**
- **MVC**: Separação de responsabilidades
- **Observer**: Logs em tempo real
- **Factory**: Criação de gráficos
- **Strategy**: Diferentes tipos de relatórios

## 🔗 **INTEGRAÇÃO EXTERNA**

### **DBeaver (Recomendado) ⭐**
```
Host: localhost:5432
Database: b3
Username: admin
Password: admin
```

### **Power BI**
```
Fonte: PostgreSQL
Servidor: localhost:5432
Consultas: consultas_powerbi.sql
```

## 📞 **SUPORTE**

### **Problemas Comuns**
1. **"Nenhum ativo encontrado"** → Execute "Coletar Dados" primeiro
2. **"Erro de conexão"** → Verifique `docker ps` e `docker-compose up -d`
3. **"Interface não responde"** → Normal durante operações longas

### **Diagnóstico**
```bash
# Verificação completa
python -c "from database_manager import DatabaseManager; print('OK' if DatabaseManager().test_connection() else 'ERRO')"

# Módulos Python
python -c "import tkinter, pandas, sqlalchemy, plotly; print('Módulos OK')"
```

### **Documentação Detalhada**
Para dúvidas específicas, consulte:
- [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) - Problemas técnicos
- [`INTERFACE_GRAFICA.md`](INTERFACE_GRAFICA.md) - Uso da interface
- [`GUIA_USO.md`](GUIA_USO.md) - Funcionalidades passo a passo

---

**🎉 Sistema B3 - Interface Moderna para Análise Financeira Profissional** 📊