# ====================================
# WORKFLOW: INGESTAO DE DADOS
# ====================================

import logging
import sys
from database_manager import DatabaseManager
from data_collector import B3DataCollector
from config import calcular_d1

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataIngestionWorkflow:
    """Workflow para ingestao de dados da B3"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.data_collector = B3DataCollector()
        self.data_d1 = calcular_d1()
    
    def execute(self):
        """Executa o workflow completo de ingestao"""
        try:
            logger.info("=== INICIANDO WORKFLOW DE INGESTAO DE DADOS ===")
            
            # 1. Verificar conexao com banco
            if not self._check_database_connection():
                return False
            
            # 2. Coletar e processar dados
            df_transformed, df_ativos, df_dividendos = self._collect_and_process_data()
            if df_transformed is None:
                return False
            
            # 3. Processar ativos
            if not self._process_ativos(df_ativos):
                return False
            
            # 4. Processar cotacoes
            if not self._process_cotacoes(df_transformed):
                return False
            
            # 5. Processar dividendos
            if not self._process_dividendos(df_dividendos):
                return False
            
            logger.info("=== WORKFLOW DE INGESTAO CONCLUIDO COM SUCESSO ===")
            return True
            
        except Exception as e:
            logger.error(f"Erro no workflow de ingestao: {e}")
            return False
    
    def _check_database_connection(self):
        """Verifica conexao com banco de dados"""
        logger.info("Verificando conexao com banco de dados...")
        
        if not self.db_manager.test_connection():
            logger.error("Falha na conexao com banco de dados")
            return False
        
        # Verificar e criar tabelas se necessário
        if not self.db_manager.check_and_create_tables():
            logger.error("Falha ao verificar/criar tabelas")
            return False
        
        return True
    
    def _collect_and_process_data(self):
        """Coleta e processa dados da B3"""
        logger.info("Iniciando coleta de dados da B3...")
        
        df_transformed, df_ativos, df_dividendos = self.data_collector.collect_and_process_data()
        
        if df_transformed is None or df_ativos is None:
            logger.error("Falha na coleta/processamento de dados")
            return None, None, None
        
        return df_transformed, df_ativos, df_dividendos
    
    def _process_ativos(self, df_ativos):
        """Sincroniza ativos com tipo e setor"""
        logger.info("Sincronizando ativos com tipo e setor...")
        
        try:
            # Sincronizar todos os ativos (inserir novos, atualizar existentes, remover inativos)
            if not self.db_manager.sync_ativos(df_ativos):
                logger.error("Falha ao sincronizar ativos")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao sincronizar ativos: {e}")
            return False
    
    def _process_cotacoes(self, df_transformed):
        """Processa cotacoes"""
        logger.info("Processando cotacoes...")
        
        try:
            # Buscar ativos atualizados do banco
            ativos_db = self.db_manager.get_existing_ativos()
            
            # Preparar cotacoes
            df_cotacoes = self.data_collector.prepare_cotacoes(df_transformed, ativos_db)
            
            if df_cotacoes.empty:
                logger.warning("Nenhuma cotacao valida para processar")
                return True
            
            # Inserir cotacoes
            if not self.db_manager.insert_cotacoes(df_cotacoes, self.data_d1):
                logger.error("Falha ao inserir cotacoes")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao processar cotacoes: {e}")
            return False
    
    def _process_dividendos(self, df_dividendos):
        """Processa dividendos"""
        logger.info("Processando dividendos...")
        
        try:
            if df_dividendos.empty:
                logger.info("Nenhum dividendo para processar")
                return True
            
            # Buscar ativos atualizados do banco
            ativos_db = self.db_manager.get_existing_ativos()
            
            # Inserir dividendos
            if not self.db_manager.insert_dividendos(df_dividendos, ativos_db):
                logger.error("Falha ao inserir dividendos")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao processar dividendos: {e}")
            return False

def main():
    """Funcao principal para execucao standalone"""
    workflow = DataIngestionWorkflow()
    
    if workflow.execute():
        logger.info("Workflow executado com sucesso!")
        sys.exit(0)
    else:
        logger.error("Workflow falhou!")
        sys.exit(1)

if __name__ == "__main__":
    main()
