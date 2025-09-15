# ====================================
# SISTEMA PRINCIPAL B3 - VERSAO MODULAR
# ====================================

import logging
import sys
import argparse
from data_ingestion_workflow import DataIngestionWorkflow
from reports_workflow import ReportsWorkflow

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class B3System:
    """Sistema principal de análise B3"""
    
    def __init__(self):
        self.data_workflow = DataIngestionWorkflow()
        self.reports_workflow = ReportsWorkflow()
    
    def menu_principal(self):
        """Menu interativo do sistema"""
        while True:
            try:
                print(f"\nSISTEMA DE ANALISE B3")
                print("=" * 40)
                print("1. Consultar Ativos")
                print("2. Histórico de Cotações")
                print("3. Relatório de Dividendos")
                print("4. Dashboard de Alocação")
                print("5. Coletar Dados B3 (D-1)")
                print("6. Resumo do Sistema")
                print("7. Executar Todos os Relatórios")
                print("0. Sair")
                
                opcao = input("\nEscolha uma opção: ").strip()
                
                if opcao == "1":
                    self._handle_consulta_ativos()
                    
                elif opcao == "2":
                    self._handle_historico_cotacoes()
                    
                elif opcao == "3":
                    self._handle_relatorio_dividendos()
                    
                elif opcao == "4":
                    self._handle_dashboard_alocacao()
                    
                elif opcao == "5":
                    self._handle_coleta_dados()
                    
                elif opcao == "6":
                    self._handle_resumo_sistema()
                    
                elif opcao == "7":
                    self._handle_todos_relatorios()
                    
                elif opcao == "0":
                    print("Até logo!")
                    break
                    
                else:
                    print("ERRO: Opção inválida!")
                
                input("\nPressione Enter para continuar...")
                
            except KeyboardInterrupt:
                print("\n\nSistema interrompido pelo usuário.")
                break
            except Exception as e:
                logger.error(f"Erro no menu principal: {e}")
                print(f"ERRO: {e}")
    
    def _handle_consulta_ativos(self):
        """Manipula consulta de ativos"""
        print("\n=== CONSULTA DE ATIVOS ===")
        
        try:
            tipo = input("Filtrar por tipo (ou Enter para todos): ").strip() or None
            setor = input("Filtrar por setor (ou Enter para todos): ").strip() or None
            
            self.reports_workflow.execute_consulta_ativos(tipo, setor)
            
        except Exception as e:
            logger.error(f"Erro na consulta de ativos: {e}")
            print(f"ERRO: {e}")
    
    def _handle_historico_cotacoes(self):
        """Manipula histórico de cotações"""
        print("\n=== HISTÓRICO DE COTAÇÕES ===")
        
        try:
            codigo = input("Código do ativo: ").strip().upper()
            if not codigo:
                print("ERRO: Código do ativo é obrigatório")
                return
            
            periodo_input = input("Período em dias (padrão 30): ").strip()
            periodo = int(periodo_input) if periodo_input else 30
            
            gerar_grafico = input("Gerar gráfico? (s/N): ").strip().lower() == 's'
            
            self.reports_workflow.execute_historico_cotacoes(codigo, periodo, gerar_grafico)
            
        except ValueError:
            print("ERRO: Período deve ser um número")
        except Exception as e:
            logger.error(f"Erro no histórico de cotações: {e}")
            print(f"ERRO: {e}")
    
    def _handle_relatorio_dividendos(self):
        """Manipula relatório de dividendos"""
        print("\n=== RELATÓRIO DE DIVIDENDOS ===")
        
        try:
            codigo = input("Código do ativo (ou Enter para todos): ").strip().upper() or None
            ano_input = input("Ano (ou Enter para todos): ").strip()
            ano = int(ano_input) if ano_input else None
            
            gerar_grafico = input("Gerar gráfico? (s/N): ").strip().lower() == 's'
            
            self.reports_workflow.execute_relatorio_dividendos(codigo, ano, gerar_grafico)
            
        except ValueError:
            print("ERRO: Ano deve ser um número")
        except Exception as e:
            logger.error(f"Erro no relatório de dividendos: {e}")
            print(f"ERRO: {e}")
    
    def _handle_dashboard_alocacao(self):
        """Manipula dashboard de alocação"""
        print("\n=== DASHBOARD DE ALOCAÇÃO ===")
        
        try:
            gerar_graficos = input("Gerar gráficos? (S/n): ").strip().lower() != 'n'
            
            self.reports_workflow.execute_dashboard_alocacao(gerar_graficos)
            
        except Exception as e:
            logger.error(f"Erro no dashboard de alocação: {e}")
            print(f"ERRO: {e}")
    
    def _handle_coleta_dados(self):
        """Manipula coleta de dados B3"""
        print("\n=== COLETA DE DADOS B3 ===")
        
        try:
            print("Iniciando coleta de dados D-1...")
            
            if self.data_workflow.execute():
                print("SUCESSO: Coleta de dados concluída!")
            else:
                print("ERRO: Falha na coleta de dados")
                
        except Exception as e:
            logger.error(f"Erro na coleta de dados: {e}")
            print(f"ERRO: {e}")
    
    def _handle_resumo_sistema(self):
        """Manipula resumo do sistema"""
        print("\n=== RESUMO DO SISTEMA ===")
        
        try:
            self.reports_workflow.execute_resumo_sistema()
            
        except Exception as e:
            logger.error(f"Erro no resumo do sistema: {e}")
            print(f"ERRO: {e}")
    
    def _handle_todos_relatorios(self):
        """Manipula execução de todos os relatórios"""
        print("\n=== EXECUTANDO TODOS OS RELATÓRIOS ===")
        
        try:
            if self.reports_workflow.execute_all_reports():
                print("SUCESSO: Todos os relatórios foram executados!")
            else:
                print("ERRO: Falha na execução dos relatórios")
                
        except Exception as e:
            logger.error(f"Erro ao executar todos os relatórios: {e}")
            print(f"ERRO: {e}")

def main():
    """Função principal"""
    # Configurar argumentos de linha de comando
    parser = argparse.ArgumentParser(description='Sistema de Análise B3')
    parser.add_argument(
        '--gui', 
        action='store_true', 
        help='Executar com interface gráfica (padrão)'
    )
    parser.add_argument(
        '--terminal', 
        action='store_true', 
        help='Executar com interface de terminal'
    )
    
    args = parser.parse_args()
    
    # Se nenhuma opção for especificada, usar GUI por padrão
    if not args.gui and not args.terminal:
        args.gui = True  # Interface gráfica como padrão
    
    # Executar com interface gráfica
    if args.gui:
        try:
            from gui_interface import B3SystemGUI
            print("Iniciando interface gráfica...")
            app = B3SystemGUI()
            app.run()
        except ImportError as e:
            print(f"ERRO: Não foi possível importar a interface gráfica: {e}")
            print("Executando com interface de terminal...")
            args.terminal = True
            args.gui = False
        except Exception as e:
            logger.error(f"Erro na interface gráfica: {e}")
            print(f"ERRO na interface gráfica: {e}")
            print("Tentando executar com interface de terminal...")
            args.terminal = True
    
    # Executar com interface de terminal
    if args.terminal:
        try:
            print("Iniciando interface de terminal...")
            print("Conectando ao banco de dados...")
            
            # Inicializar sistema
            sistema = B3System()
            
            # Testar conexão
            if not sistema.data_workflow.db_manager.test_connection():
                print("ERRO: Não foi possível conectar ao banco de dados")
                print("Verifique se o PostgreSQL está rodando: docker-compose up -d")
                sys.exit(1)
            
            print("SUCESSO: Conectado com sucesso!")
            
            # Iniciar menu
            sistema.menu_principal()
            
        except KeyboardInterrupt:
            print("\nSistema interrompido pelo usuário.")
        except Exception as e:
            logger.error(f"Erro fatal no sistema: {e}")
            print(f"ERRO FATAL: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
