# 🔧 **GUIA DE SOLUÇÃO DE PROBLEMAS - SISTEMA B3**

## 🚨 **PROBLEMAS MAIS COMUNS**

---

## ❌ **ERRO: "Python não encontrado"**

### **Sintomas:**
```
'python' is not recognized as an internal or external command
```

### **Soluções:**

#### **Windows:**
```batch
# Opção 1: Usar py
py main.py
py -3 main.py

# Opção 2: Adicionar Python ao PATH
# Painel de Controle → Sistema → Variáveis de Ambiente
# Adicionar: C:\Python39\ e C:\Python39\Scripts\
```

#### **Linux/Mac:**
```bash
# Usar python3
python3 main.py

# Instalar Python se necessário
# Ubuntu/Debian:
sudo apt update
sudo apt install python3 python3-pip

# CentOS/RHEL:
sudo yum install python3 python3-pip

# macOS:
brew install python3
```

---

## ❌ **ERRO: "Docker não encontrado"**

### **Sintomas:**
```
docker: command not found
Cannot connect to the Docker daemon
```

### **Soluções:**

#### **Windows/Mac:**
1. Baixar e instalar **Docker Desktop**
2. Reiniciar o computador
3. Abrir Docker Desktop antes de usar o sistema

#### **Linux:**
```bash
# Ubuntu/Debian:
sudo apt update
sudo apt install docker.io docker-compose

# CentOS/RHEL:
sudo yum install docker docker-compose

# Iniciar serviço:
sudo systemctl start docker
sudo systemctl enable docker

# Adicionar usuário ao grupo docker:
sudo usermod -aG docker $USER
# Reiniciar sessão
```

#### **Verificação:**
```bash
docker --version
docker-compose --version
docker ps
```

---

## ❌ **ERRO: "Módulo não encontrado"**

### **Sintomas:**
```
ModuleNotFoundError: No module named 'pandas'
ImportError: No module named 'sqlalchemy'
```

### **Soluções:**

#### **Instalar todas as dependências:**
```bash
pip install -r requirements.txt

# Se der erro de permissão:
pip install --user -r requirements.txt

# Linux/Mac:
pip3 install -r requirements.txt
sudo pip3 install -r requirements.txt
```

#### **Instalar módulos individualmente:**
```bash
pip install pandas>=1.5.0
pip install sqlalchemy>=1.4.0
pip install psycopg2-binary>=2.9.0
pip install requests>=2.28.0
pip install plotly>=5.0.0
pip install matplotlib>=3.5.0
```

#### **Verificar instalação:**
```bash
python -c "import pandas, sqlalchemy, psycopg2, requests, plotly; print('Módulos OK')"
```

---

## ❌ **ERRO: "Conexão com banco falhou"**

### **Sintomas:**
```
ERRO: Não foi possível conectar ao banco de dados
psycopg2.OperationalError: could not connect to server
```

### **Soluções:**

#### **1. Verificar se PostgreSQL está rodando:**
```bash
docker ps
# Deve mostrar container postgres_b3
```

#### **2. Se não estiver rodando:**
```bash
docker-compose up -d
# Aguardar 10-15 segundos
docker ps
```

#### **3. Se ainda não funcionar:**
```bash
# Parar tudo e reiniciar
docker-compose down
docker-compose up -d

# Aguardar 30 segundos
python main.py
```

#### **4. Verificar logs do PostgreSQL:**
```bash
docker logs postgres_b3
```

#### **5. Porta em uso:**
```bash
# Verificar se porta 5432 está em uso
netstat -an | grep 5432

# Parar outros PostgreSQL
sudo systemctl stop postgresql
# Ou alterar porta no docker-compose.yml
```

---

## ❌ **ERRO: "Dados da B3 não encontrados"**

### **Sintomas:**
```
Nenhum dado encontrado para 2025-09-09
Possiveis motivos: feriado, fim de semana, dados nao disponiveis
```

### **Soluções:**

#### **1. Verificar se é dia útil:**
- Sábados/domingos não têm dados
- Feriados nacionais não têm dados
- Sistema usa automaticamente data mais recente

#### **2. Verificar conexão com internet:**
```bash
ping google.com
curl -I https://bvmf.bmfbovespa.com.br
```

#### **3. Tentar novamente:**
```bash
python main.py
# Opção 5: Coletar Dados B3
```

#### **4. Verificar logs detalhados:**
O sistema mostra datas disponíveis no arquivo.

---

## ❌ **ERRO: "Arquivo não encontrado"**

### **Sintomas:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'main.py'
```

### **Soluções:**

#### **1. Verificar diretório atual:**
```bash
pwd  # Linux/Mac
cd   # Windows

# Deve estar em: .../Projeto_Facul/
```

#### **2. Navegar para pasta correta:**
```bash
cd Projeto_Facul
ls  # ou dir no Windows
# Deve mostrar main.py, config.py, etc.
```

#### **3. Verificar se arquivos existem:**
```bash
ls -la main.py
# Deve mostrar o arquivo
```

---

## ❌ **ERRO: "Permissão negada"**

### **Sintomas (Linux/Mac):**
```
Permission denied: './iniciar.sh'
PermissionError: [Errno 13] Permission denied
```

### **Soluções:**
```bash
# Dar permissão aos scripts
chmod +x iniciar.sh
chmod +x *.py

# Ou executar com sudo
sudo python3 main.py

# Verificar proprietário dos arquivos
ls -la
chown $USER:$USER *.py
```

---

## ❌ **ERRO: "Porta em uso"**

### **Sintomas:**
```
Error starting userland proxy: listen tcp 0.0.0.0:5432: bind: address already in use
```

### **Soluções:**

#### **1. Parar PostgreSQL local:**
```bash
# Linux:
sudo systemctl stop postgresql

# Mac:
brew services stop postgresql

# Windows:
# Parar serviço PostgreSQL no Gerenciador de Serviços
```

#### **2. Alterar porta no Docker:**
Editar `docker-compose.yml`:
```yaml
ports:
  - "5433:5432"  # Em vez de 5432:5432
```

Editar `config.py`:
```python
DATABASE_CONFIG = {
    'port': '5433',  # Em vez de 5432
    # ...
}
```

---

## ❌ **ERRO: "Gráfico não abre"**

### **Sintomas:**
```
Arquivo historico_PETR4.html criado mas não abre
```

### **Soluções:**

#### **1. Abrir manualmente:**
```bash
# Windows:
start historico_PETR4.html

# Mac:
open historico_PETR4.html

# Linux:
xdg-open historico_PETR4.html
```

#### **2. Verificar navegador padrão:**
- Definir Chrome/Firefox como padrão
- Tentar abrir arquivo diretamente no navegador

#### **3. Verificar se arquivo foi criado:**
```bash
ls -la *.html
# Deve mostrar arquivos HTML
```

---

## 🔍 **DIAGNÓSTICO AUTOMÁTICO**

### **Executar diagnóstico completo:**
```bash
python diagnostico.py
```

### **Resultado esperado:**
```
✅ Python
✅ Módulos
✅ Docker
✅ Docker Compose
✅ Arquivos
✅ Banco de Dados
✅ Conexão B3

🎉 SISTEMA PRONTO PARA USO!
```

### **Se aparecer ❌:**
Cada erro tem uma descrição específica do problema.

---

## 🛠️ **COMANDOS DE VERIFICAÇÃO RÁPIDA**

### **Testar Python:**
```bash
python --version
python -c "print('Python OK')"
```

### **Testar Docker:**
```bash
docker --version
docker ps
```

### **Testar banco:**
```bash
python -c "from database_manager import DatabaseManager; print('OK' if DatabaseManager().test_connection() else 'ERRO')"
```

### **Testar módulos:**
```bash
python -c "import pandas, sqlalchemy, psycopg2, requests, plotly; print('Módulos OK')"
```

---

## 🔄 **RESET COMPLETO DO SISTEMA**

### **Se nada funcionar:**
```bash
# 1. Parar tudo
docker-compose down
docker system prune -f

# 2. Remover dados
sudo rm -rf data/  # CUIDADO: Remove todos os dados!

# 3. Reinstalar dependências
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# 4. Reiniciar
docker-compose up -d
python setup.py
python main.py
```

---

## 🌐 **PROBLEMAS DE REDE**

### **Proxy corporativo:**
```bash
# Configurar proxy para pip
pip install --proxy http://proxy:porta -r requirements.txt

# Configurar proxy para Docker
# Docker Desktop → Settings → Resources → Proxies
```

### **Firewall:**
- **Windows**: Permitir Python e Docker no Windows Defender
- **Linux**: Configurar iptables se necessário
- **Corporativo**: Liberar portas 5432 e 80/443

---

## 📱 **PROBLEMAS ESPECÍFICOS POR SO**

### **Windows 11:**
- Executar como Administrador se necessário
- Verificar Windows Subsystem for Linux (WSL)
- Desabilitar antivírus temporariamente para teste

### **macOS:**
- Dar permissão para Docker no System Preferences
- Usar Homebrew para instalar dependências
- Verificar Xcode Command Line Tools

### **Linux:**
- Verificar SELinux/AppArmor
- Instalar build-essential se necessário
- Configurar sudo sem senha para Docker

---

## 📞 **QUANDO PEDIR AJUDA**

### **Informações para fornecer:**
1. **Sistema operacional** e versão
2. **Versão do Python** (`python --version`)
3. **Mensagem de erro completa**
4. **Resultado do diagnóstico** (`python diagnostico.py`)
5. **Logs do Docker** (`docker logs postgres_b3`)

### **Logs úteis:**
```bash
# Executar com logs detalhados
python main.py 2>&1 | tee sistema.log

# Ver logs do PostgreSQL
docker logs postgres_b3

# Verificar espaço em disco
df -h  # Linux/Mac
dir   # Windows
```

---

## ✅ **CHECKLIST DE VERIFICAÇÃO**

Antes de relatar problema:

- [ ] Python 3.8+ instalado e funcionando
- [ ] Docker Desktop instalado e rodando
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] PostgreSQL iniciado (`docker-compose up -d`)
- [ ] Diagnóstico executado (`python diagnostico.py`)
- [ ] Arquivos principais existem (main.py, config.py, etc.)
- [ ] Internet funcionando
- [ ] Sem proxy/firewall bloqueando

---

## 🎯 **PROBLEMAS CONHECIDOS E SOLUÇÕES**

### **1. SQLAlchemy 2.0+ compatibility:**
✅ **Resolvido** - Sistema usa `text()` para queries

### **2. Duplicatas na opção 5:**
✅ **Resolvido** - Sistema usa UPSERT automático

### **3. Encoding do COTAHIST:**
✅ **Resolvido** - Sistema tenta múltiplos encodings

### **4. Posições fixas CSV:**
✅ **Resolvido** - Layout oficial implementado

---

**Sistema B3 - Suporte Técnico Completo** 🛠️
