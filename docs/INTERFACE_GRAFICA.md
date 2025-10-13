# Interface Grafica do Sistema B3

## Visao Geral

O Sistema B3 possui uma **interface grafica moderna e intuitiva** desenvolvida com `tkinter`, proporcionando uma experiencia profissional para analise de dados financeiros.

## Como Executar

### Execucao Padrao (Interface Grafica)
```bash
python main.py
```
**A interface grafica abre automaticamente!**

## Funcionalidades da Interface

### Design Moderno
- **Interface limpa** e profissional
- **Botoes organizados** para cada funcionalidade  
- **Logs em tempo real** das operacoes
- **Pop-ups interativos** para entrada de dados
- **Janelas dedicadas** para resultados
- **Operacoes assincronas** (nao trava)

### Funcionalidades Principais

#### 1. Consultar Ativos
- **Filtros dinamicos**: Tipo → Setor (carrega automaticamente)
- **Pop-up inteligente** com dropdowns
- **Resultado em janela dedicada** com duas abas:
  - **Relatorio**: Lista formatada com estatisticas
  - **Dados**: Tabela navegavel com scroll

#### 2. Historico de Cotacoes  
- **Entrada via pop-up**: Codigo + periodo
- **Botoes separados**: "Buscar Historico" e "Gerar Grafico"
- **Grafico candlestick profissional** estilo TradingView
- **Cores profissionais** (verde/vermelho)
- **Linhas de suporte e resistencia** automaticas
- **Abre automaticamente** no navegador
- **Estatisticas** de performance no resultado

#### 3. Relatorio de Dividendos
- **Filtros opcionais**: Ativo e/ou ano
- **Checkbox** para gerar grafico mensal
- **Resultado tabular** com valores e datas
- **Resumos estatisticos** automaticos

#### 4. Dados Historicos (30d)
- **Botao dedicado**: "Dados Historicos (30d)"
- **Confirmacao via pop-up** antes de executar
- **Progresso em tempo real** nos logs
- **Geracao de 30 dias** de dados simulados
- **Base para graficos completos**

#### 5. Resumo do Sistema
- **Estatisticas gerais** do banco de dados
- **Status de conectividade**
- **Contadores** de registros por tabela

#### 6. Coletar Dados B3
- **Operacao principal** do sistema
- **Download automatico** da B3
- **Logs detalhados** do progresso
- **Classificacao automatica** por tipo/setor

### Aba Dados

Quando aplicavel, os resultados sao exibidos em uma **aba "Dados"** com:
- **Tabela interativa** com scroll horizontal/vertical
- **Colunas redimensionaveis**
- **Dados formatados** e organizados
- **Busca integrada** (quando disponivel)

## Como Usar

### Fluxo Basico

1. **Primeira Execucao:**
   - Execute `python main.py`
   - Interface abre automaticamente
   - Clique: "Coletar Dados B3 (D-1)" (OBRIGATORIO)
   - Aguarde conclusao (~5-10 minutos)

2. **Geracao de Dados Historicos (RECOMENDADO):**
   - Clique: "Dados Historicos (30d)"
   - Confirme no pop-up
   - Aguarde processamento (~3-5 minutos)

3. **Exploracao:**
   - Clique: "Consultar Ativos"
   - Selecione filtros desejados
   - Visualize resultados em abas

4. **Analise Especifica:**
   - Clique: "Historico de Cotacoes"
   - Digite codigo (ex: PETR4)
   - Clique: "Gerar Grafico"
   - Grafico abre no navegador

## Recursos Avancados

### Filtros Inteligentes
- **Tipo de Ativo**: Carrega setores correspondentes
- **Cascata automatica**: Opcoes se ajustam dinamicamente
- **Validacao**: Impede selecoes invalidas

### Operacoes em Background
- **Thread separada** para operacoes longas
- **Interface responsiva** durante processamento
- **Logs em tempo real** mostram progresso
- **Botoes desabilitados** durante execucao

### Tratamento de Erros
- **Pop-ups informativos** para erros
- **Logs detalhados** no console
- **Recuperacao automatica** quando possivel
- **Mensagens claras** para o usuario

## Layout da Interface

```
┌─────────────────────────────────────────────────┐
│ Sistema de Analise B3                           │
├─────────────────────────────────────────────────┤
│ OPERACOES DO SISTEMA                            │
│ [Coletar Dados B3] [Dados Historicos] [Resumo] │
├─────────────────────────────────────────────────┤
│ RELATORIOS E CONSULTAS                          │
│ [Consultar Ativos] [Historico] [Dividendos]    │
├─────────────────────────────────────────────────┤
│ STATUS E LOGS                                   │
│ ┌─────────────────────────────────────────────┐ │
│ │ SUCESSO: Conectado ao PostgreSQL!         │ │
│ │ Iniciando consulta de ativos...           │ │
│ │ Encontrados 1247 ativos do tipo ACAO     │ │
│ │ Consulta concluida com sucesso!           │ │
│ └─────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────┤
│                [Sair]                           │
└─────────────────────────────────────────────────┘
```

## Filtros e Pop-ups

### Pop-up de Consulta de Ativos
```
┌─────────────────────────────────┐
│ Filtros para Consulta de Ativos │
├─────────────────────────────────┤
│ Tipo de Ativo: [ACAO      ▼]   │
│ Setor:         [BANCOS    ▼]   │
├─────────────────────────────────┤
│ Selecione tipo para             │
│ carregar setores                │
├─────────────────────────────────┤
│        [OK]    [Cancelar]       │
└─────────────────────────────────┘
```

### Pop-up de Historico
```
┌─────────────────────────────────┐
│ Historico de Cotacoes           │
├─────────────────────────────────┤
│ Codigo do Ativo: [PETR4____]   │
│ Periodo (dias):  [30_______]   │
├─────────────────────────────────┤
│          [Buscar Historico]     │
│          [Gerar Grafico]        │
│          [Cancelar]             │
└─────────────────────────────────┘
```

## Arquivos Gerados

A interface gera automaticamente:

### Graficos HTML Interativos
- `historico_[CODIGO].html` - Grafico candlestick profissional
  - Cores estilo TradingView (verde/vermelho)
  - Linhas de suporte e resistencia
  - Volume integrado
  - Abre automaticamente no navegador
  
- `dividendos_mensal.html` - Distribuicao de dividendos

### Logs do Sistema
- Logs detalhados na interface
- Historico de operacoes
- Status de conexoes

## Troubleshooting

### Interface nao abre
**Solucao:**
```bash
# Verificar tkinter
python -c "import tkinter; print('OK')"

# Executar com logs
python main.py --verbose
```

### "Nenhum ativo encontrado"
**Solucao:**
1. Execute "Coletar Dados B3" primeiro
2. Aguarde conclusao completa
3. Verifique conexao com PostgreSQL

### Interface trava
Normal: Operacoes longas rodam em background
Aguarde: Logs mostram progresso em tempo real
Nao force: Deixe a operacao concluir

### Graficos nao geram
**Verificar:**
1. Plotly instalado: `pip install plotly`
2. Dados disponíveis no periodo
3. Execute "Dados Historicos (30d)" antes

## Dicas de Uso

### Fluxo Recomendado
1. **Configure** o ambiente (Docker + PostgreSQL)
2. **Colete** dados da B3 (operacao obrigatoria)
3. **Explore** com consultas (Consultar Ativos)
4. **Analise** ativos especificos (Historico)
5. **Gere** dados historicos para graficos completos

### Filtros Inteligentes
- **Sempre selecione tipo primeiro** para carregar setores
- **Use "Todos"** para visao geral
- **Combine filtros** para analises especificas

### Visualizacoes
- **Graficos HTML** sao interativos
- **Zoom** e **pan** disponiveis
- **Hover** mostra detalhes
- **Salve** para apresentacoes

### Usabilidade
- **Operacoes longas** nao travam a interface
- **Logs** mostram progresso em tempo real
- **Pop-ups** guiam entrada de dados
- **Abas** organizam resultados

### Produtividade
- **Execute "Dados Historicos"** para graficos completos
- **Use filtros** para analises focadas
- **Salve graficos** HTML para reutilizar
- **Monitore logs** para acompanhar progresso

### Profissionalismo
- **Graficos estilo TradingView** para apresentacoes
- **Dados organizados** em tabelas limpas
- **Interface intuitiva** para todos os niveis
- **Resultados visuais** impactantes

---

**Interface moderna para analise profissional de dados da B3!**