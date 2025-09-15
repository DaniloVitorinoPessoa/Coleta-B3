# 🚀 **GUIA COMPLETO DE INSTALAÇÃO - SISTEMA B3**

## 📋 **PRÉ-REQUISITOS**

### **Sistema Operacional**
- ✅ Windows 10/11
- ✅ Linux (Ubuntu, CentOS, etc.)
- ✅ macOS 10.15+

### **Software Necessário**
- ✅ **Python 3.8+** (recomendado 3.9+)
- ✅ **Docker Desktop** (para PostgreSQL)
- ✅ **Git** (opcional, para clonagem)

### **Hardware Mínimo**
- ✅ **RAM**: 4GB (recomendado 8GB)
- ✅ **Disco**: 2GB livres
- ✅ **Internet**: Para download dos dados B3

---

## 🎯 **INSTALAÇÃO AUTOMÁTICA (RECOMENDADA)**

### **Windows**
```batch
# 1. Baixar o projeto
git clone <url-do-projeto>
cd Projeto_Facul

# 2. Executar instalação automática
iniciar.bat
```

### **Linux/Mac**
```bash
# 1. Baixar o projeto
git clone <url-do-projeto>
cd Projeto_Facul

# 2. Dar permissão de execução
chmod +x iniciar.sh

# 3. Executar instalação automática
./iniciar.sh
```

### **O que a instalação automática faz:**
1. ✅ Verifica Python e Docker
2. ✅ Instala dependências Python
3. ✅ Inicia PostgreSQL com Docker
4. ✅ Cria tabelas no banco
5. ✅ Testa todas as conexões
6. ✅ Executa o sistema principal

---

## 🔧 **INSTALAÇÃO MANUAL PASSO A PASSO**

### **Passo 1: Verificar Python**
```bash
# Verificar versão do Python
python --version
# ou
python3 --version

# Deve retornar Python 3.8+ 
```

**Se não tiver Python:**
- **Windows**: Baixar de https://python.org
- **Linux**: `sudo apt install python3 python3-pip`
- **Mac**: `brew install python3`

### **Passo 2: Instalar Docker**
```bash
# Verificar se Docker está instalado
docker --version
docker-compose --version
```

**Se não tiver Docker:**
- **Windows/Mac**: Baixar Docker Desktop
- **Linux**: 
  ```bash
  sudo apt update
  sudo apt install docker.io docker-compose
  sudo usermod -aG docker $USER
  # Reiniciar sessão
  ```

### **Passo 3: Baixar o Projeto**
```bash
# Opção 1: Git (recomendado)
git clone <url-do-projeto>
cd Projeto_Facul

# Opção 2: Download ZIP
# Baixar e extrair o arquivo ZIP
cd Projeto_Facul
```

### **Passo 4: Instalar Dependências Python**
```bash
# Instalar bibliotecas necessárias
pip install -r requirements.txt

# Ou no Linux/Mac se der erro:
pip3 install -r requirements.txt
```

### **Passo 5: Iniciar Banco de Dados**
```bash
# Iniciar PostgreSQL com Docker
docker-compose up -d

# Verificar se está rodando
docker ps
```

### **Passo 6: Configurar Banco**
```bash
# Executar setup automático
python setup.py

# Ou criar tabelas manualmente
# docker exec -it postgres_b3 psql -U admin -d b3 -f schema.sql
```

### **Passo 7: Testar Sistema**
```bash
# Verificar se tudo está funcionando
python diagnostico.py

# Executar sistema principal
python main.py
```

---

## 🔍 **VERIFICAÇÃO DA INSTALAÇÃO**

### **Teste Rápido**
```bash
# 1. Testar diagnóstico
python diagnostico.py

# Deve mostrar:
# ✅ Python
# ✅ Módulos  
# ✅ Docker
# ✅ Docker Compose
# ✅ Arquivos
# ✅ Banco de Dados
# ✅ Conexão B3
```

### **Teste Completo**
```bash
# 1. Executar sistema
python main.py

# 2. Escolher opção 5 (Coletar Dados B3)
# 3. Aguardar conclusão (~2-5 minutos)
# 4. Escolher opção 1 (Consultar Ativos)
# 5. Deve mostrar lista de ativos
```

---

## 🛠️ **SOLUÇÃO DE PROBLEMAS COMUNS**

### **❌ Erro: "Python não encontrado"**
```bash
# Windows: Adicionar Python ao PATH
# Ou usar:
py -3 main.py

# Linux/Mac: Usar python3
python3 main.py
```

### **❌ Erro: "Docker não encontrado"**
```bash
# Windows/Mac: Instalar Docker Desktop
# Linux:
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
```

### **❌ Erro: "Módulo não encontrado"**
```bash
# Instalar dependências
pip install -r requirements.txt

# Se persistir:
pip install pandas sqlalchemy psycopg2-binary requests plotly
```

### **❌ Erro: "Conexão com banco falhou"**
```bash
# Verificar se PostgreSQL está rodando
docker ps

# Se não estiver:
docker-compose up -d

# Aguardar 10-15 segundos e tentar novamente
```

### **❌ Erro: "Permissão negada (Linux/Mac)"**
```bash
# Dar permissão aos scripts
chmod +x iniciar.sh
chmod +x *.py

# Ou executar com sudo se necessário
sudo python3 main.py
```

### **❌ Erro: "Porta 5432 em uso"**
```bash
# Parar outros PostgreSQL
sudo systemctl stop postgresql

# Ou usar porta diferente no docker-compose.yml
# Alterar "5432:5432" para "5433:5432"
```

---

## 🗄️ **VISUALIZAÇÃO DOS DADOS (DBeaver)**

### **Instalação do DBeaver**
1. Baixar DBeaver Community: https://dbeaver.io/download/
2. Instalar e executar o DBeaver
3. Configurar conexão com PostgreSQL

### **Configurar Conexão DBeaver**
1. **Nova Conexão**: PostgreSQL
2. **Configurações**:
   ```
   Host: localhost
   Port: 5432
   Database: b3
   Username: admin
   Password: admin
   ```
3. **Testar Conexão** e **Finalizar**

### **Navegação no DBeaver**
```
b3 (Database)
├── public (Schema)
│   ├── ativos (Table)          # ~11.500 ativos
│   ├── cotacoes (Table)        # ~11.500+ cotações
│   └── dividendos (Table)      # Dividendos/Proventos
```

### **Consultas Úteis no DBeaver**
```sql
-- Ver todos os ativos
SELECT * FROM ativos LIMIT 100;

-- Ver cotações mais recentes
SELECT a.codigo, a.nome, c.data, c.preco_fechamento, c.volume_financeiro
FROM cotacoes c
JOIN ativos a ON c.id_ativo = a.id
ORDER BY c.data DESC, c.volume_financeiro DESC
LIMIT 50;

-- Ver dividendos
SELECT a.codigo, a.nome, d.data, d.valor, d.tipo
FROM dividendos d
JOIN ativos a ON d.id_ativo = a.id
ORDER BY d.data DESC;
```

## 🌐 **CONFIGURAÇÕES DE REDE**

### **Firewall (Windows)**
1. Abrir "Windows Defender Firewall"
2. Permitir aplicativo através do firewall
3. Adicionar Python, Docker e DBeaver

### **Proxy Corporativo**
```bash
# Configurar proxy para pip
pip install --proxy http://proxy:porta -r requirements.txt

# Configurar proxy para Docker
# Adicionar no Docker Desktop → Settings → Resources → Proxies
```

---

## 🔧 **CONFIGURAÇÕES AVANÇADAS**

### **Alterar Configurações de Banco**
Editar `config.py`:
```python
DATABASE_CONFIG = {
    'host': 'localhost',      # Alterar se necessário
    'port': '5432',          # Alterar se necessário  
    'database': 'b3',
    'username': 'admin',
    'password': 'admin'      # Alterar senha se necessário
}
```

### **Configurar Memória Docker**
No Docker Desktop:
1. Settings → Resources → Advanced
2. Aumentar Memory para 4GB+
3. Restart Docker

### **Logs Detalhados**
Adicionar no início dos arquivos Python:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 📊 **PRIMEIRA EXECUÇÃO**

### **Fluxo Recomendado:**
```bash
# 1. Instalação
iniciar.bat  # ou ./iniciar.sh

# 2. Primeira coleta (OBRIGATÓRIO)
python main.py
# Escolher opção 5: "Coletar Dados B3 (D-1)"
# Aguardar 2-5 minutos

# 3. Testar funcionalidades
# Escolher opção 1: "Consultar Ativos"
# Escolher opção 4: "Dashboard de Alocação"

# 4. Integrar com Power BI (opcional)
# Seguir guia em POWER_BI_SETUP.md
```

---

## 🎯 **ESTRUTURA PÓS-INSTALAÇÃO**

```
Projeto_Facul/
├── 📁 data/              # Dados PostgreSQL
├── 📁 docs/              # Documentação
├── 📁 __pycache__/       # Cache Python
├── 🐍 main.py            # Sistema principal
├── ⚙️ config.py          # Configurações
├── 🗄️ database_manager.py # Banco de dados
├── 📊 data_collector.py   # Coleta B3
├── 📈 reports_manager.py  # Relatórios
├── 🎨 visualization_manager.py # Gráficos
├── 🔄 *_workflow.py      # Workflows
├── 🐳 docker-compose.yml # PostgreSQL
├── 📄 schema.sql         # Estrutura BD
├── 📋 requirements.txt   # Dependências
└── 📚 README.md          # Documentação
```

---

## ✅ **CHECKLIST DE INSTALAÇÃO**

- [ ] Python 3.8+ instalado
- [ ] Docker Desktop instalado e rodando
- [ ] Projeto baixado/clonado
- [ ] Dependências Python instaladas (`pip install -r requirements.txt`)
- [ ] PostgreSQL iniciado (`docker-compose up -d`)
- [ ] Tabelas criadas (`python setup.py`)
- [ ] Sistema testado (`python diagnostico.py`)
- [ ] Primeira coleta realizada (opção 5)
- [ ] Funcionalidades testadas (opções 1-4)

---

## 🎉 **INSTALAÇÃO CONCLUÍDA!**

Se todos os passos foram executados com sucesso:

```bash
python main.py
```

Deve exibir:
```
Conectando ao banco de dados...
SUCESSO: Conectado com sucesso!

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

**🎯 Sistema B3 pronto para uso!** 🚀

---

## 📞 **SUPORTE**

Se encontrar problemas:
1. Execute `python diagnostico.py`
2. Consulte `docs/TROUBLESHOOTING.md`
3. Verifique logs no console
4. Reinicie Docker se necessário

**Sistema B3 - Instalação Completa e Funcional** 💻
