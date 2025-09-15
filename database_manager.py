# ====================================
# MODULO: OPERACOES DE BANCO DE DADOS
# ====================================

import pandas as pd
import logging
from config import engine

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Gerenciador de operacoes do banco de dados"""
    
    def __init__(self):
        self.engine = engine
    
    def test_connection(self):
        """Testa a conexao com o banco de dados"""
        try:
            from sqlalchemy import text
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1 as test"))
                test_value = result.fetchone()[0]
                if test_value == 1:
                    logger.info("Conexao com banco de dados estabelecida com sucesso")
                    return True
                else:
                    logger.error("Teste de conexao falhou")
                    return False
        except Exception as e:
            logger.error(f"Erro de conexao com banco: {e}")
            logger.info("Verifique se o PostgreSQL está rodando: docker-compose up -d")
            return False
    
    def get_existing_ativos(self):
        """Busca ativos existentes no banco"""
        try:
            query = "SELECT id, codigo FROM ativos"
            df = pd.read_sql(query, self.engine)
            logger.info(f"Encontrados {len(df)} ativos no banco")
            return df
        except Exception as e:
            logger.error(f"Erro ao buscar ativos: {e}")
            return pd.DataFrame()
    
    def sync_ativos(self, df_ativos_novos):
        """Sincroniza completamente a tabela de ativos com tipo e setor"""
        try:
            if df_ativos_novos.empty:
                logger.info("Nenhum ativo para sincronizar")
                return True
            
            from sqlalchemy import text
            
            with self.engine.connect() as conn:
                # 1. Primeiro, garantir que as colunas tipo e setor existem
                try:
                    conn.execute(text("ALTER TABLE ativos ADD COLUMN IF NOT EXISTS tipo VARCHAR(20)"))
                    conn.execute(text("ALTER TABLE ativos ADD COLUMN IF NOT EXISTS setor VARCHAR(80)"))
                    conn.commit()
                    logger.info("Colunas tipo e setor verificadas/criadas")
                except Exception as e:
                    logger.warning(f"Erro ao adicionar colunas (podem já existir): {e}")
                
                # 2. Remover coluna quantidade se existir (migração)
                try:
                    # Verificar se a coluna existe antes de tentar remover
                    result = conn.execute(text("""
                        SELECT column_name FROM information_schema.columns 
                        WHERE table_name = 'cotacoes' AND column_name = 'quantidade'
                    """))
                    if result.fetchone():
                        conn.execute(text("ALTER TABLE cotacoes DROP COLUMN quantidade"))
                        conn.commit()
                        logger.info("Coluna 'quantidade' removida da tabela cotacoes")
                except Exception as e:
                    logger.warning(f"Erro ao remover coluna quantidade (pode não existir): {e}")
                
                # 3. Inserir/Atualizar ativos usando UPSERT
                logger.info(f"Sincronizando {len(df_ativos_novos)} ativos...")
                for _, row in df_ativos_novos.iterrows():
                    upsert_query = text("""
                        INSERT INTO ativos (codigo, nome, tipo, setor)
                        VALUES (:codigo, :nome, :tipo, :setor)
                        ON CONFLICT (codigo) 
                        DO UPDATE SET 
                            nome = EXCLUDED.nome,
                            tipo = EXCLUDED.tipo,
                            setor = EXCLUDED.setor
                    """)
                    
                    conn.execute(upsert_query, {
                        'codigo': row['codigo'],
                        'nome': row['nome'],
                        'tipo': row['tipo'],
                        'setor': row['setor']
                    })
                
                # 3. Remover ativos que não estão mais na coleta atual
                # Buscar códigos atuais no banco
                current_codes_result = conn.execute(text("SELECT codigo FROM ativos"))
                current_codes_db = [row[0] for row in current_codes_result.fetchall()]
                
                # Códigos da nova coleta
                new_codes = set(df_ativos_novos['codigo'].tolist())
                codes_to_remove = [code for code in current_codes_db if code not in new_codes]
                
                removed_count = 0
                if codes_to_remove:
                    for code in codes_to_remove:
                        # Verificar se o ativo tem cotações ou dividendos antes de remover
                        has_data = conn.execute(text("""
                            SELECT 1 FROM cotacoes c 
                            JOIN ativos a ON c.id_ativo = a.id 
                            WHERE a.codigo = :codigo 
                            LIMIT 1
                        """), {'codigo': code}).fetchone()
                        
                        if not has_data:
                            # Só remove se não tiver dados históricos
                            conn.execute(text("DELETE FROM ativos WHERE codigo = :codigo"), {'codigo': code})
                            removed_count += 1
                
                conn.commit()
                
                logger.info(f"Sincronização de ativos concluída:")
                logger.info(f"- {len(df_ativos_novos)} ativos atualizados/inseridos")
                logger.info(f"- {removed_count} ativos sem dados removidos")
                
                return True
                
        except Exception as e:
            logger.error(f"Erro ao sincronizar ativos: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
    
    def insert_cotacoes(self, df_cotacoes, data_referencia):
        """Insere ou atualiza cotacoes no banco"""
        try:
            if df_cotacoes.empty:
                logger.warning("Nenhuma cotacao para inserir")
                return False
            
            data_str = data_referencia.strftime('%Y-%m-%d')
            
            # Sempre remover cotações existentes da data primeiro
            from sqlalchemy import text
            with self.engine.connect() as conn:
                # Usar formato de data mais específico
                result = conn.execute(text("DELETE FROM cotacoes WHERE DATE(data) = :target_date"), 
                                    {'target_date': data_str})
                deleted_count = result.rowcount
                conn.commit()
                
                logger.info(f"Removidas {deleted_count} cotacoes existentes para {data_str}")
                
                # Verificar se ainda existem duplicatas
                check_result = conn.execute(text("SELECT COUNT(*) as count FROM cotacoes WHERE DATE(data) = :target_date"), 
                                          {'target_date': data_str})
                remaining = check_result.fetchone()[0]
                
                if remaining > 0:
                    logger.warning(f"Ainda existem {remaining} cotacoes para {data_str}. Removendo novamente...")
                    conn.execute(text("DELETE FROM cotacoes WHERE DATE(data) = :target_date"), 
                               {'target_date': data_str})
                    conn.commit()
            
            # Inserir dados usando inserção em lotes para melhor performance
            batch_size = 1000
            total_inserted = 0
            
            with self.engine.connect() as conn:
                for i in range(0, len(df_cotacoes), batch_size):
                    batch = df_cotacoes.iloc[i:i+batch_size]
                    
                    # Preparar dados para inserção
                    insert_data = []
                    for _, row in batch.iterrows():
                        insert_data.append({
                            'id_ativo': int(row['id_ativo']),
                            'data': row['data'],
                            'preco_abertura': float(row['preco_abertura']) if pd.notna(row['preco_abertura']) else None,
                            'preco_fechamento': float(row['preco_fechamento']) if pd.notna(row['preco_fechamento']) else None,
                            'maximo': float(row['maximo']) if pd.notna(row['maximo']) else None,
                            'minimo': float(row['minimo']) if pd.notna(row['minimo']) else None,
                            'negocios': int(row['negocios']) if pd.notna(row['negocios']) else None,
                            'volume_financeiro': float(row['volume_financeiro']) if pd.notna(row['volume_financeiro']) else None
                        })
                    
                    # Inserir lote com UPSERT (evita duplicatas)
                    conn.execute(text("""
                        INSERT INTO cotacoes (id_ativo, data, preco_abertura, preco_fechamento, 
                                            maximo, minimo, negocios, volume_financeiro)
                        VALUES (:id_ativo, :data, :preco_abertura, :preco_fechamento,
                                :maximo, :minimo, :negocios, :volume_financeiro)
                        ON CONFLICT (id_ativo, data) 
                        DO UPDATE SET 
                            preco_abertura = EXCLUDED.preco_abertura,
                            preco_fechamento = EXCLUDED.preco_fechamento,
                            maximo = EXCLUDED.maximo,
                            minimo = EXCLUDED.minimo,
                            negocios = EXCLUDED.negocios,
                            volume_financeiro = EXCLUDED.volume_financeiro
                    """), insert_data)
                    
                    total_inserted += len(insert_data)
                    logger.info(f"Inserido lote {i//batch_size + 1}: {len(insert_data)} cotacoes")
                
                conn.commit()
            
            logger.info(f"Inseridas {total_inserted} cotacoes para {data_str}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao inserir cotacoes: {e}")
            return False
    
    def execute_query(self, query, params=None):
        """Executa uma query personalizada"""
        try:
            if params and len(params) > 0:
                # Converter lista para dicionário se necessário
                if isinstance(params, list):
                    # Para queries com %s, usar lista diretamente
                    df = pd.read_sql(query, self.engine, params=params)
                else:
                    # Para queries com :param, usar dicionário
                    df = pd.read_sql(query, self.engine, params=params)
            else:
                # Se não há parâmetros, usar sem params
                df = pd.read_sql(query, self.engine)
            logger.info(f"Query executada com sucesso. Retornadas {len(df)} linhas")
            return df
        except Exception as e:
            logger.error(f"Erro ao executar query: {e}")
            logger.error(f"Query: {query}")
            logger.error(f"Params: {params}")
            # Tentar execução alternativa sem parâmetros se falhar
            try:
                if params:
                    logger.warning("Tentando execução sem parâmetros...")
                    df = pd.read_sql(query.replace('%s', "''"), self.engine)
                    logger.info(f"Query alternativa executada. Retornadas {len(df)} linhas")
                    return df
            except:
                pass
            return pd.DataFrame()
    
    def insert_dividendos(self, df_dividendos, ativos_db):
        """Insere dividendos no banco"""
        try:
            if df_dividendos.empty:
                logger.warning("Nenhum dividendo para inserir")
                return True
            
            # Fazer merge com ativos do banco para obter IDs
            df_dividendos['codigo'] = df_dividendos['codigo'].astype(str)
            ativos_db['codigo'] = ativos_db['codigo'].astype(str)
            
            df_merged = df_dividendos.merge(ativos_db, how='left', on='codigo')
            df_merged = df_merged.dropna(subset=['id'])  # Remover ativos não encontrados
            
            if df_merged.empty:
                logger.warning("Nenhum dividendo com ativo válido encontrado")
                return True
            
            # Preparar dados para inserção
            insert_data = []
            for _, row in df_merged.iterrows():
                insert_data.append({
                    'id_ativo': int(row['id']),
                    'data': row['data'],
                    'valor': float(row['valor']),
                    'tipo': row['tipo']
                })
            
            # Inserir com UPSERT (evita duplicatas)
            from sqlalchemy import text
            with self.engine.connect() as conn:
                conn.execute(text("""
                    INSERT INTO dividendos (id_ativo, data, valor, tipo)
                    VALUES (:id_ativo, :data, :valor, :tipo)
                    ON CONFLICT (id_ativo, data) 
                    DO UPDATE SET 
                        valor = EXCLUDED.valor,
                        tipo = EXCLUDED.tipo
                """), insert_data)
                conn.commit()
            
            logger.info(f"Inseridos/atualizados {len(insert_data)} dividendos")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao inserir dividendos: {e}")
            return False

    def get_table_count(self, table_name):
        """Retorna o numero de registros de uma tabela"""
        try:
            result = pd.read_sql(f"SELECT COUNT(*) as count FROM {table_name}", self.engine)
            return result['count'][0]
        except Exception as e:
            logger.error(f"Erro ao contar registros da tabela {table_name}: {e}")
            return 0
    
    def check_and_create_tables(self):
        """Verifica se as tabelas existem e cria se necessário"""
        try:
            # Verificar se as tabelas existem
            tables_query = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            """
            existing_tables = pd.read_sql(tables_query, self.engine)['table_name'].tolist()
            
            required_tables = ['ativos', 'cotacoes', 'dividendos']
            missing_tables = [table for table in required_tables if table not in existing_tables]
            
            if missing_tables:
                logger.info(f"Tabelas faltando: {missing_tables}")
                logger.info("Criando tabelas...")
                
                # Executar schema.sql
                import os
                schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
                if os.path.exists(schema_path):
                    with open(schema_path, 'r') as f:
                        schema_sql = f.read()
                    
                    from sqlalchemy import text
                    with self.engine.connect() as conn:
                        conn.execute(text(schema_sql))
                        conn.commit()
                    
                    logger.info("Tabelas criadas com sucesso")
                else:
                    logger.error("Arquivo schema.sql não encontrado")
                    return False
            else:
                logger.info("Todas as tabelas já existem")
            
            # Verificar e corrigir constraints da tabela dividendos
            self._fix_dividendos_constraint()
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao verificar/criar tabelas: {e}")
            return False
    
    def _fix_dividendos_constraint(self):
        """Corrige constraint da tabela dividendos se necessário"""
        try:
            from sqlalchemy import text
            with self.engine.connect() as conn:
                # Verificar se a constraint existe
                check_constraint = """
                SELECT constraint_name 
                FROM information_schema.table_constraints 
                WHERE table_name = 'dividendos' 
                AND constraint_type = 'UNIQUE'
                AND constraint_name LIKE '%id_ativo%data%'
                """
                result = conn.execute(text(check_constraint))
                constraints = result.fetchall()
                
                if not constraints:
                    logger.info("Adicionando constraint única para dividendos...")
                    # Primeiro remover duplicatas se existirem
                    remove_duplicates = """
                    DELETE FROM dividendos a USING dividendos b 
                    WHERE a.id > b.id 
                    AND a.id_ativo = b.id_ativo 
                    AND a.data = b.data
                    """
                    conn.execute(text(remove_duplicates))
                    
                    # Adicionar constraint
                    add_constraint = """
                    ALTER TABLE dividendos 
                    ADD CONSTRAINT dividendos_id_ativo_data_unique 
                    UNIQUE (id_ativo, data)
                    """
                    conn.execute(text(add_constraint))
                    conn.commit()
                    logger.info("Constraint de dividendos corrigida")
                else:
                    logger.info("Constraint de dividendos já existe")
                    
        except Exception as e:
            logger.warning(f"Não foi possível corrigir constraint de dividendos: {e}")
