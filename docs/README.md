# DOCUMENTACAO - Sistema B3 com Interface Grafica

## INDICE DA DOCUMENTACAO

### Interface e Uso
- [`INTERFACE_GRAFICA.md`](INTERFACE_GRAFICA.md) - Guia da interface moderna
- [`GUIA_USO.md`](GUIA_USO.md) - Como usar o sistema passo a passo
- [`FUNCIONALIDADES.md`](FUNCIONALIDADES.md) - Detalhes de cada funcionalidade

### Instalacao e Configuracao
- [`GUIA_INSTALACAO.md`](GUIA_INSTALACAO.md) - Guia completo de instalacao
- [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) - Solucao de problemas

### Documentacao Tecnica
- [`ARQUIVOS_SISTEMA.md`](ARQUIVOS_SISTEMA.md) - Explicacao de cada arquivo
- [`ESTRUTURA_PROJETO.md`](ESTRUTURA_PROJETO.md) - Arquitetura do sistema

### Analise e Visualizacao
- [`TUTORIAL_DBEAVER.md`](TUTORIAL_DBEAVER.md) - Tutorial completo DBeaver
- [`ANALISE_DADOS.md`](ANALISE_DADOS.md) - DBeaver + Power BI (guia completo)

### Avaliacao
- [`AVALIACAO_PROJETO.md`](AVALIACAO_PROJETO.md) - Criterios e documentacao para avaliacao

## VISAO GERAL DO SISTEMA

### O que e o Sistema B3?
Sistema completo para analise de dados da B3 (Bolsa de Valores brasileira) com interface grafica moderna que:

- Interface intuitiva com pop-ups e janelas organizadas
- Coleta automatica de ~14.000 ativos da B3
- Classificacao inteligente por tipo e setor
- Graficos interativos com Plotly
- Sincronizacao robusta de dados
- Integracao Power BI e DBeaver
- Dados historicos simulados para analises completas

### Principais Caracteristicas
- **Interface Moderna**: tkinter com design responsivo
- **Operacoes Assincronas**: Nao trava durante operacoes longas
- **Filtros Dinamicos**: Setores carregam baseados no tipo
- **Visualizacao Rica**: Tabelas navegaveis + graficos profissionais
- **Tratamento de Erros**: Logs detalhados e recuperacao
- **Graficos Candlestick**: Estilo TradingView com suporte/resistencia

### Tecnologias Utilizadas
- **Python 3.8+** - Linguagem principal
- **tkinter** - Interface grafica nativa
- **PostgreSQL** - Banco de dados robusto
- **Pandas** - Manipulacao de dados
- **SQLAlchemy** - ORM para banco
- **Plotly** - Graficos interativos profissionais
- **Docker** - Containerizacao do banco

## INICIO RAPIDO

### 1. Execucao Imediata
```bash
python main.py
```
*Interface grafica abre automaticamente*

### 2. Primeira Vez (OBRIGATORIO)
1. Clique em **"Coletar Dados B3 (D-1)"**
2. Aguarde coleta (~14.000 ativos)
3. Clique em **"Dados Historicos (30d)"** (RECOMENDADO)
4. Dados prontos para analise completa!

### 3. Explorar Funcionalidades
- **Consultar Ativos** - Lista filtrada
- **Historico de Cotacoes** - Graficos candlestick profissionais
- **Relatorio de Dividendos** - Analise de proventos
- **Dados Historicos** - 30 dias de dados simulados
- **Resumo do Sistema** - Estatisticas gerais

## FUNCIONALIDADES PRINCIPAIS

| Interface | Funcionalidade | Descricao |
|-----------|---------------|-----------|
| Pop-ups | Entrada de dados | Formularios interativos |
| Tabelas | Visualizacao | Dados organizados em abas |
| Filtros | Consultas | Filtros dinamicos inteligentes |
| Graficos | Analise visual | Candlestick + dashboards profissionais |
| Background | Operacoes longas | Interface nao trava |

## DADOS DO SISTEMA

### Volume de Dados
- **~14.000 ativos** unicos (acoes, FIIs, ETFs, BDRs)
- **Cotacoes diarias** com precos OHLC e volumes
- **Dividendos historicos** com datas e valores
- **Classificacao automatica** em tipos e setores
- **30 dias de dados historicos** simulados

### Tipos de Ativos
- **ACAO** (~13.000): Acoes ordinarias e preferenciais
- **FII**: Fundos de Investimento Imobiliario  
- **ETF**: Exchange Traded Funds
- **BDR**: Brazilian Depositary Receipts

### Setores Identificados
- **Mineracao e Siderurgia** (Vale, CSN)
- **Bancos** (Itau, Bradesco, Santander)
- **Energia Eletrica** (Eletrobras, Cemig)
- **Petroleo e Gas** (Petrobras)
- **Telecomunicacoes** (Tim, Telefonica)
- **Outros** (Demais setores)

## PARA DESENVOLVEDORES

### Arquitetura Modular
```
Sistema B3/
├── main.py                    # Ponto de entrada
├── gui_interface.py           # Interface grafica
├── database_manager.py        # Operacoes de banco
├── data_collector.py          # Coleta e classificacao
├── reports_manager.py         # Relatorios e consultas
├── visualization_manager.py   # Graficos interativos
├── workflows/                 # Fluxos de trabalho
└── docs/                     # Documentacao
```

### Fluxo de Dados
```
B3 API → Coleta → Classificacao → PostgreSQL → Interface → Visualizacao
```

### Padroes Utilizados
- **MVC**: Separacao de responsabilidades
- **Observer**: Logs em tempo real
- **Factory**: Criacao de graficos
- **Strategy**: Diferentes tipos de relatorios

## INTEGRACAO EXTERNA

### DBeaver (Recomendado)
```
Host: localhost:5432
Database: b3
Username: admin
Password: admin
```

### Power BI
```
Fonte: PostgreSQL
Servidor: localhost:5432
Consultas: consultas_powerbi.sql
```

## SUPORTE

### Problemas Comuns
1. **"Nenhum ativo encontrado"** → Execute "Coletar Dados B3" primeiro
2. **"Erro de conexao"** → Verifique `docker ps` e `docker-compose up -d`
3. **"Interface nao responde"** → Normal durante operacoes longas
4. **"Nenhum dado para grafico"** → Execute "Dados Historicos (30d)"

### Diagnostico
```bash
# Verificacao completa
python -c "from database_manager import DatabaseManager; print('OK' if DatabaseManager().test_connection() else 'ERRO')"

# Modulos Python
python -c "import tkinter, pandas, sqlalchemy, plotly; print('Modulos OK')"
```

### Documentacao Detalhada
Para duvidas especificas, consulte:
- [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) - Problemas tecnicos
- [`INTERFACE_GRAFICA.md`](INTERFACE_GRAFICA.md) - Uso da interface
- [`GUIA_USO.md`](GUIA_USO.md) - Funcionalidades passo a passo

---

**Sistema B3 - Interface Moderna para Analise Financeira Profissional**