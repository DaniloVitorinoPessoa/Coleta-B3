# ====================================
# MODULO: VISUALIZACOES E GRAFICOS
# ====================================

import pandas as pd
import logging
from database_manager import DatabaseManager

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VisualizationManager:
    """Gerenciador de visualizacoes e graficos"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def create_candlestick_chart(self, codigo_ativo, periodo_dias=30):
        """Cria grafico de candlestick para um ativo"""
        try:
            # Importar plotly apenas quando necessario
            import plotly.graph_objects as go
            from plotly.subplots import make_subplots
            
            query = """
                SELECT c.data, c.preco_abertura, c.preco_fechamento, 
                       c.maximo, c.minimo, c.volume_financeiro, a.nome
                FROM cotacoes c
                JOIN ativos a ON c.id_ativo = a.id
                WHERE a.codigo = %s
                AND c.data >= CURRENT_DATE - INTERVAL '%s days'
                ORDER BY c.data
            """
            
            df = self.db.execute_query(query, [codigo_ativo, periodo_dias])
            
            if df.empty:
                logger.warning(f"Nenhum dado encontrado para {codigo_ativo}")
                return None
            
            # Criar subplots
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=(f'Cotacoes - {codigo_ativo}', 'Volume Financeiro'),
                vertical_spacing=0.1,
                row_heights=[0.7, 0.3]
            )
            
            # Grafico de candlestick
            fig.add_trace(
                go.Candlestick(
                    x=df['data'],
                    open=df['preco_abertura'],
                    high=df['maximo'],
                    low=df['minimo'],
                    close=df['preco_fechamento'],
                    name='Cotacoes'
                ),
                row=1, col=1
            )
            
            # Grafico de volume
            fig.add_trace(
                go.Bar(
                    x=df['data'],
                    y=df['volume_financeiro'],
                    name='Volume',
                    marker_color='lightblue'
                ),
                row=2, col=1
            )
            
            fig.update_layout(
                title=f'Analise de {codigo_ativo} - {df["nome"].iloc[0]}',
                xaxis_rangeslider_visible=False,
                height=600
            )
            
            # Salvar grafico
            filename = f'historico_{codigo_ativo}.html'
            fig.write_html(filename)
            logger.info(f"Grafico salvo como '{filename}'")
            
            return fig
            
        except ImportError:
            logger.warning("Plotly nao instalado. Instale com: pip install plotly")
            return None
        except Exception as e:
            logger.error(f"Erro ao criar grafico de candlestick: {e}")
            return None
    
    def create_portfolio_charts(self):
        """Cria graficos de alocacao da carteira"""
        try:
            import plotly.express as px
            
            query = """
                SELECT 
                    a.codigo, a.nome, a.tipo, a.setor,
                    c.qtd, c.preco_medio,
                    c.qtd * c.preco_medio as valor_investido,
                    cot.preco_fechamento as preco_atual,
                    c.qtd * cot.preco_fechamento as valor_atual
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
                logger.warning("Carteira vazia")
                return None
            
            # Grafico por setor
            if df['setor'].notna().any():
                alocacao_setor = df.groupby('setor')['valor_atual'].sum().reset_index()
                
                fig1 = px.pie(
                    alocacao_setor, 
                    values='valor_atual', 
                    names='setor',
                    title='Alocacao por Setor'
                )
                fig1.write_html('alocacao_setor.html')
                logger.info("Grafico 'alocacao_setor.html' criado")
            
            # Grafico por tipo
            if df['tipo'].notna().any():
                alocacao_tipo = df.groupby('tipo')['valor_atual'].sum().reset_index()
                
                fig2 = px.pie(
                    alocacao_tipo, 
                    values='valor_atual', 
                    names='tipo',
                    title='Alocacao por Tipo'
                )
                fig2.write_html('alocacao_tipo.html')
                logger.info("Grafico 'alocacao_tipo.html' criado")
            
            # Grafico de rentabilidade
            df['rentabilidade_pct'] = ((df['preco_atual'] - df['preco_medio']) / df['preco_medio']) * 100
            df_rent = df.nlargest(10, 'rentabilidade_pct')
            
            if not df_rent.empty:
                fig3 = px.bar(
                    df_rent, 
                    x='codigo', 
                    y='rentabilidade_pct',
                    title='Top 10 - Rentabilidade por Ativo',
                    color='rentabilidade_pct',
                    color_continuous_scale='RdYlGn'
                )
                fig3.write_html('rentabilidade_ativos.html')
                logger.info("Grafico 'rentabilidade_ativos.html' criado")
            
            return True
            
        except ImportError:
            logger.warning("Plotly nao instalado. Instale com: pip install plotly")
            return False
        except Exception as e:
            logger.error(f"Erro ao criar graficos da carteira: {e}")
            return False
    
    def create_dividends_chart(self, codigo_ativo=None, ano=None):
        """Cria grafico de dividendos"""
        try:
            import plotly.express as px
            
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
            
            query += " ORDER BY d.data"
            
            df = self.db.execute_query(query, params)
            
            if df.empty:
                logger.warning("Nenhum dividendo encontrado")
                return None
            
            # Grafico mensal
            df_mensal = df.groupby(['ano', 'mes'])['valor'].sum().reset_index()
            df_mensal['periodo'] = df_mensal['ano'].astype(str) + '-' + df_mensal['mes'].astype(str).str.zfill(2)
            
            fig = px.bar(
                df_mensal, 
                x='periodo', 
                y='valor',
                title='Dividendos por Mes',
                labels={'valor': 'Valor (R$)', 'periodo': 'Periodo'}
            )
            
            filename = 'dividendos_mensal.html'
            fig.write_html(filename)
            logger.info(f"Grafico salvo como '{filename}'")
            
            return fig
            
        except ImportError:
            logger.warning("Plotly nao instalado. Instale com: pip install plotly")
            return None
        except Exception as e:
            logger.error(f"Erro ao criar grafico de dividendos: {e}")
            return None
