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
            from datetime import datetime, timedelta

            logger.info(f"Iniciando criação de gráfico candlestick para {codigo_ativo}")
            logger.info(f"Período solicitado: {periodo_dias} dias")

            data_limite = datetime.now().date() - timedelta(days=periodo_dias)
            logger.info(f"Data limite calculada: {data_limite}")
            logger.info(f"Data atual: {datetime.now().date()}")

            query = """
                SELECT c.data, c.preco_abertura, c.preco_fechamento, 
                       c.maximo, c.minimo, c.volume_financeiro, a.nome
                FROM cotacoes c
                JOIN ativos a ON c.id_ativo = a.id
                WHERE a.codigo = %s
                AND c.data >= %s
                ORDER BY c.data
            """

            df = self.db.execute_query(query, [codigo_ativo, data_limite])

            logger.info(f"Query executada - Data limite: {data_limite}")
            logger.info(f"Dados retornados: {len(df)} registros")

            if not df.empty:
                logger.info(f"Primeira data: {df['data'].min()}")
                logger.info(f"Última data: {df['data'].max()}")
                logger.info(
                    f"Período real dos dados: {(df['data'].max() - df['data'].min()).days} dias"
                )

            if df.empty:
                logger.warning(f"Nenhum dado encontrado para {codigo_ativo}")

                # Tentar buscar qualquer dado disponível para este ativo
                logger.info("Tentando buscar dados sem filtro de data...")
                query_any = """
                    SELECT c.data, c.preco_abertura, c.preco_fechamento, 
                           c.maximo, c.minimo, c.volume_financeiro, a.nome
                    FROM cotacoes c
                    JOIN ativos a ON c.id_ativo = a.id
                    WHERE a.codigo = %s
                    ORDER BY c.data DESC
                    LIMIT 100
                """
                df_any = self.db.execute_query(query_any, [codigo_ativo])

                if not df_any.empty:
                    logger.warning(
                        f"Encontrados {len(df_any)} registros sem filtro de data"
                    )
                    logger.info(f"Data mais recente disponível: {df_any['data'].max()}")
                    logger.info(f"Data mais antiga disponível: {df_any['data'].min()}")

                    # Usar apenas os registros solicitados, respeitando o período
                    num_registros = min(len(df_any), periodo_dias)
                    df = df_any.head(num_registros)
                    logger.info(
                        f"Usando os {len(df)} registros mais recentes (respeitando período de {periodo_dias} dias)"
                    )
                else:
                    logger.error(
                        "Nenhum dado encontrado para este ativo em qualquer período"
                    )
                    return None

            logger.info(f"Dados obtidos para gráfico: {len(df)} registros")

            # Garantir que as datas são objetos datetime
            if isinstance(df["data"].iloc[0], str):
                df["data"] = pd.to_datetime(df["data"])

            # Calcular linhas de suporte e resistência
            precos_fechamento = df["preco_fechamento"].dropna()
            precos_maximos = df["maximo"].dropna()
            precos_minimos = df["minimo"].dropna()

            # Suporte: média dos 3 menores mínimos
            suporte = precos_minimos.nsmallest(3).mean()
            # Resistência: média dos 3 maiores máximos
            resistencia = precos_maximos.nlargest(3).mean()

            logger.info(f"Suporte calculado: R$ {suporte:.2f}")
            logger.info(f"Resistência calculada: R$ {resistencia:.2f}")

            # Criar subplots profissionais - Candlestick + Volume
            fig = make_subplots(
                rows=2,
                cols=1,
                shared_xaxes=True,
                vertical_spacing=0.05,
                subplot_titles=("", ""),  # Sem títulos automáticos
                row_heights=[0.75, 0.25],
                specs=[[{"secondary_y": False}], [{"secondary_y": False}]],
            )

            # Grafico de candlestick principal com cores profissionais
            fig.add_trace(
                go.Candlestick(
                    x=df["data"],
                    open=df["preco_abertura"],
                    high=df["maximo"],
                    low=df["minimo"],
                    close=df["preco_fechamento"],
                    name=codigo_ativo,
                    increasing_line_color="#26a69a",  # Verde TradingView
                    decreasing_line_color="#ef5350",  # Vermelho TradingView
                    increasing_fillcolor="#26a69a",
                    decreasing_fillcolor="#ef5350",
                    line=dict(width=1),
                    whiskerwidth=0.8,
                ),
                row=1,
                col=1,
            )

            # Linha de Suporte
            fig.add_hline(
                y=suporte,
                line_dash="dash",
                line_color="#2196F3",
                line_width=1.5,
                annotation_text=f"Suporte: R$ {suporte:.2f}",
                annotation_position="left",
                annotation_font_size=10,
                annotation_font_color="#2196F3",
                row=1,
            )

            # Linha de Resistência
            fig.add_hline(
                y=resistencia,
                line_dash="dash",
                line_color="#FF9800",
                line_width=1.5,
                annotation_text=f"Resistência: R$ {resistencia:.2f}",
                annotation_position="left",
                annotation_font_size=10,
                annotation_font_color="#FF9800",
                row=1,
            )

            # Volume com cores baseadas na direção do preço
            colors_volume = []
            for i in range(len(df)):
                if df.iloc[i]["preco_fechamento"] >= df.iloc[i]["preco_abertura"]:
                    colors_volume.append("#26a69a")  # Verde para alta
                else:
                    colors_volume.append("#ef5350")  # Vermelho para baixa

            fig.add_trace(
                go.Bar(
                    x=df["data"],
                    y=df["volume_financeiro"],
                    name="Volume",
                    marker_color=colors_volume,
                    opacity=0.7,
                    showlegend=False,
                ),
                row=2,
                col=1,
            )

            # Calcular estatísticas para o título
            preco_inicial = df["preco_fechamento"].iloc[0] if len(df) > 0 else 0
            preco_final = df["preco_fechamento"].iloc[-1] if len(df) > 0 else 0
            preco_max = df["maximo"].max() if len(df) > 0 else 0
            preco_min = df["minimo"].min() if len(df) > 0 else 0
            variacao_pct = (
                ((preco_final - preco_inicial) / preco_inicial * 100)
                if preco_inicial > 0
                else 0
            )

            # Calcular período real dos dados
            if len(df) > 1:
                data_inicial = df["data"].min()
                data_final = df["data"].max()
                periodo_real = (data_final - data_inicial).days
                data_info = f"{data_inicial.strftime('%d/%m/%Y')} - {data_final.strftime('%d/%m/%Y')}"
                periodo_info = (
                    f"{periodo_dias} dias solicitados | {periodo_real} dias reais"
                )
            else:
                data_info = f"{df['data'].iloc[0].strftime('%d/%m/%Y')}"
                periodo_info = f"{periodo_dias} dias solicitados"

            # Layout profissional estilo TradingView
            fig.update_layout(
                title={
                    "text": f'<b>{codigo_ativo}</b> - {df["nome"].iloc[0]}<br>'
                    f'<span style="font-size:14px; color:#37474f">{data_info}</span><br>'
                    f'<span style="font-size:12px; color:#666">Último: R$ {preco_final:.2f} '
                    f"({variacao_pct:+.2f}%) | Máx: R$ {preco_max:.2f} | Mín: R$ {preco_min:.2f}</span>",
                    "x": 0.02,
                    "xanchor": "left",
                    "y": 0.98,
                    "yanchor": "top",
                    "font": {"size": 18, "family": "Arial, sans-serif"},
                },
                # Fundo e estilo
                plot_bgcolor="white",
                paper_bgcolor="white",
                # Dimensões
                height=700,
                width=1200,
                # Margens
                margin=dict(l=80, r=80, t=120, b=60),
                # Sem legenda para candlestick
                showlegend=False,
                # Hover
                hovermode="x unified",
                # Fonte global
                font=dict(family="Arial, sans-serif", size=11, color="#37474f"),
            )

            # Configurar eixo X (tempo) - painel superior
            fig.update_xaxes(
                showgrid=True,
                gridwidth=1,
                gridcolor="rgba(128,128,128,0.2)",
                showline=True,
                linewidth=1.5,
                linecolor="#e0e0e0",
                tickfont=dict(size=10, color="#666"),
                showticklabels=False,  # Ocultar labels no painel superior
                row=1,
                col=1,
            )

            # Configurar eixo Y (preço) - painel superior
            fig.update_yaxes(
                title_text="Preço (R$)",
                title_font=dict(size=12, color="#37474f"),
                showgrid=True,
                gridwidth=1,
                gridcolor="rgba(128,128,128,0.2)",
                showline=True,
                linewidth=1.5,
                linecolor="#e0e0e0",
                tickfont=dict(size=10, color="#666"),
                side="right",
                tickformat=".2f",
                row=1,
                col=1,
            )

            # Configurar eixo X (tempo) - painel volume
            fig.update_xaxes(
                title_text="Data",
                title_font=dict(size=12, color="#37474f"),
                showgrid=True,
                gridwidth=1,
                gridcolor="rgba(128,128,128,0.2)",
                showline=True,
                linewidth=1.5,
                linecolor="#e0e0e0",
                tickfont=dict(size=10, color="#666"),
                row=2,
                col=1,
            )

            # Configurar eixo Y (volume) - painel volume
            fig.update_yaxes(
                title_text="Volume Financeiro",
                title_font=dict(size=12, color="#37474f"),
                showgrid=True,
                gridwidth=1,
                gridcolor="rgba(128,128,128,0.2)",
                showline=True,
                linewidth=1.5,
                linecolor="#e0e0e0",
                tickfont=dict(size=10, color="#666"),
                side="right",
                tickformat=".0s",  # Formato científico para volume
                row=2,
                col=1,
            )

            # Adicionar anotação com estatísticas no canto
            fig.add_annotation(
                text=f"Período: {periodo_info}<br>"
                f"Registros: {len(df)}<br>"
                f"Suporte: R$ {suporte:.2f}<br>"
                f"Resistência: R$ {resistencia:.2f}",
                xref="paper",
                yref="paper",
                x=0.02,
                y=0.02,
                showarrow=False,
                font=dict(size=9, color="#666"),
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="#ddd",
                borderwidth=1,
                align="left",
            )

            # Salvar grafico
            import os

            filename = f"historico_{codigo_ativo}.html"
            full_path = os.path.abspath(filename)
            fig.write_html(filename)
            logger.info(f"Grafico salvo como '{filename}'")
            logger.info(f"Caminho completo: {full_path}")

            # Tentar abrir no navegador
            try:
                import webbrowser

                webbrowser.open(f"file://{full_path}")
                logger.info("Gráfico aberto no navegador")
            except Exception as browser_error:
                logger.warning(
                    f"Não foi possível abrir automaticamente: {browser_error}"
                )
                logger.info(f"Abra manualmente o arquivo: {full_path}")

            return fig

        except ImportError as e:
            logger.error(f"Plotly não instalado: {e}")
            logger.warning("Instale com: pip install plotly")
            return None
        except Exception as e:
            logger.error(f"Erro ao criar grafico de candlestick: {e}")
            import traceback

            logger.error(f"Traceback: {traceback.format_exc()}")
            return None

    def create_dividends_chart(self, codigo_ativo=None, ano=None, trimestre=None):
        """Cria grafico de dividendos"""
        try:
            logger.info(f"Iniciando criacao de grafico de dividendos")
            logger.info(
                f"Parametros: codigo={codigo_ativo}, ano={ano}, trimestre={trimestre}"
            )

            import plotly.express as px
            import os
            import webbrowser

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

            if trimestre:
                if trimestre == 1:
                    query += " AND EXTRACT(MONTH FROM d.data) BETWEEN 1 AND 3"
                elif trimestre == 2:
                    query += " AND EXTRACT(MONTH FROM d.data) BETWEEN 4 AND 6"
                elif trimestre == 3:
                    query += " AND EXTRACT(MONTH FROM d.data) BETWEEN 7 AND 9"
                elif trimestre == 4:
                    query += " AND EXTRACT(MONTH FROM d.data) BETWEEN 10 AND 12"

            query += " ORDER BY d.data"

            logger.info(f"Executando query de dividendos...")
            df = self.db.execute_query(query, params if params else None)
            logger.info(f"Query executada. Registros encontrados: {len(df)}")

            if df.empty:
                logger.warning(
                    "Nenhum dividendo encontrado para os filtros especificados"
                )
                print(
                    "AVISO: Nenhum dividendo encontrado para os filtros especificados"
                )
                print(
                    "SUGESTAO: Verifique se ha dados de dividendos no banco ou tente sem filtros"
                )
                return None

            logger.info(f"Dados de dividendos obtidos: {len(df)} registros")
            logger.info(f"Primeiras datas: {df['data'].head().tolist()}")
            logger.info(f"Primeiros valores: {df['valor'].head().tolist()}")

            # Grafico mensal
            df_mensal = df.groupby(["ano", "mes"])["valor"].sum().reset_index()
            df_mensal["periodo"] = (
                df_mensal["ano"].astype(str)
                + "-"
                + df_mensal["mes"].astype(str).str.zfill(2)
            )

            logger.info(f"Dados mensais agrupados: {len(df_mensal)} periodos")

            title = "Dividendos por Mes"
            if codigo_ativo:
                title += f" - {codigo_ativo}"
            if ano:
                title += f" - {ano}"
            if trimestre:
                trimestre_nome = {
                    1: "1º Trimestre",
                    2: "2º Trimestre",
                    3: "3º Trimestre",
                    4: "4º Trimestre",
                }
                title += (
                    f' - {trimestre_nome.get(trimestre, f"{trimestre}º Trimestre")}'
                )

            logger.info(f"Criando grafico com titulo: {title}")

            fig = px.bar(
                df_mensal,
                x="periodo",
                y="valor",
                title=title,
                labels={"valor": "Valor (R$)", "periodo": "Periodo"},
                color="valor",
                color_continuous_scale="Blues",
            )

            # Melhorar layout do grafico
            fig.update_layout(
                xaxis_title="Periodo (Ano-Mes)",
                yaxis_title="Valor Total (R$)",
                showlegend=False,
                height=600,
                width=1000,
            )

            filename = "dividendos_mensal.html"
            full_path = os.path.abspath(filename)
            fig.write_html(filename)
            logger.info(f"Grafico salvo como '{filename}'")
            logger.info(f"Caminho completo: {full_path}")

            # Tentar abrir no navegador
            try:
                webbrowser.open(f"file://{full_path}")
                logger.info("Grafico de dividendos aberto no navegador")
                print(f"Grafico de dividendos salvo: {filename}")
                print(f"Abrindo automaticamente no navegador...")
            except Exception as browser_error:
                logger.warning(
                    f"Nao foi possivel abrir automaticamente: {browser_error}"
                )
                print(f"Grafico salvo em: {full_path}")
                print("Abra manualmente o arquivo no navegador")

            return fig

        except ImportError as e:
            error_msg = "Plotly nao instalado. Instale com: pip install plotly"
            logger.error(error_msg)
            print(f"ERRO: {error_msg}")
            return None
        except Exception as e:
            logger.error(f"Erro ao criar grafico de dividendos: {e}")
            import traceback

            logger.error(f"Traceback: {traceback.format_exc()}")
            print(f"ERRO ao gerar grafico de dividendos: {e}")
            return None
