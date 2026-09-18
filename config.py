# ====================================
# CONFIGURACOES CENTRALIZADAS
# ====================================

import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine

# Configurações do Banco de Dados
# As credenciais são lidas de variáveis de ambiente (arquivo .env).
# Consulte .env.example para os nomes esperados.
DATABASE_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
    "database": os.getenv("POSTGRES_DB", "b3"),
    "username": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}

if not DATABASE_CONFIG["username"] or not DATABASE_CONFIG["password"]:
    raise RuntimeError(
        "Defina POSTGRES_USER e POSTGRES_PASSWORD no arquivo .env "
        "(veja .env.example) antes de executar o projeto."
    )

# String de conexão
DATABASE_URL = f"postgresql+psycopg2://{DATABASE_CONFIG['username']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"

# Engine do SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={"connect_timeout": 10},
)

# Configurações da B3
B3_CONFIG = {
    "cotahist_url": "https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/cotacoes-historicas/",
    "cotahist_url_2025": "https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A2025.ZIP",
    "cotahist_direct_url": "https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A{}.ZIP",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "timeout": 30,
    "colunas_csv": [
        "TIPREG",
        "DATA",
        "CODBDI",
        "CODNEG",
        "TPMERC",
        "NOMRES",
        "ESPECI",
        "PRAZOT",
        "MODREF",
        "PREABE",
        "PREMAX",
        "PREMIN",
        "PREMED",
        "PREULT",
        "PREOFC",
        "PREOFV",
        "TOTNEG",
        "QUATOTNEG",
        "VOLTOT",
        "PREEXE",
        "INDOPC",
        "DATVEN",
        "FATCOT",
        "PTOEXE",
        "CODISI",
        "DISMES",
    ],
}

# Configurações de Log
LOG_CONFIG = {
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "level": "INFO",
}


def calcular_d1():
    """Calcula D-1 considerando apenas dias úteis"""
    hoje = datetime.now().date()
    data_d1 = hoje - timedelta(days=1)

    if hoje.weekday() == 0:  # Segunda-feira
        data_d1 = hoje - timedelta(days=3)
    elif hoje.weekday() == 6:  # Domingo
        data_d1 = hoje - timedelta(days=2)

    return data_d1


def get_cotahist_url():
    """Retorna a URL do COTAHIST baseada no ano atual"""
    ano_atual = datetime.now().year

    # URL direta com ano dinâmico
    url = f"https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A{ano_atual}.ZIP"

    return url
