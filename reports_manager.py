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

                if "tipo" in df.columns and df["tipo"].notna().any():
                    print("Por tipo:")
                    print(df["tipo"].value_counts().to_string())

                if "setor" in df.columns and df["setor"].notna().any():
                    print("\nPor setor:")
                    print(df["setor"].value_counts().to_string())
            else:
                print("Nenhum ativo encontrado com os filtros especificados")

            return df

        except Exception as e:
            logger.error(f"Erro ao consultar ativos: {e}")
            return pd.DataFrame()

    def historico_cotacoes(self, codigo_ativo, periodo_dias=30):
        """Gera relatorio de historico de cotacoes"""
        try:
            from datetime import datetime, timedelta

            data_limite = datetime.now().date() - timedelta(days=periodo_dias)

            logger.info(f"Buscando histórico para {codigo_ativo} desde {data_limite}")

            # Primeiro verificar se o ativo existe
            ativo_query = "SELECT id, nome FROM ativos WHERE codigo = %s"
            ativo_df = self.db.execute_query(ativo_query, [codigo_ativo])

            if ativo_df.empty:
                print(f"ERRO: Ativo {codigo_ativo} não encontrado na base de dados")
                logger.error(f"Ativo {codigo_ativo} não encontrado")
                return None

            ativo_id = int(ativo_df.iloc[0]["id"])  # Converter numpy.int64 para int
            ativo_nome = ativo_df.iloc[0]["nome"]
            logger.info(
                f"Ativo encontrado: {codigo_ativo} - {ativo_nome} (ID: {ativo_id})"
            )

            # Verificar se há cotações para este ativo
            count_query = "SELECT COUNT(*) as total FROM cotacoes WHERE id_ativo = %s"
            count_df = self.db.execute_query(count_query, [ativo_id])

            # Verificar se o DataFrame não está vazio
            if count_df.empty:
                print(f"ERRO: Não foi possível verificar cotações para {codigo_ativo}")
                logger.error(f"Query de contagem falhou para {codigo_ativo}")
                return None

            total_cotacoes = count_df.iloc[0]["total"]

            logger.info(
                f"Total de cotações disponíveis para {codigo_ativo}: {total_cotacoes}"
            )

            if total_cotacoes == 0:
                print(f"ERRO: Nenhuma cotação encontrada para {codigo_ativo}")
                logger.error(f"Nenhuma cotação disponível para {codigo_ativo}")
                return None

            # Buscar cotações no período
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

            if df.empty:
                print(
                    f"ERRO: Nenhum dado encontrado para {codigo_ativo} no período de {periodo_dias} dias"
                )
                logger.warning(f"Nenhum dado no período para {codigo_ativo}")

                # Verificar qual é a data mais recente disponível
                recent_query = """
                    SELECT MAX(c.data) as data_mais_recente
                    FROM cotacoes c
                    JOIN ativos a ON c.id_ativo = a.id
                    WHERE a.codigo = %s
                """
                recent_df = self.db.execute_query(recent_query, [codigo_ativo])
                if not recent_df.empty and recent_df.iloc[0]["data_mais_recente"]:
                    data_recente = recent_df.iloc[0]["data_mais_recente"]
                    print(
                        f"INFORMAÇÃO: Última cotação disponível para {codigo_ativo}: {data_recente}"
                    )

                    # Se há dados mas não no período, sugerir período maior
                    from datetime import datetime

                    if isinstance(data_recente, str):
                        data_recente = datetime.strptime(
                            data_recente, "%Y-%m-%d"
                        ).date()

                    dias_diferenca = (datetime.now().date() - data_recente).days
                    if dias_diferenca > periodo_dias:
                        print(
                            f"SUGESTÃO: Tente um período maior que {dias_diferenca} dias"
                        )
                else:
                    print(
                        f"INFORMAÇÃO: Nenhuma cotação encontrada para {codigo_ativo} em qualquer período"
                    )
                    print(
                        "SUGESTÃO: Execute 'Coletar Dados B3' para obter cotações atualizadas"
                    )

                return None

            print(f"\nHISTORICO DE COTACOES - {codigo_ativo}")
            print(f"Periodo: {periodo_dias} dias | Registros: {len(df)}")
            print("=" * 60)

            # Estatisticas basicas
            ultimo_preco = df["preco_fechamento"].iloc[-1]
            primeiro_preco = df["preco_fechamento"].iloc[0]
            variacao = ((ultimo_preco - primeiro_preco) / primeiro_preco) * 100

            print(f"\nESTATISTICAS DO PERIODO:")
            print(f"Preco inicial: R$ {primeiro_preco:.2f}")
            print(f"Preco final: R$ {ultimo_preco:.2f}")
            print(f"Variacao: {variacao:+.2f}%")
            print(f"Maior alta: R$ {df['maximo'].max():.2f}")
            print(f"Menor baixa: R$ {df['minimo'].min():.2f}")

            logger.info(f"Histórico gerado com sucesso: {len(df)} registros")
            return df

        except Exception as e:
            logger.error(f"Erro ao gerar historico de cotacoes: {e}")
            import traceback

            logger.error(f"Traceback: {traceback.format_exc()}")
            return None

    def relatorio_dividendos(self, codigo_ativo=None, ano=None, trimestre=None):
        """Gera relatorio de dividendos/proventos"""
        try:
            query = """
                SELECT a.codigo, a.nome, d.data, d.valor, d.tipo,
                       EXTRACT(YEAR FROM d.data) as ano,
                       EXTRACT(MONTH FROM d.data) as mes,
                       CASE 
                           WHEN EXTRACT(MONTH FROM d.data) BETWEEN 1 AND 3 THEN 1
                           WHEN EXTRACT(MONTH FROM d.data) BETWEEN 4 AND 6 THEN 2
                           WHEN EXTRACT(MONTH FROM d.data) BETWEEN 7 AND 9 THEN 3
                           WHEN EXTRACT(MONTH FROM d.data) BETWEEN 10 AND 12 THEN 4
                       END as trimestre
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

            query += " ORDER BY d.data DESC"

            df = self.db.execute_query(query, params if params else None)

            if df.empty:
                print("ERRO: Nenhum dividendo encontrado")
                return None

            print(f"\nRELATORIO DE DIVIDENDOS")
            if codigo_ativo:
                print(f"Ativo: {codigo_ativo}")
            if ano:
                print(f"Ano: {ano}")
            if trimestre:
                trimestre_nome = {
                    1: "1º Trimestre",
                    2: "2º Trimestre",
                    3: "3º Trimestre",
                    4: "4º Trimestre",
                }
                print(f"Trimestre: {trimestre_nome.get(trimestre, trimestre)}")
            print("=" * 60)

            # Resumo por ativo
            resumo = (
                df.groupby(["codigo", "nome"])
                .agg({"valor": ["sum", "count", "mean"], "data": ["min", "max"]})
                .round(2)
            )

            print("RESUMO POR ATIVO:")
            print(resumo)

            return df

        except Exception as e:
            logger.error(f"Erro ao gerar relatorio de dividendos: {e}")
            return None

    def resumo_sistema(self):
        """Gera resumo do sistema"""
        try:
            print("\nRESUMO DO SISTEMA")
            print("=" * 50)

            # Contar registros por tabela
            tabelas = ["ativos", "cotacoes", "dividendos"]

            for tabela in tabelas:
                count = self.db.get_table_count(tabela)
                print(f"{tabela:12s}: {count:6d} registros")

            # Data mais recente de cotacoes
            try:
                query = "SELECT MAX(data) as ultima_data FROM cotacoes"
                result = self.db.execute_query(query)
                if not result.empty and result["ultima_data"].iloc[0] is not None:
                    ultima_data = result["ultima_data"].iloc[0]
                    print(f"\nUltima cotacao: {ultima_data}")
            except:
                print("\nUltima cotacao: Nao disponivel")

        except Exception as e:
            logger.error(f"Erro ao gerar resumo do sistema: {e}")
