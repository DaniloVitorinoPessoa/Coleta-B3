# 🎨 Interface Gráfica do Sistema B3

## 📋 Visão Geral

O Sistema B3 possui uma **interface gráfica moderna e intuitiva** desenvolvida com `tkinter`, proporcionando uma experiência profissional para análise de dados financeiros.

## 🚀 Como Executar

### **Execução Padrão (Interface Gráfica)**
```bash
python main.py
```
**A interface gráfica abre automaticamente!**

### **Para usar Interface de Terminal**
```bash
python main.py --terminal
```

## ✨ Funcionalidades da Interface

### 🎯 **Design Moderno**
- **Interface limpa** e profissional
- **Ícones visuais** para cada funcionalidade  
- **Logs em tempo real** das operações
- **Pop-ups interativos** para entrada de dados
- **Janelas dedicadas** para resultados
- **Operações assíncronas** (não trava)

### 📊 **Funcionalidades Principais**

#### **1. 📋 Consultar Ativos**
- **Filtros dinâmicos**: Tipo → Setor (carrega automaticamente)
- **Pop-up inteligente** com dropdowns
- **Resultado em janela dedicada** com duas abas:
  - 📄 **Relatório**: Lista formatada com estatísticas
  - 📊 **Dados**: Tabela navegável com scroll

#### **2. 📈 Histórico de Cotações**  
- **Entrada via pop-up**: Código + período
- **Checkbox** para gerar gráfico
- **Gráfico candlestick** interativo salvo em HTML
- **Estatísticas** de performance no resultado

#### **3. 💰 Relatório de Dividendos**
- **Filtros opcionais**: Ativo e/ou ano
- **Checkbox** para gerar gráfico mensal
- **Resultado tabular** com valores e datas
- **Resumos estatísticos** automáticos

#### **4. 🎯 Dashboard de Alocação**
- **Confirmação** antes de gerar
- **Múltiplos gráficos** criados:
  - Alocação por setor (pizza)
  - Alocação por tipo (pizza)  
  - Rentabilidade por ativo (barras)

#### **5. ⭐ Coletar Dados B3**
- **Confirmação** antes de executar
- **Progresso em tempo real** no log
- **Coleta automática** de ~14.000 ativos
- **Classificação inteligente** por tipo e setor

#### **6. 📋 Resumo do Sistema**
- **Estatísticas do banco** em tempo real
- **Contagem de registros** por tabela
- **Data da última cotação**

## 🪟 Janelas de Resultado Dedicadas

### **📄 Aba Relatório**
- **Texto formatado** com estatísticas
- **Botão copiar** para área de transferência
- **Scroll automático** para navegar

### **📊 Aba Dados**
- **Tabela interativa** com todos os dados
- **Scroll horizontal/vertical**
- **Colunas redimensionáveis**
- **Dados estruturados** para análise

## 🎮 Como Usar (Passo a Passo)

### **1️⃣ Primeira Execução**
```
1. Execute: python main.py
2. Interface abre automaticamente
3. Clique: "⭐ Coletar Dados B3" (OBRIGATÓRIO)
4. Aguarde: Logs mostram progresso
5. Pronto: Dados coletados para análise
```

### **2️⃣ Consultar Ativos**
```
1. Clique: "📋 Consultar Ativos"
2. Pop-up: Selecione tipo (AÇÃO, FII, ETF) ou deixe vazio
3. Setor: Carrega automaticamente baseado no tipo
4. OK: Janela de resultado abre com duas abas
5. Explore: Relatório formatado + tabela navegável
```

### **3️⃣ Análise de Cotações**
```
1. Clique: "📈 Histórico de Cotações"
2. Digite: Código do ativo (ex: PETR4, VALE3)
3. Período: Número de dias (padrão: 30)
4. Gráfico: Marque checkbox para gerar
5. Resultado: Estatísticas + arquivo HTML
```

## 🔄 Recursos Avançados

### **Operações Assíncronas**
- **Threads separadas** para operações longas
- **Interface responsiva** nunca trava
- **Logs em tempo real** mostram progresso
- **Cancelamento seguro** se necessário

### **Filtros Inteligentes**
- **Tipo primeiro**: Selecione AÇÃO, FII, ETF, BDR
- **Setor dinâmico**: Carrega setores disponíveis
- **Cache inteligente**: Evita consultas desnecessárias
- **Validação automática**: Previne erros

### **Tratamento de Erros**
- **Pop-ups informativos** para erros
- **Logs detalhados** para debug
- **Recuperação automática** quando possível
- **Fallback para terminal** se necessário

## 📱 Layout da Interface

```
┌─────────────────────────────────────────────┐
│ 📊 Sistema de Análise B3                    │
├─────────────────────────────────────────────┤
│ 🔧 OPERAÇÕES DO SISTEMA                     │
│ [⭐ Coletar Dados B3] [📋 Resumo Sistema]   │
│ ⚠️ Execute 'Coletar Dados B3' primeiro     │
├─────────────────────────────────────────────┤
│ 📊 RELATÓRIOS E CONSULTAS                   │
│ [📋 Consultar Ativos] [📈 Histórico]       │
│ [💰 Dividendos]       [🎯 Dashboard]       │
│ [🚀 Executar Todos]                        │
├─────────────────────────────────────────────┤
│ 📝 STATUS E LOGS                            │
│ ┌─────────────────────────────────────────┐ │
│ │ 🔌 Testando conexão com banco...       │ │
│ │ ✅ SUCESSO: Conectado ao PostgreSQL!   │ │
│ │ 📊 Iniciando consulta de ativos...     │ │
│ │ ⏳ Processando 14.252 registros...     │ │
│ │ ✅ Consulta concluída com sucesso!     │ │
│ └─────────────────────────────────────────┘ │
├─────────────────────────────────────────────┤
│                [❌ Sair]                    │
└─────────────────────────────────────────────┘
```

## 🎯 Filtros e Pop-ups

### **Pop-up de Consulta de Ativos**
```
┌─────────────────────────────┐
│ Filtros para Consulta       │
├─────────────────────────────┤
│ Tipo de Ativo:              │
│ [ACAO ▼] (Dropdown)         │
│                             │
│ Setor:                      │
│ [Bancos ▼] (Dinâmico)       │
│                             │
│ 💡 Selecione tipo para      │
│    filtrar setores          │
├─────────────────────────────┤
│      [OK]    [Cancelar]     │
└─────────────────────────────┘
```

### **Pop-up de Histórico**
```
┌─────────────────────────────┐
│ Histórico de Cotações       │
├─────────────────────────────┤
│ Código do Ativo:            │
│ [PETR4____________]         │
│                             │
│ Período (dias):             │
│ [30_______________]         │
│                             │
│ ☑ Gerar gráfico             │
├─────────────────────────────┤
│      [OK]    [Cancelar]     │
└─────────────────────────────┘
```

## 📈 Arquivos Gerados

Todos os gráficos são salvos como **HTML interativo**:

- **`historico_[CODIGO].html`** - Gráfico candlestick
- **`alocacao_setor.html`** - Pizza por setor
- **`alocacao_tipo.html`** - Pizza por tipo
- **`rentabilidade_ativos.html`** - Barras de performance
- **`dividendos_mensal.html`** - Dividendos mensais

## 🔧 Troubleshooting

### **❌ Interface não abre**
```bash
# Fallback para terminal
python main.py --terminal

# Verificar tkinter (Linux)
sudo apt-get install python3-tk
```

### **❌ "Nenhum ativo encontrado"**
```
Solução: Execute "⭐ Coletar Dados B3" primeiro
```

### **❌ Interface trava**
```
✅ Normal: Operações longas rodam em background
✅ Aguarde: Logs mostram progresso em tempo real
✅ Não force: Deixe a operação concluir
```

### **❌ Gráficos não geram**
```bash
# Verificar Plotly
pip install plotly

# Verificar permissões de escrita
ls -la *.html
```

## 💡 Dicas de Uso

### **🎯 Fluxo Recomendado**
1. **Execute** `python main.py`
2. **Colete dados** primeiro (⭐ Coletar Dados B3)
3. **Explore** com consultas (📋 Consultar Ativos)
4. **Analise** ativos específicos (📈 Histórico)
5. **Visualize** dashboards (🎯 Dashboard)

### **🔍 Filtros Inteligentes**
- **Tipo primeiro**: Sempre selecione tipo antes do setor
- **Cache**: Setores são carregados uma vez por tipo
- **Vazio = Todos**: Deixe filtros vazios para ver tudo
- **Combinação**: Use tipo + setor para filtros específicos

### **📊 Visualizações**
- **HTML interativo**: Abra gráficos no navegador
- **Zoom e pan**: Gráficos são totalmente interativos
- **Exportação**: Use botões do Plotly para salvar
- **Responsivo**: Gráficos se adaptam ao tamanho

## 🚀 Vantagens da Interface Gráfica

### **✅ Usabilidade**
- **Cliques simples** substituem comandos
- **Validação automática** previne erros
- **Feedback visual** imediato
- **Não precisa memorizar** códigos

### **✅ Produtividade**
- **Operações paralelas** não travam
- **Resultados organizados** em janelas
- **Logs em tempo real** para acompanhar
- **Acesso rápido** a todas as funções

### **✅ Profissionalismo**
- **Interface moderna** e limpa
- **Dados estruturados** em tabelas
- **Gráficos interativos** de qualidade
- **Experiência consistente** multiplataforma

---

**🎉 Interface moderna para análise profissional de dados da B3!** 📊