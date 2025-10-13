# ====================================
# WORKFLOW: GERACAO DE RELATORIOS
# ====================================

import logging
from reports_manager import ReportsManager
from visualization_manager import VisualizationManager

# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ReportsWorkflow:
    """Workflow para geracao de relatorios"""

    def __init__(self):
        self.reports_manager = ReportsManager()
        self.viz_manager = VisualizationManager()

    def execute_consulta_ativos(self, filtro_tipo=None, filtro_setor=None):
        """Executa consulta de ativos"""
        logger.info("=== EXECUTANDO CONSULTA DE ATIVOS ===")

        try:
            df = self.reports_manager.consultar_ativos(filtro_tipo, filtro_setor)
            logger.info("Consulta de ativos concluida")
            return df
        except Exception as e:
            logger.error(f"Erro na consulta de ativos: {e}")
            return None

    def execute_historico_cotacoes(
        self, codigo_ativo, periodo_dias=30, gerar_grafico=True
    ):
        """Executa relatorio de historico de cotacoes"""
        logger.info(f"=== EXECUTANDO HISTORICO DE COTACOES - {codigo_ativo} ===")

        try:
            # Gerar relatorio
            df = self.reports_manager.historico_cotacoes(codigo_ativo, periodo_dias)

            if df is None or df.empty:
                logger.warning(f"Nenhum dado retornado para {codigo_ativo}")
                return None

            logger.info(f"Dados obtidos: {len(df)} registros para {codigo_ativo}")

            # Gerar grafico se solicitado
            if gerar_grafico:
                logger.info(f"Gerando gráfico para {codigo_ativo}...")
                try:
                    grafico = self.viz_manager.create_candlestick_chart(
                        codigo_ativo, periodo_dias
                    )
                    if grafico:
                        logger.info(f"Gráfico gerado com sucesso para {codigo_ativo}")
                    else:
                        logger.warning(f"Falha ao gerar gráfico para {codigo_ativo}")
                except Exception as viz_error:
                    logger.error(f"Erro na geração do gráfico: {viz_error}")
                    # Não falha a operação inteira se só o gráfico deu erro

            logger.info("Historico de cotacoes concluido")
            return df

        except Exception as e:
            logger.error(f"Erro no historico de cotacoes: {e}")
            import traceback

            logger.error(f"Traceback: {traceback.format_exc()}")
            return None

    def execute_relatorio_dividendos(
        self, codigo_ativo=None, ano=None, trimestre=None, gerar_grafico=True
    ):
        """Executa relatorio de dividendos"""
        logger.info("=== EXECUTANDO RELATORIO DE DIVIDENDOS ===")

        try:
            # Gerar relatorio
            df = self.reports_manager.relatorio_dividendos(codigo_ativo, ano, trimestre)

            if df is None:
                return None

            # Gerar grafico se solicitado
            if gerar_grafico:
                self.viz_manager.create_dividends_chart(codigo_ativo, ano, trimestre)

            logger.info("Relatorio de dividendos concluido")
            return df

        except Exception as e:
            logger.error(f"Erro no relatorio de dividendos: {e}")
            return None

    def execute_resumo_sistema(self):
        """Executa resumo do sistema"""
        logger.info("=== EXECUTANDO RESUMO DO SISTEMA ===")

        try:
            self.reports_manager.resumo_sistema()
            logger.info("Resumo do sistema concluido")
            return True
        except Exception as e:
            logger.error(f"Erro no resumo do sistema: {e}")
            return False

    def execute_all_reports(self):
        """Executa todos os relatorios disponiveis"""
        logger.info("=== EXECUTANDO TODOS OS RELATORIOS ===")

        try:
            # Resumo do sistema
            self.execute_resumo_sistema()

            # Consulta de ativos (sem filtro)
            self.execute_consulta_ativos()

            logger.info("Todos os relatorios foram executados")
            return True

        except Exception as e:
            logger.error(f"Erro ao executar todos os relatorios: {e}")
            return False


def main():
    """Funcao principal para execucao standalone"""
    workflow = ReportsWorkflow()

    print("Executando todos os relatorios disponiveis...")
    workflow.execute_all_reports()


if __name__ == "__main__":
    main()
