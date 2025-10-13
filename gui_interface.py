# ====================================
# INTERFACE GRAFICA - GUI SYSTEM
# ====================================

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import logging
import sys
import io
import contextlib
import pandas as pd
from data_ingestion_workflow import DataIngestionWorkflow
from reports_workflow import ReportsWorkflow

# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class B3SystemGUI:
    """Interface gráfica para o Sistema B3"""

    def __init__(self):
        self.data_workflow = DataIngestionWorkflow()
        self.reports_workflow = ReportsWorkflow()

        # Criar janela principal
        self.root = tk.Tk()
        self.root.title("Sistema de Análise B3 - Interface Gráfica")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Configurar estilo
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.setup_ui()

    def setup_ui(self):
        """Configurar interface do usuário"""

        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # Título
        title_label = ttk.Label(
            main_frame, text="Sistema de Análise B3", font=("Arial", 18, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 20))

        # Subtitle
        subtitle_label = ttk.Label(
            main_frame,
            text="Análise de dados financeiros com geração de gráficos interativos",
            font=("Arial", 10),
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 30))

        # Frame para operações do sistema (PRIMEIRO - mais importante)
        system_frame = ttk.LabelFrame(
            main_frame, text="Operações do Sistema (Execute Primeiro)", padding="15"
        )
        system_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        system_frame.columnconfigure(0, weight=1)
        system_frame.columnconfigure(1, weight=1)
        system_frame.columnconfigure(2, weight=1)

        btn_coleta = ttk.Button(
            system_frame,
            text=" Coletar Dados B3 (D-1)",
            command=self.coletar_dados,
            width=25,
        )
        btn_coleta.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

        # Botão para coletar dados históricos
        btn_historico = ttk.Button(
            system_frame,
            text="Dados Historicos (30d)",
            command=self.coletar_historico,
            width=25,
        )
        btn_historico.grid(row=0, column=2, padx=5, pady=5, sticky=(tk.W, tk.E))

        btn_resumo = ttk.Button(
            system_frame,
            text=" Resumo do Sistema",
            command=self.resumo_sistema,
            width=25,
        )
        btn_resumo.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        # Aviso importante
        aviso_label = ttk.Label(
            system_frame,
            text="Execute 'Coletar Dados B3' primeiro para ter dados nos relatórios",
            font=("Arial", 9, "italic"),
            foreground="orange",
        )
        aviso_label.grid(row=1, column=0, columnspan=2, pady=(5, 0))

        # Frame para relatórios e consultas (SEGUNDO - após ter dados)
        buttons_frame = ttk.LabelFrame(
            main_frame, text="Relatórios e Consultas (Após Coletar Dados)", padding="15"
        )
        buttons_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)

        # Botões de relatórios
        btn_ativos = ttk.Button(
            buttons_frame,
            text=" Consultar Ativos",
            command=self.consultar_ativos,
            width=25,
        )
        btn_ativos.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

        btn_cotacoes = ttk.Button(
            buttons_frame,
            text=" Histórico de Cotações",
            command=self.historico_cotacoes,
            width=25,
        )
        btn_cotacoes.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        btn_dividendos = ttk.Button(
            buttons_frame,
            text=" Relatório de Dividendos",
            command=self.relatorio_dividendos,
            width=25,
        )
        btn_dividendos.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

        btn_todos = ttk.Button(
            buttons_frame,
            text=" Executar Todos os Relatórios",
            command=self.todos_relatorios,
            width=25,
        )
        btn_todos.grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        # Frame para log/status
        log_frame = ttk.LabelFrame(main_frame, text="Status e Log", padding="10")
        log_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)

        # Área de texto para log
        self.log_text = tk.Text(log_frame, height=10, wrap=tk.WORD, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(
            log_frame, orient=tk.VERTICAL, command=self.log_text.yview
        )
        self.log_text.configure(yscrollcommand=scrollbar.set)

        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Botão sair
        btn_sair = ttk.Button(
            main_frame, text=" Sair", command=self.root.quit, width=15
        )
        btn_sair.grid(row=5, column=0, pady=(10, 0))

        # Testar conexão na inicialização
        self.testar_conexao_inicial()

    def log_message(self, message):
        """Adiciona mensagem ao log da interface"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()

    @contextlib.contextmanager
    def capture_output(self):
        """Context manager para capturar print statements"""
        old_stdout = sys.stdout
        sys.stdout = mystdout = io.StringIO()
        try:
            yield mystdout
        finally:
            sys.stdout = old_stdout

    def show_result_window(self, title, content, data_frame=None):
        """Exibe janela com resultados detalhados"""
        result_window = tk.Toplevel(self.root)
        result_window.title(title)
        result_window.geometry("900x600")
        result_window.resizable(True, True)

        # Frame principal
        main_frame = ttk.Frame(result_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        title_label = ttk.Label(main_frame, text=title, font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 10))

        # Notebook para abas
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Aba de texto
        text_frame = ttk.Frame(notebook)
        notebook.add(text_frame, text=" Relatório")

        # Área de texto com scroll
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Consolas", 10))
        text_scrollbar = ttk.Scrollbar(
            text_frame, orient=tk.VERTICAL, command=text_widget.yview
        )
        text_widget.configure(yscrollcommand=text_scrollbar.set)

        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Inserir conteúdo
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)

        # Aba de dados (se DataFrame disponível)
        if data_frame is not None and not data_frame.empty:
            data_frame = self.create_data_table(notebook, data_frame)

        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)

        ttk.Button(
            button_frame,
            text=" Copiar Texto",
            command=lambda: self.copy_to_clipboard(content),
        ).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(button_frame, text=" Fechar", command=result_window.destroy).pack(
            side=tk.RIGHT
        )

        # Centralizar janela
        result_window.transient(self.root)
        result_window.grab_set()

        return result_window

    def create_data_table(self, parent, df):
        """Cria tabela para exibir DataFrame"""
        data_frame = ttk.Frame(parent)
        parent.add(data_frame, text=" Dados")

        # Criar Treeview
        columns = list(df.columns)
        tree = ttk.Treeview(data_frame, columns=columns, show="headings", height=20)

        # Configurar colunas
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        # Inserir dados
        for index, row in df.iterrows():
            values = [str(val) if pd.notna(val) else "" for val in row.values]
            tree.insert("", tk.END, values=values)

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(data_frame, orient=tk.VERTICAL, command=tree.yview)
        h_scrollbar = ttk.Scrollbar(
            data_frame, orient=tk.HORIZONTAL, command=tree.xview
        )
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Pack widgets
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        return data_frame

    def copy_to_clipboard(self, text):
        """Copia texto para clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Copiado", "Texto copiado para a área de transferência!")

    def show_dataframe_summary(self, df, title="Dados"):
        """Exibe resumo do DataFrame"""
        if df is None or df.empty:
            return "Nenhum dado encontrado."

        summary = f"=== {title} ===\n"
        summary += f"Total de registros: {len(df)}\n"
        summary += f"Colunas: {', '.join(df.columns)}\n\n"

        # Mostrar primeiras linhas
        summary += "PRIMEIRAS LINHAS:\n"
        summary += "=" * 50 + "\n"
        summary += df.head(10).to_string(index=False) + "\n\n"

        # Estatísticas se houver colunas numéricas
        numeric_cols = df.select_dtypes(include=["number"]).columns
        if len(numeric_cols) > 0:
            summary += "ESTATÍSTICAS:\n"
            summary += "=" * 50 + "\n"
            summary += df[numeric_cols].describe().to_string() + "\n"

        return summary

    def testar_conexao_inicial(self):
        """Testa conexão com o banco na inicialização"""
        self.log_message("Testando conexão com o banco de dados...")

        try:
            if self.data_workflow.db_manager.test_connection():
                self.log_message("SUCESSO: Conectado ao banco de dados!")
            else:
                self.log_message("ERRO: Não foi possível conectar ao banco")
                self.log_message(
                    "Dica: Execute 'docker-compose up -d' para iniciar o PostgreSQL"
                )
        except Exception as e:
            self.log_message(f"ERRO na conexão: {e}")

    def run_in_thread(self, func):
        """Executa função em thread separada para não travar a interface"""
        thread = threading.Thread(target=func, daemon=True)
        thread.start()

    def consultar_ativos(self):
        """Handler para consulta de ativos"""

        def execute():
            try:
                self.log_message("Iniciando consulta de ativos...")

                # Criar janela de filtros
                dialog = FilterDialog(self.root, "Filtros para Consulta de Ativos")

                if dialog.result:
                    filtro_tipo = dialog.result.get("tipo")
                    filtro_setor = dialog.result.get("setor")

                    self.log_message(
                        f"Aplicando filtros - Tipo: {filtro_tipo or 'Todos'}, Setor: {filtro_setor or 'Todos'}"
                    )

                    # Capturar saída do console
                    with self.capture_output() as output:
                        df = self.reports_workflow.execute_consulta_ativos(
                            filtro_tipo, filtro_setor
                        )

                    console_output = output.getvalue()

                    if df is not None and not df.empty:
                        self.log_message(
                            f"Consulta concluída! {len(df)} ativos encontrados"
                        )

                        # Criar conteúdo para janela de resultado
                        title = "Consulta de Ativos"
                        content = (
                            console_output
                            + "\n\n"
                            + self.show_dataframe_summary(df, "Lista de Ativos")
                        )

                        # Exibir janela de resultado
                        self.show_result_window(title, content, df)

                    else:
                        self.log_message(
                            "Nenhum ativo encontrado com os filtros especificados"
                        )
                        messagebox.showwarning(
                            "Aviso",
                            "Nenhum ativo encontrado com os filtros especificados",
                        )
                else:
                    self.log_message("Consulta cancelada pelo usuário")

            except Exception as e:
                error_msg = f"Erro na consulta de ativos: {e}"
                self.log_message(f"{error_msg}")
                messagebox.showerror("Erro", error_msg)

        self.run_in_thread(execute)

    def historico_cotacoes(self):
        """Handler para histórico de cotações"""

        def execute():
            try:
                self.log_message("=== INICIANDO HISTÓRICO DE COTAÇÕES ===")

                # Criar janela de seleção de ativo
                self.log_message("Abrindo janela de seleção de ativo...")
                dialog = AssetSelectionDialog(self.root, self.data_workflow.db_manager)

                self.log_message("Janela de seleção fechada, verificando resultado...")

                if dialog.result:
                    self.log_message(
                        f"Resultado do dialogo: {dialog.result}"
                    )  # Debug temporário
                    codigo = dialog.result.get("codigo")
                    periodo = dialog.result.get("periodo", 30)
                    gerar_grafico = dialog.result.get("gerar_grafico", True)

                    if not codigo:
                        self.log_message("Operacao cancelada - codigo nao informado")
                        return

                    self.log_message(
                        f"Gerando historico de cotacoes para {codigo} ({periodo} dias)..."
                    )

                    # Capturar saída do console
                    with self.capture_output() as output:
                        df = self.reports_workflow.execute_historico_cotacoes(
                            codigo, periodo, gerar_grafico
                        )

                    console_output = output.getvalue()
                    self.log_message(
                        f"DataFrame retornado: {df is not None}, Vazio: {df.empty if df is not None else 'N/A'}"
                    )
                    self.log_message(
                        f"Console output length: {len(console_output) if console_output else 0}"
                    )

                    if df is not None and not df.empty:
                        msg = f"Historico gerado para {codigo}! ({len(df)} registros encontrados)"
                        if gerar_grafico:
                            import os

                            graph_path = os.path.abspath(f"historico_{codigo}.html")
                            msg += f"\nGrafico salvo como 'historico_{codigo}.html'"
                            msg += f"\nLocal: {graph_path}"
                            msg += f"\nO grafico deve abrir automaticamente no seu navegador"

                        self.log_message(msg)

                        # Criar conteúdo para janela de resultado
                        title = f"Histórico de Cotações - {codigo}"
                        content = (
                            console_output
                            + "\n\n"
                            + self.show_dataframe_summary(df, f"Histórico de {codigo}")
                        )

                        self.log_message("🪟 Abrindo janela de resultado...")
                        # Exibir janela de resultado
                        self.show_result_window(title, content, df)

                    else:
                        error_msg = f"Nenhum dado encontrado para {codigo}"
                        if console_output:
                            error_msg += f"\nDetalhes: {console_output}"
                        self.log_message(error_msg)

                        # Mensagem mais informativa baseada no console output
                        if "Nenhuma cotação encontrada" in console_output:
                            messagebox.showwarning(
                                "Dados Não Encontrados",
                                f"Nenhuma cotação encontrada para {codigo}.\n\n"
                                f"O ativo existe na base, mas não há dados de cotação.\n\n"
                                f"Soluções:\n"
                                f"1. Execute 'Coletar Dados B3' para obter cotações atualizadas\n"
                                f"2. Verifique se o código está correto\n"
                                f"3. Alguns ativos podem não ter cotações recentes",
                            )
                        elif "Tente um período maior" in console_output:
                            messagebox.showwarning(
                                "Período Insuficiente",
                                f"Nenhum dado encontrado para {codigo} no período especificado.\n\n"
                                f"O ativo tem cotações, mas não no período solicitado.\n\n"
                                f"Soluções:\n"
                                f"1. Aumente o período (ex: 90 ou 180 dias)\n"
                                f"2. Verifique as datas no console para mais detalhes\n"
                                f"3. Execute 'Coletar Dados B3' para dados mais recentes",
                            )
                        else:
                            messagebox.showwarning(
                                "Aviso",
                                f"Nenhum dado encontrado para {codigo}.\n\n"
                                f"Verifique se:\n"
                                f"1. O código está correto\n"
                                f"2. Há dados de cotação para este ativo\n"
                                f"3. O período não é muito antigo\n\n"
                                f"Execute 'Coletar Dados B3' se necessário.",
                            )
                else:
                    self.log_message(
                        "Operacao cancelada pelo usuario - sem resultado do dialogo"
                    )

            except Exception as e:
                error_msg = f"Erro no histórico de cotações: {e}"
                self.log_message(f"{error_msg}")
                messagebox.showerror("Erro", error_msg)

        self.run_in_thread(execute)

    def relatorio_dividendos(self):
        """Handler para relatório de dividendos"""

        def execute():
            try:
                # DIAGNOSTICO: Verificar se ha dados de dividendos no banco
                self.log_message("=== DIAGNOSTICO DE DIVIDENDOS ===")

                # Verificar total de dividendos
                count_query = "SELECT COUNT(*) as total FROM dividendos"
                count_df = self.data_workflow.db_manager.execute_query(count_query)
                total_dividendos = (
                    count_df.iloc[0]["total"] if not count_df.empty else 0
                )
                self.log_message(f"Total de dividendos no banco: {total_dividendos}")

                if total_dividendos == 0:
                    self.log_message("PROBLEMA: Nenhum dividendo no banco de dados!")
                    self.log_message(
                        "SOLUCAO: Execute 'Coletar Dados B3' para inserir dados de dividendos"
                    )

                    messagebox.showwarning(
                        "Sem Dados de Dividendos",
                        "Nenhum dividendo encontrado no banco de dados.\n\n"
                        + "Para ter dados de dividendos:\n"
                        + "1. Execute 'Coletar Dados B3 (D-1)'\n"
                        + "2. Aguarde a coleta completa\n"
                        + "3. Tente novamente o relatório de dividendos\n\n"
                        + "Nota: Os dados de dividendos são exemplos simulados incluídos na coleta.",
                    )
                    return
                else:
                    # Mostrar amostra dos dados
                    sample_query = "SELECT a.codigo, d.data, d.valor, d.tipo FROM dividendos d JOIN ativos a ON d.id_ativo = a.id LIMIT 5"
                    sample_df = self.data_workflow.db_manager.execute_query(
                        sample_query
                    )
                    self.log_message("Amostra de dividendos no banco:")
                    for _, row in sample_df.iterrows():
                        self.log_message(
                            f"  {row['codigo']}: R$ {row['valor']:.2f} em {row['data']} ({row['tipo']})"
                        )

                # Criar janela de filtros para dividendos
                dialog = DividendsFilterDialog(self.root)

                if dialog.result:
                    codigo = dialog.result.get("codigo")
                    ano = dialog.result.get("ano")
                    trimestre = dialog.result.get("trimestre")
                    gerar_grafico = dialog.result.get("gerar_grafico", True)

                    self.log_message(f"Gerando relatório de dividendos...")
                    if codigo:
                        self.log_message(f"Ativo: {codigo}")
                    if ano:
                        self.log_message(f"Ano: {ano}")
                    if trimestre:
                        self.log_message(f"Trimestre: {trimestre}º")

                    # Capturar saída do console
                    with self.capture_output() as output:
                        df = self.reports_workflow.execute_relatorio_dividendos(
                            codigo, ano, trimestre, gerar_grafico
                        )

                    console_output = output.getvalue()

                    if df is not None and not df.empty:
                        msg = f"Relatorio de dividendos gerado! ({len(df)} registros encontrados)"
                        if gerar_grafico:
                            import os

                            graph_path = os.path.abspath("dividendos_mensal.html")
                            msg += f"\nGrafico salvo como 'dividendos_mensal.html'"
                            msg += f"\nLocal: {graph_path}"
                            msg += f"\nO grafico deve abrir automaticamente no seu navegador"

                        self.log_message(msg)

                        # Criar conteúdo para janela de resultado
                        title = "Relatório de Dividendos"
                        if codigo:
                            title += f" - {codigo}"
                        if ano:
                            title += f" ({ano})"

                        content = (
                            console_output
                            + "\n\n"
                            + self.show_dataframe_summary(df, "Dividendos")
                        )

                        # Exibir janela de resultado
                        self.show_result_window(title, content, df)

                    else:
                        error_msg = (
                            "Nenhum dividendo encontrado com os filtros especificados"
                        )
                        self.log_message(error_msg)

                        # Mensagem mais informativa
                        aviso_msg = "Nenhum dividendo encontrado com os filtros especificados.\n\n"
                        aviso_msg += "Possiveis causas:\n"
                        aviso_msg += "• Os filtros sao muito restritivos\n"
                        aviso_msg += "• O ativo especificado nao paga dividendos\n"
                        aviso_msg += "• O periodo especificado nao tem dados\n\n"
                        aviso_msg += "Tente:\n"
                        aviso_msg += "• Relatorio sem filtros (deixe campos vazios)\n"
                        aviso_msg += "• Apenas filtro por ano (ex: 2024)\n"
                        aviso_msg += "• Codigos que pagam dividendos: HGLG11, XPML11, ITUB4, PETR4"

                        messagebox.showwarning("Aviso", aviso_msg)
                else:
                    self.log_message("Operação cancelada pelo usuário")

            except Exception as e:
                error_msg = f"Erro no relatório de dividendos: {e}"
                self.log_message(f"{error_msg}")
                messagebox.showerror("Erro", error_msg)

        self.run_in_thread(execute)

    def coletar_dados(self):
        """Handler para coleta de dados B3"""

        def execute():
            try:
                confirm = messagebox.askyesno(
                    "Coleta de Dados B3",
                    "Deseja iniciar a coleta de dados do dia anterior (D-1)?\n\nEsta operação pode demorar alguns minutos.",
                    parent=self.root,
                )

                if not confirm:
                    self.log_message("Coleta de dados cancelada pelo usuário")
                    return

                self.log_message("Iniciando coleta de dados B3 (D-1)...")
                self.log_message("Aguarde... Esta operação pode demorar alguns minutos")

                success = self.data_workflow.execute()

                if success:
                    msg = "Coleta de dados concluída com sucesso!"
                    self.log_message(msg)
                    messagebox.showinfo("Sucesso", msg)
                else:
                    error_msg = "Falha na coleta de dados"
                    self.log_message(error_msg)
                    messagebox.showerror(
                        "Erro",
                        "Falha na coleta de dados. Verifique o log para detalhes.",
                    )

            except Exception as e:
                error_msg = f"Erro na coleta de dados: {e}"
                self.log_message(f"{error_msg}")
                messagebox.showerror("Erro", error_msg)

        self.run_in_thread(execute)

    def coletar_historico(self):
        """Handler para coleta de dados históricos"""

        def execute():
            try:
                confirm = messagebox.askyesno(
                    "Coleta de Dados Históricos",
                    "Deseja gerar dados históricos simulados para os últimos 30 dias?\n\n"
                    "Esta operação irá:\n"
                    "• Coletar dados atuais da B3\n"
                    "• Gerar dados históricos simulados\n"
                    "• Permitir gráficos com mais dados\n\n"
                    "Pode demorar alguns minutos.",
                    parent=self.root,
                )

                if not confirm:
                    self.log_message(
                        "Coleta de dados históricos cancelada pelo usuário"
                    )
                    return

                self.log_message("Iniciando coleta de dados históricos...")
                self.log_message("Gerando 30 dias de dados simulados...")

                # Importar e usar o collector
                from data_collector import B3DataCollector
                from database_manager import DatabaseManager

                collector = B3DataCollector()
                db_manager = DatabaseManager()

                # Coletar dados históricos
                df_cotacoes, df_ativos, df_dividendos = (
                    collector.collect_historical_data(30)
                )

                if df_cotacoes is not None and not df_cotacoes.empty:
                    self.log_message(
                        f"Coletados {len(df_cotacoes)} registros historicos"
                    )

                    # Inserir ativos primeiro
                    if df_ativos is not None and not df_ativos.empty:
                        success_ativos = db_manager.sync_ativos(df_ativos)
                        self.log_message(f"Ativos sincronizados: {success_ativos}")

                    # CORREÇÃO: Mapear id_ativo antes de inserir cotações
                    if "id_ativo" not in df_cotacoes.columns:
                        self.log_message("Mapeando IDs dos ativos...")

                        # Buscar mapeamento código -> id
                        ativos_db = db_manager.get_existing_ativos()
                        codigo_to_id = dict(zip(ativos_db["codigo"], ativos_db["id"]))

                        # Mapear id_ativo usando o código
                        df_cotacoes["id_ativo"] = df_cotacoes["codigo"].map(
                            codigo_to_id
                        )

                        # Remover registros sem mapeamento
                        df_cotacoes = df_cotacoes.dropna(subset=["id_ativo"])
                        df_cotacoes["id_ativo"] = df_cotacoes["id_ativo"].astype(int)

                        self.log_message(
                            f"{len(df_cotacoes)} registros com IDs mapeados"
                        )

                    # Inserir cotações históricas (usar data fictícia para não sobrescrever)
                    from datetime import datetime, timedelta

                    data_base = datetime.now().date() - timedelta(days=15)
                    success_cotacoes = db_manager.insert_cotacoes(
                        df_cotacoes, data_base
                    )

                    if success_cotacoes:
                        msg = (
                            f"Dados historicos inseridos com sucesso!\n\n"
                            f"{len(df_cotacoes)} cotacoes historicas\n"
                            f"30 dias de dados simulados\n"
                            f"Agora voce pode gerar graficos com mais dados!"
                        )

                        self.log_message("Dados historicos coletados com sucesso!")
                        messagebox.showinfo("Sucesso", msg)
                    else:
                        error_msg = "Erro ao inserir dados historicos no banco"
                        self.log_message(error_msg)
                        messagebox.showerror("Erro", error_msg)
                else:
                    error_msg = "Falha na geracao de dados historicos"
                    self.log_message(error_msg)
                    messagebox.showerror("Erro", error_msg)

            except Exception as e:
                error_msg = f"Erro na coleta de dados históricos: {e}"
                self.log_message(f"{error_msg}")
                messagebox.showerror("Erro", error_msg)

        self.run_in_thread(execute)

    def resumo_sistema(self):
        """Handler para resumo do sistema"""

        def execute():
            try:
                self.log_message("Gerando resumo do sistema...")

                # Capturar saída do console
                with self.capture_output() as output:
                    success = self.reports_workflow.execute_resumo_sistema()

                console_output = output.getvalue()

                if success:
                    msg = "Resumo do sistema gerado!"
                    self.log_message(msg)

                    # Criar conteúdo para janela de resultado
                    title = "Resumo do Sistema"
                    content = console_output

                    # Exibir janela de resultado
                    self.show_result_window(title, content)

                else:
                    error_msg = "Erro ao gerar resumo do sistema"
                    self.log_message(error_msg)
                    messagebox.showerror("Erro", "Erro ao gerar resumo do sistema")

            except Exception as e:
                error_msg = f"Erro no resumo do sistema: {e}"
                self.log_message(f"{error_msg}")
                messagebox.showerror("Erro", error_msg)

        self.run_in_thread(execute)

    def todos_relatorios(self):
        """Handler para executar todos os relatórios"""

        def execute():
            try:
                confirm = messagebox.askyesno(
                    "Executar Todos os Relatórios",
                    "Deseja executar todos os relatórios disponíveis?\n\nEsta operação pode demorar alguns minutos.",
                    parent=self.root,
                )

                if not confirm:
                    self.log_message("Execução cancelada pelo usuário")
                    return

                self.log_message("Executando todos os relatórios...")
                self.log_message("Aguarde... Esta operação pode demorar alguns minutos")

                # Capturar saída do console
                with self.capture_output() as output:
                    success = self.reports_workflow.execute_all_reports()

                console_output = output.getvalue()

                if success:
                    msg = "Todos os relatórios foram executados com sucesso!"
                    self.log_message(msg)

                    # Criar conteúdo para janela de resultado
                    title = "Execução de Todos os Relatórios"
                    content = console_output

                    # Exibir janela de resultado
                    self.show_result_window(title, content)

                else:
                    error_msg = "Falha na execução dos relatórios"
                    self.log_message(error_msg)
                    messagebox.showerror("Erro", "Falha na execução dos relatórios")

            except Exception as e:
                error_msg = f"Erro ao executar relatórios: {e}"
                self.log_message(f"{error_msg}")
                messagebox.showerror("Erro", error_msg)

        self.run_in_thread(execute)

    def run(self):
        """Executar interface gráfica"""
        self.root.mainloop()


class FilterDialog:
    """Diálogo para filtros de consulta de ativos"""

    def __init__(self, parent, title):
        self.result = None
        self.parent = parent

        # Criar janela
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("450x320")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Centralizar na tela
        self.dialog.geometry(
            "+%d+%d" % (parent.winfo_rootx() + 200, parent.winfo_rooty() + 100)
        )

        # Garantir que o diálogo espere antes de ser destruído
        self.dialog.protocol("WM_DELETE_WINDOW", self.cancel_clicked)

        self.setup_dialog()

        # Aguardar até que o diálogo seja fechado
        self.dialog.wait_window()

    def setup_dialog(self):
        """Configurar diálogo"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        title_label = ttk.Label(
            main_frame, text="Filtros para Consulta", font=("Arial", 12, "bold")
        )
        title_label.pack(pady=(0, 15))

        # Tipo
        ttk.Label(main_frame, text="Filtrar por Tipo:").pack(anchor=tk.W, pady=(0, 5))
        self.tipo_var = tk.StringVar()
        self.tipo_combo = ttk.Combobox(
            main_frame,
            textvariable=self.tipo_var,
            values=["", "ACAO", "FII", "ETF", "BDR"],
            state="readonly",
        )
        self.tipo_combo.pack(fill=tk.X, pady=(0, 15))
        self.tipo_combo.set("")

        # Bind para atualizar setores quando tipo mudar
        self.tipo_combo.bind("<<ComboboxSelected>>", self.on_tipo_changed)

        # Setor
        ttk.Label(main_frame, text="Filtrar por Setor:").pack(anchor=tk.W, pady=(0, 5))
        self.setor_var = tk.StringVar()
        self.setor_combo = ttk.Combobox(
            main_frame, textvariable=self.setor_var, state="readonly"
        )
        self.setor_combo.pack(fill=tk.X, pady=(0, 15))

        # Info label
        self.info_label = ttk.Label(
            main_frame,
            text="Selecione um tipo para filtrar setores disponíveis",
            font=("Arial", 9),
            foreground="gray",
        )
        self.info_label.pack(pady=(0, 15))

        # Carregar setores iniciais (todos) - DEPOIS de criar info_label
        self.load_setores()

        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)

        ttk.Button(button_frame, text="Consultar", command=self.ok_clicked).pack(
            side=tk.RIGHT, padx=(5, 0)
        )

        ttk.Button(button_frame, text="Cancelar", command=self.cancel_clicked).pack(
            side=tk.RIGHT
        )

    def load_setores(self, tipo_filtro=None):
        """Carrega setores disponíveis baseado no tipo selecionado"""
        try:
            from database_manager import DatabaseManager
            import pandas as pd

            db = DatabaseManager()

            # Primeiro verificar se há dados na tabela
            count_query = "SELECT COUNT(*) as total FROM ativos"
            count_df = pd.read_sql(count_query, db.engine)
            total_ativos = count_df.iloc[0]["total"]

            if total_ativos == 0:
                self.setor_combo["values"] = [""]
                self.info_label.config(
                    text="Nenhum ativo encontrado no banco. Execute a coleta de dados primeiro."
                )
                self.setor_combo.set("")
                return

            # Query para buscar setores
            if tipo_filtro:
                query = "SELECT DISTINCT setor FROM ativos WHERE tipo = %s AND setor IS NOT NULL AND setor != '' ORDER BY setor"
                df = pd.read_sql(query, db.engine, params=(tipo_filtro,))
            else:
                query = "SELECT DISTINCT setor FROM ativos WHERE setor IS NOT NULL AND setor != '' ORDER BY setor"
                df = pd.read_sql(query, db.engine)

            # Atualizar combo de setores
            if not df.empty:
                setores = [""] + df["setor"].tolist()  # Adicionar opção vazia
                self.setor_combo["values"] = setores

                # Atualizar info label
                if tipo_filtro:
                    self.info_label.config(
                        text=f"{len(df)} setores encontrados para {tipo_filtro}"
                    )
                else:
                    self.info_label.config(
                        text=f"{len(df)} setores disponíveis no total"
                    )
            else:
                self.setor_combo["values"] = [""]
                if tipo_filtro:
                    self.info_label.config(
                        text=f"Nenhum setor encontrado para {tipo_filtro}"
                    )
                else:
                    self.info_label.config(text="Dados sem informação de setor")

            # Resetar seleção
            self.setor_combo.set("")

        except Exception as e:
            print(f"Erro detalhado ao carregar setores: {e}")
            import traceback

            traceback.print_exc()
            self.setor_combo["values"] = [""]
            self.info_label.config(text=f"Erro ao carregar setores")

    def on_tipo_changed(self, event=None):
        """Handler para mudança de tipo"""
        tipo_selecionado = self.tipo_var.get()
        if tipo_selecionado:
            self.load_setores(tipo_selecionado)
        else:
            self.load_setores()  # Carregar todos os setores

    def ok_clicked(self):
        """Handler para botão OK"""
        self.result = {
            "tipo": self.tipo_var.get() if self.tipo_var.get() else None,
            "setor": self.setor_var.get() if self.setor_var.get() else None,
        }
        self.dialog.destroy()

    def cancel_clicked(self):
        """Handler para botão Cancelar"""
        self.result = None
        self.dialog.destroy()


class DividendsFilterDialog:
    """Diálogo para filtros de dividendos"""

    def __init__(self, parent):
        self.result = None

        # Criar janela
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Relatório de Dividendos")
        self.dialog.geometry("480x380")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Centralizar na tela
        self.dialog.geometry(
            "+%d+%d" % (parent.winfo_rootx() + 200, parent.winfo_rooty() + 100)
        )

        # Garantir que o diálogo espere antes de ser destruído
        self.dialog.protocol("WM_DELETE_WINDOW", self.cancel_clicked)

        self.setup_dialog()

        # Aguardar até que o diálogo seja fechado
        self.dialog.wait_window()

    def setup_dialog(self):
        """Configurar diálogo"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        title_label = ttk.Label(
            main_frame,
            text="Relatório de Dividendos",
            font=("Arial", 14, "bold"),
        )
        title_label.pack(pady=(0, 20))

        # Seleção de Ativo
        ativo_frame = ttk.LabelFrame(main_frame, text="Selecionar Ativo", padding="10")
        ativo_frame.pack(fill=tk.X, pady=(0, 15))

        # Frame para código e botão
        codigo_frame = ttk.Frame(ativo_frame)
        codigo_frame.pack(fill=tk.X, pady=(5, 0))

        ttk.Label(codigo_frame, text="Código do Ativo:").pack(anchor=tk.W, pady=(0, 5))

        # Combobox com lista de ativos
        self.codigo_var = tk.StringVar()
        self.codigo_combo = ttk.Combobox(
            codigo_frame,
            textvariable=self.codigo_var,
            state="normal",  # Permite digitação e seleção
        )
        self.codigo_combo.pack(fill=tk.X, pady=(0, 5))

        # Carregar lista apenas quando necessário (lazy loading)
        self.codigo_combo.bind("<Button-1>", self.on_combo_click)
        self.codigo_combo.bind("<Down>", self.on_combo_click)

        # Inicializar com sugestões básicas de ativos com dividendos
        self.codigo_combo["values"] = ["", "HGLG11", "XPML11", "ITUB4", "PETR4"]

        # Sugestões
        suggestion_label = ttk.Label(
            ativo_frame,
            text="Apenas ativos com dividendos serão listados",
            font=("Arial", 8),
            foreground="gray",
        )
        suggestion_label.pack(anchor=tk.W, pady=(5, 0))

        # Seleção de Período
        periodo_frame = ttk.LabelFrame(
            main_frame, text="Selecionar Período", padding="10"
        )
        periodo_frame.pack(fill=tk.X, pady=(0, 15))

        # Ano e Trimestre lado a lado
        periodo_controls_frame = ttk.Frame(periodo_frame)
        periodo_controls_frame.pack(fill=tk.X, pady=(5, 0))

        # Ano
        ano_frame = ttk.Frame(periodo_controls_frame)
        ano_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        ttk.Label(ano_frame, text="Ano:").pack(anchor=tk.W, pady=(0, 5))
        self.ano_var = tk.StringVar()
        ano_combo = ttk.Combobox(ano_frame, textvariable=self.ano_var, state="readonly")

        # Gerar anos dinamicamente baseado nos dados disponíveis
        try:
            from database_manager import DatabaseManager

            db_manager = DatabaseManager()

            # Buscar todos os anos que têm dividendos no banco
            query_anos = """
                SELECT DISTINCT EXTRACT(YEAR FROM data_com) as ano
                FROM dividendos 
                WHERE data_com IS NOT NULL
                ORDER BY ano DESC
            """
            df_anos = db_manager.execute_query(query_anos)

            if not df_anos.empty:
                anos_disponiveis = [
                    str(int(row["ano"])) for _, row in df_anos.iterrows()
                ]
                anos = ["Todos"] + anos_disponiveis
                print(
                    f"Carregados {len(anos_disponiveis)} anos com dividendos: {', '.join(anos_disponiveis)}"
                )
            else:
                # Fallback se não há dados
                from datetime import datetime

                ano_atual = datetime.now().year
                anos = ["Todos"] + [str(ano) for ano in range(2020, ano_atual + 2)]
                print("Nenhum ano com dividendos encontrado, usando anos padrão")

        except Exception as e:
            # Fallback em caso de erro
            print(f"Erro ao carregar anos: {e}")
            from datetime import datetime

            ano_atual = datetime.now().year
            anos = ["Todos"] + [str(ano) for ano in range(2020, ano_atual + 2)]

        ano_combo["values"] = anos
        ano_combo.set("Todos")
        ano_combo.pack(fill=tk.X)

        # Trimestre
        trimestre_frame = ttk.Frame(periodo_controls_frame)
        trimestre_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(trimestre_frame, text="Trimestre:").pack(anchor=tk.W, pady=(0, 5))
        self.trimestre_var = tk.StringVar()
        trimestre_combo = ttk.Combobox(
            trimestre_frame,
            textvariable=self.trimestre_var,
            state="readonly",
        )
        trimestre_combo["values"] = [
            "Todos",
            "1º Trimestre (Jan-Mar)",
            "2º Trimestre (Abr-Jun)",
            "3º Trimestre (Jul-Set)",
            "4º Trimestre (Out-Dez)",
        ]
        trimestre_combo.set("Todos")
        trimestre_combo.pack(fill=tk.X)

        # Botões com texto visível
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(25, 10))

        # Botão Cancelar (esquerda)
        cancel_btn = tk.Button(
            button_frame,
            text="Cancelar",
            command=self.cancel_clicked,
            width=12,
            height=1,
            font=("Arial", 9),
        )
        cancel_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Botão Gerar Relatório (direita)
        generate_btn = tk.Button(
            button_frame,
            text="Gerar Relatorio",
            command=self.ok_clicked,
            width=15,
            height=1,
            font=("Arial", 9),
        )
        generate_btn.pack(side=tk.RIGHT)

    def on_combo_click(self, event=None):
        """Carrega lista completa apenas quando usuário clica no combo"""
        # Carregar apenas se ainda não foi carregado
        if not hasattr(self, "_ativos_loaded"):
            self.load_ativos_list()
            self._ativos_loaded = True

    def load_ativos_list(self):
        """Carrega lista de ativos no combobox - apenas ativos com dividendos"""
        try:
            # Cache simples - se já carregou uma vez, não recarrega
            if hasattr(self, "_ativos_cache") and self._ativos_cache:
                self.codigo_combo["values"] = self._ativos_cache
                return

            # Importar a classe aqui para evitar referência circular
            from database_manager import DatabaseManager

            db_manager = DatabaseManager()

            # Query otimizada - buscar apenas ativos que TÊM dividendos
            query = """
                SELECT DISTINCT a.codigo, a.nome, COUNT(d.id) as total_dividendos
                FROM ativos a
                INNER JOIN dividendos d ON a.id = d.id_ativo
                WHERE a.codigo IS NOT NULL AND a.codigo != ''
                GROUP BY a.codigo, a.nome
                HAVING COUNT(d.id) > 0
                ORDER BY a.codigo
                LIMIT 100
            """
            df_ativos = db_manager.execute_query(query)

            if df_ativos.empty:
                # Se não há dados de dividendos, usar apenas as sugestões conhecidas
                ativos_list = ["", "HGLG11", "XPML11", "ITUB4", "PETR4"]
                self.codigo_combo["values"] = ativos_list
                self._ativos_cache = ativos_list
                return
            else:
                # Criar lista apenas com códigos de ativos que têm dividendos
                ativos_list = [""] + [
                    f"{row['codigo']}" for _, row in df_ativos.iterrows()
                ]

            # Salvar no cache
            self._ativos_cache = ativos_list

            # Configurar o combobox
            self.codigo_combo["values"] = ativos_list

            # Bind simplificado - não precisa extrair código
            self.codigo_combo.bind("<<ComboboxSelected>>", self.on_ativo_selected)

            # Log para debug
            print(f"Carregados {len(ativos_list)-1} ativos com dividendos")

        except Exception as e:
            # Em caso de erro, usar apenas as sugestões conhecidas
            print(f"Erro ao carregar ativos: {e}")
            ativos_list = ["", "HGLG11", "XPML11", "ITUB4", "PETR4"]
            self.codigo_combo["values"] = ativos_list
            self._ativos_cache = ativos_list

    def on_ativo_selected(self, event=None):
        """Handler otimizado quando um ativo é selecionado no combobox"""
        selected = self.codigo_combo.get()
        # Como agora só temos códigos, não precisa processar
        if selected and selected.strip():
            self.codigo_var.set(selected.strip().upper())

    def ok_clicked(self):
        """Handler para botão OK"""
        # Código do ativo
        codigo = (
            self.codigo_var.get().strip().upper()
            if self.codigo_var.get().strip()
            else None
        )

        # Ano
        ano_str = self.ano_var.get().strip()
        ano = None
        if ano_str and ano_str != "Todos":
            try:
                ano = int(ano_str)
            except ValueError:
                pass

        # Trimestre
        trimestre_str = self.trimestre_var.get().strip()
        trimestre = None
        if trimestre_str and trimestre_str != "Todos":
            if "1º" in trimestre_str:
                trimestre = 1
            elif "2º" in trimestre_str:
                trimestre = 2
            elif "3º" in trimestre_str:
                trimestre = 3
            elif "4º" in trimestre_str:
                trimestre = 4

        # Gerar gráfico (sempre True)
        gerar_grafico = True

        self.result = {
            "codigo": codigo,
            "ano": ano,
            "trimestre": trimestre,
            "gerar_grafico": gerar_grafico,
        }
        self.dialog.destroy()

    def cancel_clicked(self):
        """Handler para botão Cancelar"""
        self.result = None
        self.dialog.destroy()


class AssetSelectionDialog:
    """Diálogo para seleção de ativo"""

    def __init__(self, parent, db_manager):
        self.result = None
        self.db = db_manager
        self.current_selected_code = None  # Inicializar código selecionado

        # Criar janela
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Seleção de Ativo para Histórico")
        self.dialog.geometry("500x500")  # Aumentar altura para nova interface
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Centralizar na tela
        self.dialog.geometry(
            "+%d+%d" % (parent.winfo_rootx() + 200, parent.winfo_rooty() + 100)
        )

        # Garantir que o diálogo espere antes de ser destruído
        self.dialog.protocol("WM_DELETE_WINDOW", self.cancel_clicked)

        self.setup_dialog()

        # Aguardar até que o diálogo seja fechado
        self.dialog.wait_window()

    def setup_dialog(self):
        """Configurar diálogo"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        title_label = ttk.Label(
            main_frame,
            text="Selecionar Ativo para Histórico",
            font=("Arial", 12, "bold"),
        )
        title_label.pack(pady=(0, 10))

        # Instrução
        instruction_label = ttk.Label(
            main_frame,
            text="⚠️ Se a lista estiver vazia, execute 'Coletar Dados B3' primeiro na tela principal",
            font=("Arial", 9),
            foreground="orange",
            wraplength=450,
        )
        instruction_label.pack(pady=(0, 15))

        # Campo de busca
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(search_frame, text="Buscar ativo:").pack(anchor=tk.W, pady=(0, 5))

        search_input_frame = ttk.Frame(search_frame)
        search_input_frame.pack(fill=tk.X)

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_input_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        search_entry.bind("<KeyRelease>", self.on_search_change)
        search_entry.bind(
            "<Return>", self.on_search_change
        )  # Buscar ao pressionar Enter

        ttk.Button(
            search_input_frame,
            text="Buscar",
            command=self.on_search_change,
            width=10,
        ).pack(side=tk.RIGHT, padx=(0, 5))
        ttk.Button(
            search_input_frame, text="Limpar", command=self.clear_search, width=10
        ).pack(side=tk.RIGHT)

        # Lista de ativos
        ttk.Label(main_frame, text="Selecione o ativo:").pack(anchor=tk.W, pady=(10, 5))

        # Frame para listbox com scrollbar
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        self.listbox = tk.Listbox(list_frame, height=8)
        scrollbar = ttk.Scrollbar(
            list_frame, orient=tk.VERTICAL, command=self.listbox.yview
        )
        self.listbox.configure(yscrollcommand=scrollbar.set)

        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Frame para seleção e configurações
        config_frame = ttk.LabelFrame(
            main_frame, text="Configurações do Histórico", padding="10"
        )
        config_frame.pack(fill=tk.X, pady=(0, 15))

        # Ativo selecionado
        selected_frame = ttk.Frame(config_frame)
        selected_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(selected_frame, text="Ativo selecionado:").pack(side=tk.LEFT)
        self.selected_asset_var = tk.StringVar(value="Nenhum ativo selecionado")
        self.selected_label = ttk.Label(
            selected_frame,
            textvariable=self.selected_asset_var,
            font=("Arial", 9, "bold"),
            foreground="blue",
        )
        self.selected_label.pack(side=tk.LEFT, padx=(10, 0))

        # Bind para atualizar seleção
        self.listbox.bind("<<ListboxSelect>>", self.on_asset_selected)

        # Período
        period_frame = ttk.Frame(config_frame)
        period_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(period_frame, text="Período (dias):").pack(side=tk.LEFT)
        self.periodo_var = tk.StringVar(value="30")
        periodo_entry = ttk.Entry(period_frame, textvariable=self.periodo_var, width=10)
        periodo_entry.pack(side=tk.LEFT, padx=(10, 0))

        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        # Botão Cancelar
        tk.Button(button_frame, text="Cancelar", command=self.cancel_clicked).pack(
            side=tk.LEFT
        )

        # Botão para buscar histórico
        tk.Button(button_frame, text="Buscar Historico", command=self.ok_clicked).pack(
            side=tk.RIGHT, padx=(5, 0)
        )

        # Botão para gerar gráfico
        tk.Button(
            button_frame, text="Gerar Grafico", command=self.gerar_grafico_clicked
        ).pack(side=tk.RIGHT, padx=(5, 0))

        # Carregar ativos
        self.load_assets()

    def load_assets(self, search_term=""):
        """Carrega lista de ativos"""
        try:
            print(f"DEBUG: load_assets chamado com search_term='{search_term}'")
            self.listbox.delete(0, tk.END)  # Limpar primeiro

            # Query mais simples e direta
            if search_term:
                query = """
                    SELECT codigo, nome, tipo 
                    FROM ativos 
                    WHERE codigo ILIKE %s OR nome ILIKE %s
                    ORDER BY codigo
                    LIMIT 50
                """
                search_pattern = f"%{search_term}%"
                print(f"DEBUG: Buscando '{search_term}' com pattern '{search_pattern}'")
                df = self.db.execute_query(query, [search_pattern, search_pattern])
            else:
                query = """
                    SELECT codigo, nome, tipo 
                    FROM ativos 
                    ORDER BY codigo
                    LIMIT 50
                """
                print("DEBUG: Carregando todos os ativos (primeiros 50)")
                df = self.db.execute_query(query)

            print(
                f"DEBUG: Query retornou {len(df) if df is not None else 'None'} registros"
            )

            if df is not None and not df.empty:
                print("DEBUG: Inserindo ativos na listbox...")
                for i, row in df.iterrows():
                    try:
                        codigo = str(row["codigo"]).strip()
                        nome = str(row["nome"]).strip()[:40]
                        tipo = str(row.get("tipo", "")).strip()

                        display_text = f"{codigo} - {nome}"
                        if tipo and tipo != "nan":
                            display_text += f" ({tipo})"

                        self.listbox.insert(tk.END, display_text)
                        if i < 3:  # Mostrar apenas os primeiros 3 no debug
                            print(f"DEBUG: Inserido: {display_text}")
                        elif i == 3:
                            print(f"DEBUG: ... e mais {len(df)-3} ativos")

                    except Exception as e:
                        print(f"DEBUG: Erro ao processar linha {i}: {e}")
                        continue

                print(f"DEBUG: Total inserido na listbox: {self.listbox.size()}")

            else:
                print("DEBUG: Nenhum resultado da query")
                if search_term:
                    self.listbox.insert(
                        tk.END, f"Nenhum ativo encontrado para '{search_term}'"
                    )
                    self.listbox.insert(tk.END, "Clique 'Limpar' para ver todos")
                else:
                    self.listbox.insert(tk.END, "Nenhum ativo no banco")
                    self.listbox.insert(tk.END, "Execute 'Coletar Dados B3' primeiro")

        except Exception as e:
            print(f"DEBUG: ERRO em load_assets: {e}")
            import traceback

            traceback.print_exc()

            self.listbox.delete(0, tk.END)
            self.listbox.insert(tk.END, "ERRO ao carregar ativos")
            self.listbox.insert(tk.END, f"Erro: {str(e)}")
            self.listbox.insert(tk.END, "Verifique o console para detalhes")

    def on_search_change(self, event=None):
        """Handler para mudança no campo de busca"""
        search_term = self.search_var.get().strip()
        self.load_assets(search_term)

    def clear_search(self):
        """Limpa o campo de busca e recarrega todos os ativos"""
        self.search_var.set("")
        self.load_assets("")

    def executar_historico_direto(self):
        """Método direto para executar histórico sem complicações"""
        print("DEBUG: executar_historico_direto - MÉTODO CHAMADO!")

        # Verificar se temos ativo selecionado
        if not hasattr(self, "current_selected_code") or not self.current_selected_code:
            print("DEBUG: Nenhum ativo selecionado")
            messagebox.showwarning("Aviso", "Selecione um ativo da lista primeiro")
            return

        codigo = self.current_selected_code
        periodo = (
            int(self.periodo_var.get()) if self.periodo_var.get().isdigit() else 30
        )
        gerar_grafico = self.grafico_var.get()

        print(f"DEBUG: Executando histórico para {codigo}, período {periodo}")

        # Criar resultado e fechar diálogo
        self.result = {
            "codigo": codigo,
            "periodo": periodo,
            "gerar_grafico": gerar_grafico,
        }

        print(f"DEBUG: Resultado criado: {self.result}")
        self.dialog.destroy()

    def test_button_click(self):
        """Método de teste para verificar se botões funcionam"""
        print("DEBUG: test_button_click - BOTÃO DE TESTE CLICADO!")

        # Verificar estado do botão principal
        button_state = self.buscar_button["state"]
        print(f"DEBUG: Estado do botão principal: {button_state}")

        # Verificar se temos ativo selecionado
        if hasattr(self, "current_selected_code"):
            print(f"DEBUG: Ativo selecionado: '{self.current_selected_code}'")
        else:
            print("DEBUG: Nenhum ativo selecionado")

        # Forçar chamada do método principal
        print("DEBUG: Chamando buscar_historico_clicked diretamente...")
        self.buscar_historico_clicked()

    def on_asset_selected(self, event=None):
        """Handler para quando um ativo é selecionado na lista"""
        print("DEBUG: on_asset_selected - EVENTO DISPARADO!")
        selection = self.listbox.curselection()
        print(f"DEBUG: Seleção: {selection}")

        if selection:
            selected_text = self.listbox.get(selection[0])
            print(f"DEBUG: Texto selecionado: '{selected_text}'")

            # Verificar se é uma mensagem de erro ou informativa
            if any(
                text in selected_text
                for text in [
                    "Nenhum ativo",
                    "Erro ao carregar",
                    "Execute 'Coletar Dados B3'",
                    "banco de dados",
                    "Detalhes:",
                ]
            ):
                print("DEBUG: Texto é mensagem de erro - ignorando")
                self.selected_asset_var.set("Nenhum ativo selecionado")
                return

            # Extrair código do ativo
            if " - " in selected_text:
                codigo = selected_text.split(" - ")[0].strip()
                nome_curto = (
                    selected_text.split(" - ")[1][:30] + "..."
                    if len(selected_text.split(" - ")[1]) > 30
                    else selected_text.split(" - ")[1]
                )

                print(f"DEBUG: Código extraído: '{codigo}'")
                print(f"DEBUG: Nome curto: '{nome_curto}'")

                self.selected_asset_var.set(f"{codigo} - {nome_curto}")
                self.current_selected_code = codigo
                print(f"DEBUG: Ativo selecionado salvo: '{self.current_selected_code}'")
                print("DEBUG: Ativo selecionado!")
            else:
                print("DEBUG: Formato inválido - sem ' - '")
                self.selected_asset_var.set("Ativo inválido selecionado")
        else:
            print("DEBUG: Nenhuma seleção")
            self.selected_asset_var.set("Nenhum ativo selecionado")

    def buscar_historico_clicked(self):
        """Handler para buscar histórico do ativo selecionado"""
        print("DEBUG: buscar_historico_clicked - MÉTODO CHAMADO!")

        if not hasattr(self, "current_selected_code") or not self.current_selected_code:
            print(
                f"DEBUG: Código não encontrado. hasattr: {hasattr(self, 'current_selected_code')}"
            )
            if hasattr(self, "current_selected_code"):
                print(f"DEBUG: Valor do código: '{self.current_selected_code}'")
            messagebox.showwarning("Aviso", "Selecione um ativo da lista primeiro")
            return

        print(f"DEBUG: Código selecionado: '{self.current_selected_code}'")

        # Validar período
        try:
            periodo = int(self.periodo_var.get())
            print(f"DEBUG: Período: {periodo}")
            if periodo <= 0 or periodo > 365:
                raise ValueError()
        except ValueError:
            print("DEBUG: Erro no período")
            messagebox.showerror("Erro", "Período deve ser um número entre 1 e 365")
            return

        # Confirmar ação
        confirm_msg = f"Buscar histórico de {self.current_selected_code} para os últimos {periodo} dias?"
        print(f"DEBUG: Mostrando confirmação: '{confirm_msg}'")

        if not messagebox.askyesno("Confirmar Busca", confirm_msg):
            print("DEBUG: Usuário cancelou na confirmação")
            return

        print("DEBUG: Usuário confirmou - criando resultado")
        self.result = {
            "codigo": self.current_selected_code,
            "periodo": periodo,
            "gerar_grafico": self.grafico_var.get(),
        }
        print(f"DEBUG: Resultado criado: {self.result}")
        print("DEBUG: Destruindo diálogo...")
        self.dialog.destroy()

    def ok_clicked(self):
        """Handler para botão OK - VERSÃO SIMPLES"""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um ativo da lista")
            return

        # Extrair código do ativo selecionado
        selected_text = self.listbox.get(selection[0])

        # Verificar se é uma mensagem de erro
        if "Nenhum ativo" in selected_text or "Erro" in selected_text:
            messagebox.showwarning("Aviso", "Selecione um ativo válido")
            return

        # Extrair código
        if " - " not in selected_text:
            messagebox.showwarning("Aviso", "Formato de ativo inválido")
            return

        codigo = selected_text.split(" - ")[0].strip()

        if not codigo:
            messagebox.showwarning("Aviso", "Código do ativo não encontrado")
            return

        # Validar período
        try:
            periodo = int(self.periodo_var.get())
            if periodo <= 0 or periodo > 365:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Erro", "Período deve ser um número entre 1 e 365")
            return

        self.result = {
            "codigo": codigo,
            "periodo": periodo,
            "gerar_grafico": False,
        }
        self.dialog.destroy()

    def gerar_grafico_clicked(self):
        """Handler para botão Gerar Gráfico"""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um ativo da lista")
            return

        # Extrair código do ativo selecionado
        selected_text = self.listbox.get(selection[0])

        # Verificar se é uma mensagem de erro
        if "Nenhum ativo" in selected_text or "Erro" in selected_text:
            messagebox.showwarning("Aviso", "Selecione um ativo válido")
            return

        # Extrair código
        if " - " not in selected_text:
            messagebox.showwarning("Aviso", "Formato de ativo inválido")
            return

        codigo = selected_text.split(" - ")[0].strip()

        if not codigo:
            messagebox.showwarning("Aviso", "Código do ativo não encontrado")
            return

        # Validar período
        try:
            periodo = int(self.periodo_var.get())
            if periodo <= 0 or periodo > 365:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Erro", "Período deve ser um número entre 1 e 365")
            return

        self.result = {
            "codigo": codigo,
            "periodo": periodo,
            "gerar_grafico": True,
        }
        self.dialog.destroy()

    def cancel_clicked(self):
        """Handler para botão Cancelar"""
        self.result = None
        self.dialog.destroy()


def main():
    """Função principal para executar a GUI"""
    try:
        app = B3SystemGUI()
        app.run()
    except Exception as e:
        logger.error(f"Erro fatal na interface gráfica: {e}")
        messagebox.showerror("Erro Fatal", f"Erro fatal na interface gráfica: {e}")


if __name__ == "__main__":
    main()
