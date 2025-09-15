# ====================================
# CONFIGURACOES CENTRALIZADAS
# ====================================

import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine

# Configurações do Banco de Dados
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'b3',
    'username': 'admin',
    'password': 'admin'
}

# String de conexão
DATABASE_URL = f"postgresql+psycopg2://{DATABASE_CONFIG['username']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"

# Engine do SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={
        "connect_timeout": 10
    }
)

# Configurações da B3
B3_CONFIG = {
    'cotahist_url': 'https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A2024.ZIP',
    'cotahist_url_2025': 'https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A2025.ZIP',
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'timeout': 30,
    'colunas_csv': [
        'TIPREG', 'DATA', 'CODBDI', 'CODNEG', 'TPMERC', 'NOMRES', 'ESPECI',
        'PRAZOT', 'MODREF', 'PREABE', 'PREMAX', 'PREMIN', 'PREMED', 'PREULT',
        'PREOFC', 'PREOFV', 'TOTNEG', 'QUATOTNEG', 'VOLTOT', 'PREEXE', 'INDOPC',
        'DATVEN', 'FATCOT', 'PTOEXE', 'CODISI', 'DISMES'
    ]
}

# Configurações de Log
LOG_CONFIG = {
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'level': 'INFO'
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
    if ano_atual >= 2025:
        return B3_CONFIG['cotahist_url_2025']
    else:
        return B3_CONFIG['cotahist_url']
