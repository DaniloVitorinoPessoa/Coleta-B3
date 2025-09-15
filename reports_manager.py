# ====================================
# MODULO: RELATORIOS E CONSULTAS
# ====================================

import pandas as pd
import logging
from database_manager import DatabaseManager

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReportsManager:
    """Gerenciador de relatorios e consultas"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def consultar_ativos(self, filtro_tipo=None, filtro_setor=None):
        """Consulta lista de ativos com filtros opcionais"""
        try:
            query = "SELECT codigo, nome, tipo, setor FROM ativos WHERE 1=1"
            params = []
            
            if filtro_tipo:
                query += " AND tipo = %s"
                params.append(filtro_tipo)
            
            if filtro_setor:
                query += " AND setor = %s"
                params.append(filtro_setor)
            
            query += " ORDER BY codigo"
            
            df = self.db.execute_query(query, tuple(params) if params else None)
            
            if not df.empty:
                print(f"\nLISTA DE ATIVOS ({len(df)} encontrados)")
                print("=" * 60)
                print(df.to_string(index=False))
                
                # Estatisticas
                print(f"\nESTATISTICAS:")
                print(f"Total de ativos: {len(df)}")
                
                if 'tipo' in df.columns and df['tipo'].notna().any():
                    print("Por tipo:")
                    print(df['tipo'].value_counts().to_string())
                
                if 'setor' in df.columns and df['setor'].notna().any():
                    print("\nPor setor:")
                    print(df['setor'].value_counts().to_string())
            else:
                print("Nenhum ativo encontrado com os filtros especificados")
            
            return df
            
        except Exception as e:
            logger.error(f"Erro ao consultar ativos: {e}")
            return pd.DataFrame()
    
    def historico_cotacoes(self, codigo_ativo, periodo_dias=30):
        """Gera relatorio de historico de cotacoes"""
        try:
            query = """
                SELECT c.data, c.preco_abertura, c.preco_fechamento, 
                       c.maximo, c.minimo, c.volume_financeiro, a.nome
                FROM cotacoes c
                JOIN ativos a ON c.id_ativo = a.id
                WHERE a.codigo = %s
                AND c.data >= CURRENT_DATE - INTERVAL '%s days'
                ORDER BY c.data
            """
            
            df = self.db.execute_query(query, (codigo_ativo, periodo_dias))
            
            if df.empty:
                print(f"ERRO: Nenhum dado encontrado para {codigo_ativo}")
                return None
            
            print(f"\nHISTORICO DE COTACOES - {codigo_ativo}")
            print(f"Periodo: {periodo_dias} dias | Registros: {len(df)}")
            print("=" * 60)
            
            # Estatisticas basicas
            ultimo_preco = df['preco_fechamento'].iloc[-1]
            primeiro_preco = df['preco_fechamento'].iloc[0]
            variacao = ((ultimo_preco - primeiro_preco) / primeiro_preco) * 100
            
            print(f"\nESTATISTICAS DO PERIODO:")
            print(f"Preco inicial: R$ {primeiro_preco:.2f}")
            print(f"Preco final: R$ {ultimo_preco:.2f}")
            print(f"Variacao: {variacao:+.2f}%")
            print(f"Maior alta: R$ {df['maximo'].max():.2f}")
            print(f"Menor baixa: R$ {df['minimo'].min():.2f}")
            
            return df
            
        except Exception as e:
            logger.error(f"Erro ao gerar historico de cotacoes: {e}")
            return None
    
    def relatorio_dividendos(self, codigo_ativo=None, ano=None):
        """Gera relatorio de dividendos/proventos"""
        try:
            query = """
                SELECT a.codigo, a.nome, d.data, d.valor, d.tipo,
                       EXTRACT(YEAR FROM d.data) as ano,
                       EXTRACT(MONTH FROM d.data) as mes
                FROM dividendos d
                JOIN ativos a ON d.id_ativo = a.id
                WHERE 1=1
            """
            params = []
            
            if codigo_ativo:
                query += " AND a.codigo = %s"
                params.append(codigo_ativo)
            
            if ano:
                query += " AND EXTRACT(YEAR FROM d.data) = %s"
                params.append(ano)
            
            query += " ORDER BY d.data DESC"
            
            df = self.db.execute_query(query, tuple(params) if params else None)
            
            if df.empty:
                print("ERRO: Nenhum dividendo encontrado")
                return None
            
            print(f"\nRELATORIO DE DIVIDENDOS")
            if codigo_ativo:
                print(f"Ativo: {codigo_ativo}")
            if ano:
                print(f"Ano: {ano}")
            print("=" * 60)
            
            # Resumo por ativo
            resumo = df.groupby(['codigo', 'nome']).agg({
                'valor': ['sum', 'count', 'mean'],
                'data': ['min', 'max']
            }).round(2)
            
            print("RESUMO POR ATIVO:")
            print(resumo)
            
            return df
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatorio de dividendos: {e}")
            return None
    
    def dashboard_alocacao(self):
        """Dashboard completo de alocacao da carteira"""
        try:
            query = """
                SELECT 
                    a.codigo, a.nome, a.tipo, a.setor,
                    c.qtd, c.preco_medio,
                    c.qtd * c.preco_medio as valor_investido,
                    cot.preco_fechamento as preco_atual,
                    c.qtd * cot.preco_fechamento as valor_atual,
                    (c.qtd * cot.preco_fechamento) - (c.qtd * c.preco_medio) as ganho_perda,
                    ((cot.preco_fechamento - c.preco_medio) / c.preco_medio) * 100 as rentabilidade_pct
                FROM carteira c
                JOIN ativos a ON c.id_ativo = a.id
                LEFT JOIN (
                    SELECT DISTINCT ON (id_ativo) id_ativo, preco_fechamento
                    FROM cotacoes
                    ORDER BY id_ativo, data DESC
                ) cot ON c.id_ativo = cot.id_ativo
            """
            
            df = self.db.execute_query(query)
            
            if df.empty:
                print("ERRO: Carteira vazia")
                return None
            
            print(f"\nDASHBOARD DE ALOCACAO DA CARTEIRA")
            print("=" * 80)
            
            # Calculos gerais
            valor_total_investido = df['valor_investido'].sum()
            valor_total_atual = df['valor_atual'].sum()
            ganho_perda_total = valor_total_atual - valor_total_investido
            rentabilidade_total = (ganho_perda_total / valor_total_investido) * 100
            
            print(f"RESUMO GERAL:")
            print(f"Valor investido: R$ {valor_total_investido:,.2f}")
            print(f"Valor atual: R$ {valor_total_atual:,.2f}")
            print(f"Ganho/Perda: R$ {ganho_perda_total:+,.2f}")
            print(f"Rentabilidade: {rentabilidade_total:+.2f}%")
            
            # Alocacao por setor
            if df['setor'].notna().any():
                df['percentual_setor'] = (df['valor_atual'] / valor_total_atual) * 100
                alocacao_setor = df.groupby('setor').agg({
                    'valor_atual': 'sum',
                    'percentual_setor': 'sum'
                }).sort_values('valor_atual', ascending=False)
                
                print(f"\nALOCACAO POR SETOR:")
                for setor, row in alocacao_setor.iterrows():
                    print(f"{setor:20s}: {row['percentual_setor']:6.1f}% (R$ {row['valor_atual']:,.2f})")
            
            # Alocacao por tipo
            if df['tipo'].notna().any():
                alocacao_tipo = df.groupby('tipo').agg({
                    'valor_atual': 'sum'
                })
                alocacao_tipo['percentual'] = (alocacao_tipo['valor_atual'] / valor_total_atual) * 100
                
                print(f"\nALOCACAO POR TIPO:")
                for tipo, row in alocacao_tipo.iterrows():
                    print(f"{tipo:15s}: {row['percentual']:6.1f}% (R$ {row['valor_atual']:,.2f})")
            
            return df
            
        except Exception as e:
            logger.error(f"Erro ao gerar dashboard de alocacao: {e}")
            return None
    
    def resumo_sistema(self):
        """Gera resumo do sistema"""
        try:
            print("\nRESUMO DO SISTEMA")
            print("=" * 50)
            
            # Contar registros por tabela
            tabelas = ['ativos', 'cotacoes', 'dividendos']
            
            for tabela in tabelas:
                count = self.db.get_table_count(tabela)
                print(f"{tabela:12s}: {count:6d} registros")
            
            # Data mais recente de cotacoes
            try:
                query = "SELECT MAX(data) as ultima_data FROM cotacoes"
                result = self.db.execute_query(query)
                if not result.empty and result['ultima_data'].iloc[0] is not None:
                    ultima_data = result['ultima_data'].iloc[0]
                    print(f"\nUltima cotacao: {ultima_data}")
            except:
                print("\nUltima cotacao: Nao disponivel")
            
        except Exception as e:
            logger.error(f"Erro ao gerar resumo do sistema: {e}")
