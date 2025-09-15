# ====================================
# MODULO: COLETA DE DADOS DA B3
# ====================================

import pandas as pd
import requests
from io import BytesIO
from zipfile import ZipFile
import logging
from datetime import datetime
from config import B3_CONFIG, calcular_d1, get_cotahist_url

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class B3DataCollector:
    """Coletor de dados da B3"""
    
    def __init__(self):
        self.config = B3_CONFIG
        self.data_d1 = calcular_d1()
    
    def download_cotahist(self):
        """Download do arquivo COTAHIST da B3"""
        try:
            url = get_cotahist_url()
            logger.info(f"Iniciando download do COTAHIST de {url}")
            
            headers = {"User-Agent": self.config['user_agent']}
            
            response = requests.get(
                url, 
                headers=headers, 
                timeout=self.config.get('timeout', 30)
            )
            response.raise_for_status()
            
            logger.info(f"Download concluido. Tamanho: {len(response.content)} bytes")
            
            if len(response.content) == 0:
                logger.error("Arquivo baixado está vazio")
                return None
            
            zip_file = ZipFile(BytesIO(response.content))
            logger.info(f"Arquivo ZIP contem: {zip_file.namelist()}")
            
            return zip_file
            
        except requests.exceptions.Timeout:
            logger.error("Timeout no download do arquivo")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição HTTP: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro no download: {e}")
            return None
    
    def parse_csv_data(self, zip_file):
        """Processa o arquivo CSV do COTAHIST"""
        try:
            logger.info("Iniciando leitura do CSV...")
            
            # Tentar diferentes encodings
            encodings = ['latin1', 'utf-8', 'cp1252']
            df = None
            
            for encoding in encodings:
                try:
                    # Tentar com posições fixas (formato COTAHIST)
                    # Posições corretas do layout COTAHIST da B3
                    df = pd.read_fwf(
                        zip_file.open(zip_file.namelist()[0]),
                        colspecs=[
                            (0, 2),     # TIPREG
                            (2, 10),    # DATA
                            (10, 12),   # CODBDI
                            (12, 24),   # CODNEG
                            (24, 27),   # TPMERC
                            (27, 39),   # NOMRES
                            (39, 49),   # ESPECI
                            (49, 52),   # PRAZOT
                            (52, 56),   # MODREF
                            (56, 69),   # PREABE
                            (69, 82),   # PREMAX
                            (82, 95),   # PREMIN
                            (95, 108),  # PREMED
                            (108, 121), # PREULT
                            (121, 134), # PREOFC
                            (134, 147), # PREOFV
                            (147, 152), # TOTNEG
                            (152, 170), # QUATOTNEG
                            (170, 188), # VOLTOT
                            (188, 201), # PREEXE
                            (201, 202), # INDOPC
                            (202, 210), # DATVEN
                            (210, 217), # FATCOT
                            (217, 230), # PTOEXE
                            (230, 242), # CODISI
                            (242, 245)  # DISMES
                        ],
                        names=self.config['colunas_csv'],
                        encoding=encoding,
                        dtype=str  # Ler tudo como string primeiro
                    )
                    logger.info(f"CSV lido com encoding {encoding}. Linhas: {len(df)}")
                    break
                except Exception as e:
                    logger.warning(f"Falha com encoding {encoding}: {e}")
                    continue
            
            if df is None or df.empty:
                # Fallback: tentar como CSV delimitado
                df = pd.read_csv(
                    zip_file.open(zip_file.namelist()[0]),
                    sep=";",
                    encoding="latin1",
                    names=self.config['colunas_csv'],
                    header=None,
                    skiprows=1
                )
                logger.info(f"CSV lido como delimitado. Linhas: {len(df)}")
            
            return df
            
        except Exception as e:
            logger.error(f"Erro ao ler CSV: {e}")
            return pd.DataFrame()
    
    def filter_d1_data(self, df):
        """Filtra dados para D-1"""
        try:
            # Filtrar apenas registros de cotações (TIPREG = '01')
            # Isso remove cabeçalhos e rodapés automaticamente
            if 'TIPREG' in df.columns:
                df = df[df['TIPREG'] == '01'].copy()
                logger.info(f"Apos filtro TIPREG=01: {len(df)} registros")
            
            # Verificar se a coluna DATA tem valores válidos
            if df.empty:
                logger.warning("Nenhum registro válido encontrado")
                return pd.DataFrame()
            
            # Converter data - filtrar apenas valores numéricos válidos
            df = df[df['DATA'].astype(str).str.isdigit()].copy()
            logger.info(f"Apos filtro de datas validas: {len(df)} registros")
            
            if df.empty:
                logger.warning("Nenhuma data válida encontrada")
                return pd.DataFrame()
            
            # Converter para datetime
            df['DATA'] = pd.to_datetime(df['DATA'], format='%Y%m%d', errors='coerce')
            
            # Remover registros com datas inválidas
            df = df.dropna(subset=['DATA']).copy()
            
            # Filtrar D-1
            df_filtered = df[df['DATA'] == pd.to_datetime(self.data_d1)]
            
            logger.info(f"Apos filtro D-1: {len(df_filtered)} registros para {self.data_d1}")
            
            if len(df_filtered) == 0:
                logger.warning(f"Nenhum dado encontrado para {self.data_d1}")
                logger.info("Tentando usar a data mais recente disponível...")
                
                # Mostrar datas disponíveis para debug
                datas_disponiveis = df['DATA'].dt.date.unique()
                datas_ordenadas = sorted(datas_disponiveis)
                logger.info(f"Datas disponíveis no arquivo: {datas_ordenadas[-5:]}")  # Últimas 5 datas
                
                # Usar a data mais recente se D-1 não estiver disponível
                if len(datas_ordenadas) > 0:
                    data_mais_recente = datas_ordenadas[-1]
                    df_filtered = df[df['DATA'].dt.date == data_mais_recente]
                    logger.info(f"Usando data mais recente: {data_mais_recente} ({len(df_filtered)} registros)")
            
            return df_filtered
            
        except Exception as e:
            logger.error(f"Erro ao filtrar dados D-1: {e}")
            return pd.DataFrame()
    
    def transform_data(self, df):
        """Transforma e limpa os dados"""
        try:
            if df.empty:
                logger.warning("DataFrame vazio para transformação")
                return pd.DataFrame()
            
            # Renomear colunas
            df_transformed = df.rename(columns={
                'CODNEG': 'codigo',
                'NOMRES': 'nome',
                'PREABE': 'preco_abertura',
                'PREMAX': 'maximo',
                'PREMIN': 'minimo',
                'PREMED': 'preco_medio',
                'PREULT': 'preco_fechamento',
                'QUATOTNEG': 'negocios',
                'VOLTOT': 'volume_financeiro',
                'DATA': 'data'
            })
            
            # Limpar e converter tipos
            df_transformed['codigo'] = df_transformed['codigo'].astype(str).str.strip()
            df_transformed['nome'] = df_transformed['nome'].astype(str).str.strip()
            
            # Converter preços (dividir por 100 se necessário)
            price_columns = ['preco_abertura', 'maximo', 'minimo', 'preco_medio', 'preco_fechamento']
            for col in price_columns:
                if col in df_transformed.columns:
                    df_transformed[col] = pd.to_numeric(df_transformed[col], errors='coerce') / 100
            
            # Converter volumes e quantidades
            if 'volume_financeiro' in df_transformed.columns:
                df_transformed['volume_financeiro'] = pd.to_numeric(df_transformed['volume_financeiro'], errors='coerce') / 100
            
            if 'negocios' in df_transformed.columns:
                df_transformed['negocios'] = pd.to_numeric(df_transformed['negocios'], errors='coerce')
            
            # O filtro TIPREG já foi aplicado na função filter_d1_data
            # Remover registros com preços zerados ou inválidos
            df_transformed = df_transformed[
                (df_transformed['preco_fechamento'] > 0) | 
                (df_transformed['preco_abertura'] > 0)
            ]
            
            logger.info(f"Dados transformados com sucesso. {len(df_transformed)} registros válidos")
            return df_transformed
            
        except Exception as e:
            logger.error(f"Erro na transformacao: {e}")
            return pd.DataFrame()
    
    def classify_asset(self, codigo, nome):
        """Classifica o ativo por tipo e setor baseado no código"""
        try:
            # Determinar TIPO
            if codigo.endswith('11'):
                tipo = 'FII'
                # Setores de FIIs
                nome_upper = nome.upper()
                if any(word in nome_upper for word in ['SHOPPING', 'MALL', 'VAREJO']):
                    setor = 'Shoppings'
                elif any(word in nome_upper for word in ['LOGISTICO', 'LOGÍSTICA', 'GALPAO', 'GALPÃO']):
                    setor = 'Logística'
                elif any(word in nome_upper for word in ['CORPORATIVO', 'LAJES', 'ESCRITORIO', 'ESCRITÓRIO']):
                    setor = 'Corporativo'
                elif any(word in nome_upper for word in ['RESIDENCIAL', 'HABITACIONAL']):
                    setor = 'Residencial'
                elif any(word in nome_upper for word in ['HOSPITAL', 'SAUDE', 'SAÚDE', 'CLINICA', 'CLÍNICA']):
                    setor = 'Saúde'
                elif any(word in nome_upper for word in ['HOTEL', 'HOTELARIA']):
                    setor = 'Hotelaria'
                elif any(word in nome_upper for word in ['AGRO', 'AGRICOLA', 'AGRÍCOLA']):
                    setor = 'Agronegócio'
                elif any(word in nome_upper for word in ['PAPEL', 'CRI', 'CREDITO', 'CRÉDITO']):
                    setor = 'Papel e Renda'
                else:
                    setor = 'Outros'
            elif codigo.endswith(('39', '35')):
                tipo = 'BDR'
                setor = 'Internacional'
            elif 'ETF' in nome.upper() or any(codigo.startswith(prefix) for prefix in ['BOVA', 'SMAL', 'IVVB']):
                tipo = 'ETF'
                setor = 'Índices'
            else:
                tipo = 'ACAO'
                # Setores de Ações baseado no nome
                nome_upper = nome.upper()
                if any(word in nome_upper for word in ['PETRO', 'OLEO', 'GAS', 'COMBUSTIVEL']):
                    setor = 'Petróleo e Gás'
                elif any(word in nome_upper for word in ['BANCO', 'BRADESCO', 'ITAU', 'SANTANDER', 'FINANC']):
                    setor = 'Bancos'
                elif any(word in nome_upper for word in ['VALE', 'MINERA', 'SIDERUR', 'METAL', 'ACO', 'AÇO']):
                    setor = 'Mineração e Siderurgia'
                elif any(word in nome_upper for word in ['ELETRIC', 'ENERGIA', 'ENERG', 'CEMIG', 'COPEL']):
                    setor = 'Energia Elétrica'
                elif any(word in nome_upper for word in ['TELEFON', 'TELECOM', 'TIM', 'VIVO', 'OI']):
                    setor = 'Telecomunicações'
                elif any(word in nome_upper for word in ['CONSTRUC', 'CIVIL', 'MRV', 'CYRELA', 'GAFISA']):
                    setor = 'Construção Civil'
                elif any(word in nome_upper for word in ['VAREJO', 'MAGALU', 'VIA', 'AMERICANAS', 'LOJAS']):
                    setor = 'Varejo'
                elif any(word in nome_upper for word in ['ALIMENT', 'BEBIDA', 'BRF', 'AMBEV', 'JBS']):
                    setor = 'Alimentos e Bebidas'
                elif any(word in nome_upper for word in ['SAUDE', 'HOSPITAL', 'MEDIC', 'QUALICORP']):
                    setor = 'Saúde'
                elif any(word in nome_upper for word in ['PAPEL', 'CELULOSE', 'SUZANO', 'KLABIN']):
                    setor = 'Papel e Celulose'
                elif any(word in nome_upper for word in ['SEGUR', 'PORTO', 'SUL AMERICA']):
                    setor = 'Seguros'
                elif any(word in nome_upper for word in ['TRANSPORT', 'LOGISTIC', 'RUMO', 'AZUL']):
                    setor = 'Transporte'
                else:
                    setor = 'Outros'
            
            return tipo, setor
            
        except Exception as e:
            logger.warning(f"Erro ao classificar ativo {codigo}: {e}")
            return 'ACAO', 'Outros'
    
    def extract_ativos(self, df):
        """Extrai lista unica de ativos com tipo e setor"""
        try:
            # Extrair ativos únicos
            df_ativos = df[['codigo', 'nome']].drop_duplicates()
            
            # Adicionar tipo e setor
            df_ativos['tipo'] = ''
            df_ativos['setor'] = ''
            
            for idx, row in df_ativos.iterrows():
                tipo, setor = self.classify_asset(row['codigo'], row['nome'])
                df_ativos.at[idx, 'tipo'] = tipo
                df_ativos.at[idx, 'setor'] = setor
            
            logger.info(f"Extraidos {len(df_ativos)} ativos unicos com classificacao")
            
            # Log estatísticas
            if not df_ativos.empty:
                logger.info("Distribuição por tipo:")
                for tipo, count in df_ativos['tipo'].value_counts().items():
                    logger.info(f"  {tipo}: {count}")
            
            return df_ativos
        except Exception as e:
            logger.error(f"Erro ao extrair ativos: {e}")
            return pd.DataFrame()
    
    def prepare_cotacoes(self, df, ativos_db):
        """Prepara dados de cotacoes para insercao"""
        try:
            # Garantir tipos consistentes
            df['codigo'] = df['codigo'].astype(str)
            ativos_db['codigo'] = ativos_db['codigo'].astype(str)
            
            # Fazer merge com ativos do banco
            df_merged = df.merge(ativos_db, how='left', on='codigo')
            
            # Selecionar colunas para cotacoes
            df_cotacoes = df_merged[
                ['id', 'data', 'preco_abertura', 'preco_fechamento',
                 'maximo', 'minimo', 'negocios', 'volume_financeiro']
            ].rename(columns={'id': 'id_ativo'})
            
            # Limpar dados invalidos
            df_cotacoes = df_cotacoes.dropna(subset=['id_ativo', 'data'])
            df_cotacoes = df_cotacoes.dropna(
                subset=['preco_abertura', 'preco_fechamento', 'maximo', 'minimo'],
                how='all'
            )
            
            logger.info(f"Preparadas {len(df_cotacoes)} cotacoes validas")
            return df_cotacoes
            
        except Exception as e:
            logger.error(f"Erro ao preparar cotacoes: {e}")
            return pd.DataFrame()
    
    def collect_dividends_data(self):
        """Coleta dados de dividendos de FIIs da B3"""
        try:
            logger.info("Coletando dados de dividendos...")
            
            # Simular coleta de dividendos (em produção, viria de API específica)
            # Por enquanto, vamos gerar alguns dados de exemplo baseados nos FIIs
            dividendos_exemplo = [
                {'codigo': 'HGLG11', 'data': '2024-01-15', 'valor': 0.85, 'tipo': 'Rendimento'},
                {'codigo': 'XPML11', 'data': '2024-01-20', 'valor': 0.92, 'tipo': 'Rendimento'},
                {'codigo': 'BTLG11', 'data': '2024-01-25', 'valor': 0.78, 'tipo': 'Rendimento'},
                {'codigo': 'VISC11', 'data': '2024-02-15', 'valor': 0.88, 'tipo': 'Rendimento'},
                {'codigo': 'HGLG11', 'data': '2024-02-15', 'valor': 0.87, 'tipo': 'Rendimento'},
                {'codigo': 'PETR4', 'data': '2024-03-15', 'valor': 1.25, 'tipo': 'Dividendo'},
                {'codigo': 'VALE3', 'data': '2024-03-20', 'valor': 2.15, 'tipo': 'Dividendo'},
                {'codigo': 'ITUB4', 'data': '2024-03-25', 'valor': 0.45, 'tipo': 'JCP'},
            ]
            
            df_dividendos = pd.DataFrame(dividendos_exemplo)
            df_dividendos['data'] = pd.to_datetime(df_dividendos['data'])
            
            logger.info(f"Coletados {len(df_dividendos)} registros de dividendos")
            return df_dividendos
            
        except Exception as e:
            logger.error(f"Erro ao coletar dividendos: {e}")
            return pd.DataFrame()

    def collect_and_process_data(self):
        """Metodo principal para coleta e processamento"""
        try:
            logger.info(f"Iniciando coleta para D-1: {self.data_d1}")
            
            # 1. Download
            zip_file = self.download_cotahist()
            if zip_file is None:
                return None, None, None
            
            # 2. Parse CSV
            df_raw = self.parse_csv_data(zip_file)
            if df_raw.empty:
                return None, None, None
            
            # 3. Filtrar D-1
            df_filtered = self.filter_d1_data(df_raw)
            if df_filtered.empty:
                return None, None, None
            
            # 4. Transformar
            df_transformed = self.transform_data(df_filtered)
            if df_transformed.empty:
                return None, None, None
            
            # 5. Extrair ativos
            df_ativos = self.extract_ativos(df_transformed)
            
            # 6. Coletar dividendos
            df_dividendos = self.collect_dividends_data()
            
            return df_transformed, df_ativos, df_dividendos
            
        except Exception as e:
            logger.error(f"Erro no processo de coleta: {e}")
            return None, None, None
