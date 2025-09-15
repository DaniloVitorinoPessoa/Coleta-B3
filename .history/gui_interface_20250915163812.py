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
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
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
        self.style.theme_use('clam')
        
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
            main_frame, 
            text="Sistema de Análise B3", 
            font=('Arial', 18, 'bold')
        )
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Subtitle
        subtitle_label = ttk.Label(
            main_frame,
            text="Análise de dados financeiros com geração de gráficos interativos",
            font=('Arial', 10)
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 30))
        
        # Frame para operações do sistema (PRIMEIRO - mais importante)
        system_frame = ttk.LabelFrame(main_frame, text="🔧 Operações do Sistema (Execute Primeiro)", padding="15")
        system_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        system_frame.columnconfigure(0, weight=1)
        system_frame.columnconfigure(1, weight=1)
        
        btn_coleta = ttk.Button(
            system_frame,
            text=" Coletar Dados B3 (D-1)",
            command=self.coletar_dados,
            width=25
        )
        btn_coleta.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        btn_resumo = ttk.Button(
            system_frame,
            text=" Resumo do Sistema",
            command=self.resumo_sistema,
            width=25
        )
        btn_resumo.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Aviso importante
        aviso_label = ttk.Label(
            system_frame,
            text=" Execute 'Coletar Dados B3' primeiro para ter dados nos relatórios",
            font=('Arial', 9, 'italic'),
            foreground='orange'
        )
        aviso_label.grid(row=1, column=0, columnspan=2, pady=(5, 0))
        
        # Frame para relatórios e consultas (SEGUNDO - após ter dados)
        buttons_frame = ttk.LabelFrame(main_frame, text="📊 Relatórios e Consultas (Após Coletar Dados)", padding="15")
        buttons_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        
        # Botões de relatórios
        btn_ativos = ttk.Button(
            buttons_frame,
            text=" Consultar Ativos",
            command=self.consultar_ativos,
            width=25
        )
        btn_ativos.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        btn_cotacoes = ttk.Button(
            buttons_frame,
            text=" Histórico de Cotações",
            command=self.historico_cotacoes,
            width=25
        )
        btn_cotacoes.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        btn_dividendos = ttk.Button(
            buttons_frame,
            text=" Relatório de Dividendos",
            command=self.relatorio_dividendos,
            width=25
        )
        btn_dividendos.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        btn_alocacao = ttk.Button(
            buttons_frame,
            text=" Dashboard de Alocação",
            command=self.dashboard_alocacao,
            width=25
        )
        btn_alocacao.grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        btn_todos = ttk.Button(
            buttons_frame,
            text="🚀 Executar Todos os Relatórios",
            command=self.todos_relatorios,
            width=25
        )
        btn_todos.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Frame para log/status
        log_frame = ttk.LabelFrame(main_frame, text="Status e Log", padding="10")
        log_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Área de texto para log
        self.log_text = tk.Text(log_frame, height=10, wrap=tk.WORD, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Botão sair
        btn_sair = ttk.Button(
            main_frame,
            text="❌ Sair",
            command=self.root.quit,
            width=15
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
        title_label = ttk.Label(main_frame, text=title, font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # Notebook para abas
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Aba de texto
        text_frame = ttk.Frame(notebook)
        notebook.add(text_frame, text="📄 Relatório")
        
        # Área de texto com scroll
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=('Consolas', 10))
        text_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
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
            text="📋 Copiar Texto",
            command=lambda: self.copy_to_clipboard(content)
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            button_frame,
            text="❌ Fechar",
            command=result_window.destroy
        ).pack(side=tk.RIGHT)
        
        # Centralizar janela
        result_window.transient(self.root)
        result_window.grab_set()
        
        return result_window
    
    def create_data_table(self, parent, df):
        """Cria tabela para exibir DataFrame"""
        data_frame = ttk.Frame(parent)
        parent.add(data_frame, text="📊 Dados")
        
        # Criar Treeview
        columns = list(df.columns)
        tree = ttk.Treeview(data_frame, columns=columns, show='headings', height=20)
        
        # Configurar colunas
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor='center')
        
        # Inserir dados
        for index, row in df.iterrows():
            values = [str(val) if pd.notna(val) else "" for val in row.values]
            tree.insert('', tk.END, values=values)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(data_frame, orient=tk.VERTICAL, command=tree.yview)
        h_scrollbar = ttk.Scrollbar(data_frame, orient=tk.HORIZONTAL, command=tree.xview)
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
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            summary += "ESTATÍSTICAS:\n"
            summary += "=" * 50 + "\n"
            summary += df[numeric_cols].describe().to_string() + "\n"
        
        return summary
        
    def testar_conexao_inicial(self):
        """Testa conexão com o banco na inicialização"""
        self.log_message("🔌 Testando conexão com o banco de dados...")
        
        try:
            if self.data_workflow.db_manager.test_connection():
                self.log_message("✅ SUCESSO: Conectado ao banco de dados!")
            else:
                self.log_message("❌ ERRO: Não foi possível conectar ao banco")
                self.log_message("💡 Dica: Execute 'docker-compose up -d' para iniciar o PostgreSQL")
        except Exception as e:
            self.log_message(f"❌ ERRO na conexão: {e}")
    
    def run_in_thread(self, func):
        """Executa função em thread separada para não travar a interface"""
        thread = threading.Thread(target=func, daemon=True)
        thread.start()
    
    def consultar_ativos(self):
        """Handler para consulta de ativos"""
        def execute():
            try:
                self.log_message("📊 Iniciando consulta de ativos...")
                
                # Criar janela de filtros
                dialog = FilterDialog(self.root, "Filtros para Consulta de Ativos")
                
                if dialog.result:
                    filtro_tipo = dialog.result.get('tipo')
                    filtro_setor = dialog.result.get('setor')
                    
                    self.log_message(f"🔍 Aplicando filtros - Tipo: {filtro_tipo or 'Todos'}, Setor: {filtro_setor or 'Todos'}")
                    
                    # Capturar saída do console
                    with self.capture_output() as output:
                        df = self.reports_workflow.execute_consulta_ativos(filtro_tipo, filtro_setor)
                    
                    console_output = output.getvalue()
                    
                    if df is not None and not df.empty:
                        self.log_message(f"✅ Consulta concluída! {len(df)} ativos encontrados")
                        
                        # Criar conteúdo para janela de resultado
                        title = "📊 Consulta de Ativos"
                        content = console_output + "\n\n" + self.show_dataframe_summary(df, "Lista de Ativos")
                        
                        # Exibir janela de resultado
                        self.show_result_window(title, content, df)
                        
                    else:
                        self.log_message("⚠️ Nenhum ativo encontrado com os filtros especificados")
                        messagebox.showwarning("Aviso", "Nenhum ativo encontrado com os filtros especificados")
                else:
                    self.log_message("❌ Consulta cancelada pelo usuário")
                    
            except Exception as e:
                error_msg = f"Erro na consulta de ativos: {e}"
                self.log_message(f"❌ {error_msg}")
                messagebox.showerror("Erro", error_msg)
        
        self.run_in_thread(execute)
    
    def historico_cotacoes(self):
        """Handler para histórico de cotações"""
        def execute():
            try:
                # Solicitar código do ativo
                codigo = simpledialog.askstring(
                    "Histórico de Cotações",
                    "Digite o código do ativo (ex: PETR4):",
                    parent=self.root
                )
                
                if not codigo:
                    self.log_message("❌ Operação cancelada - código não informado")
                    return
                
                codigo = codigo.upper().strip()
                
                # Solicitar período
                periodo = simpledialog.askinteger(
                    "Período",
                    "Período em dias:",
                    initialvalue=30,
                    minvalue=1,
                    maxvalue=365,
                    parent=self.root
                )
                
                if not periodo:
                    periodo = 30
                
                # Perguntar sobre gráfico
                gerar_grafico = messagebox.askyesno(
                    "Gerar Gráfico",
                    "Deseja gerar gráfico de candlestick?",
                    parent=self.root
                )
                
                self.log_message(f"📈 Gerando histórico de cotações para {codigo} ({periodo} dias)...")
                
                # Capturar saída do console
                with self.capture_output() as output:
                    df = self.reports_workflow.execute_historico_cotacoes(codigo, periodo, gerar_grafico)
                
                console_output = output.getvalue()
                
                if df is not None:
                    msg = f"✅ Histórico gerado para {codigo}!"
                    if gerar_grafico:
                        msg += f"\n📊 Gráfico salvo como 'historico_{codigo}.html'"
                    
                    self.log_message(msg)
                    
                    # Criar conteúdo para janela de resultado
                    title = f"📈 Histórico de Cotações - {codigo}"
                    content = console_output + "\n\n" + self.show_dataframe_summary(df, f"Histórico de {codigo}")
                    
                    # Exibir janela de resultado
                    self.show_result_window(title, content, df)
                    
                else:
                    error_msg = f"❌ Nenhum dado encontrado para {codigo}"
                    self.log_message(error_msg)
                    messagebox.showwarning("Aviso", f"Nenhum dado encontrado para {codigo}")
                    
            except Exception as e:
                error_msg = f"Erro no histórico de cotações: {e}"
                self.log_message(f"❌ {error_msg}")
                messagebox.showerror("Erro", error_msg)
        
        self.run_in_thread(execute)
    
    def relatorio_dividendos(self):
        """Handler para relatório de dividendos"""
        def execute():
            try:
                # Criar janela de filtros para dividendos
                dialog = DividendsFilterDialog(self.root)
                
                if dialog.result:
                    codigo = dialog.result.get('codigo')
                    ano = dialog.result.get('ano')
                    gerar_grafico = dialog.result.get('gerar_grafico', True)
                    
                    self.log_message(f"💰 Gerando relatório de dividendos...")
                    if codigo:
                        self.log_message(f"🎯 Ativo: {codigo}")
                    if ano:
                        self.log_message(f"📅 Ano: {ano}")
                    
                    # Capturar saída do console
                    with self.capture_output() as output:
                        df = self.reports_workflow.execute_relatorio_dividendos(codigo, ano, gerar_grafico)
                    
                    console_output = output.getvalue()
                    
                    if df is not None:
                        msg = "✅ Relatório de dividendos gerado!"
                        if gerar_grafico:
                            msg += "\n📊 Gráfico salvo como 'dividendos_mensal.html'"
                        
                        self.log_message(msg)
                        
                        # Criar conteúdo para janela de resultado
                        title = "💰 Relatório de Dividendos"
                        if codigo:
                            title += f" - {codigo}"
                        if ano:
                            title += f" ({ano})"
                        
                        content = console_output + "\n\n" + self.show_dataframe_summary(df, "Dividendos")
                        
                        # Exibir janela de resultado
                        self.show_result_window(title, content, df)
                        
                    else:
                        error_msg = "❌ Nenhum dividendo encontrado"
                        self.log_message(error_msg)
                        messagebox.showwarning("Aviso", "Nenhum dividendo encontrado com os filtros especificados")
                else:
                    self.log_message("❌ Operação cancelada pelo usuário")
                    
            except Exception as e:
                error_msg = f"Erro no relatório de dividendos: {e}"
                self.log_message(f"❌ {error_msg}")
                messagebox.showerror("Erro", error_msg)
        
        self.run_in_thread(execute)
    
    def dashboard_alocacao(self):
        """Handler para dashboard de alocação"""
        def execute():
            try:
                gerar_graficos = messagebox.askyesno(
                    "Dashboard de Alocação",
                    "Deseja gerar gráficos interativos?",
                    parent=self.root
                )
                
                self.log_message("🎯 Gerando dashboard de alocação...")
                
                # Capturar saída do console
                with self.capture_output() as output:
                    df = self.reports_workflow.execute_dashboard_alocacao(gerar_graficos)
                
                console_output = output.getvalue()
                
                if df is not None:
                    msg = "✅ Dashboard de alocação gerado!"
                    if gerar_graficos:
                        msg += "\n📊 Gráficos salvos:\n- alocacao_setor.html\n- alocacao_tipo.html\n- rentabilidade_ativos.html"
                    
                    self.log_message(msg)
                    
                    # Criar conteúdo para janela de resultado
                    title = "🎯 Dashboard de Alocação da Carteira"
                    content = console_output + "\n\n" + self.show_dataframe_summary(df, "Carteira de Investimentos")
                    
                    # Exibir janela de resultado
                    self.show_result_window(title, content, df)
                    
                else:
                    error_msg = "❌ Carteira vazia ou erro na geração"
                    self.log_message(error_msg)
                    messagebox.showwarning("Aviso", "Carteira vazia ou erro na geração do dashboard")
                    
            except Exception as e:
                error_msg = f"Erro no dashboard de alocação: {e}"
                self.log_message(f"❌ {error_msg}")
                messagebox.showerror("Erro", error_msg)
        
        self.run_in_thread(execute)
    
    def coletar_dados(self):
        """Handler para coleta de dados B3"""
        def execute():
            try:
                confirm = messagebox.askyesno(
                    "Coleta de Dados B3",
                    "Deseja iniciar a coleta de dados do dia anterior (D-1)?\n\nEsta operação pode demorar alguns minutos.",
                    parent=self.root
                )
                
                if not confirm:
                    self.log_message("❌ Coleta de dados cancelada pelo usuário")
                    return
                
                self.log_message("🔄 Iniciando coleta de dados B3 (D-1)...")
                self.log_message("⏳ Aguarde... Esta operação pode demorar alguns minutos")
                
                success = self.data_workflow.execute()
                
                if success:
                    msg = "✅ Coleta de dados concluída com sucesso!"
                    self.log_message(msg)
                    messagebox.showinfo("Sucesso", msg)
                else:
                    error_msg = "❌ Falha na coleta de dados"
                    self.log_message(error_msg)
                    messagebox.showerror("Erro", "Falha na coleta de dados. Verifique o log para detalhes.")
                    
            except Exception as e:
                error_msg = f"Erro na coleta de dados: {e}"
                self.log_message(f"❌ {error_msg}")
                messagebox.showerror("Erro", error_msg)
        
        self.run_in_thread(execute)
    
    def resumo_sistema(self):
        """Handler para resumo do sistema"""
        def execute():
            try:
                self.log_message("📋 Gerando resumo do sistema...")
                
                # Capturar saída do console
                with self.capture_output() as output:
                    success = self.reports_workflow.execute_resumo_sistema()
                
                console_output = output.getvalue()
                
                if success:
                    msg = "✅ Resumo do sistema gerado!"
                    self.log_message(msg)
                    
                    # Criar conteúdo para janela de resultado
                    title = "📋 Resumo do Sistema"
                    content = console_output
                    
                    # Exibir janela de resultado
                    self.show_result_window(title, content)
                    
                else:
                    error_msg = "❌ Erro ao gerar resumo do sistema"
                    self.log_message(error_msg)
                    messagebox.showerror("Erro", "Erro ao gerar resumo do sistema")
                    
            except Exception as e:
                error_msg = f"Erro no resumo do sistema: {e}"
                self.log_message(f"❌ {error_msg}")
                messagebox.showerror("Erro", error_msg)
        
        self.run_in_thread(execute)
    
    def todos_relatorios(self):
        """Handler para executar todos os relatórios"""
        def execute():
            try:
                confirm = messagebox.askyesno(
                    "Executar Todos os Relatórios",
                    "Deseja executar todos os relatórios disponíveis?\n\nEsta operação pode demorar alguns minutos.",
                    parent=self.root
                )
                
                if not confirm:
                    self.log_message("❌ Execução cancelada pelo usuário")
                    return
                
                self.log_message("🚀 Executando todos os relatórios...")
                self.log_message("⏳ Aguarde... Esta operação pode demorar alguns minutos")
                
                # Capturar saída do console
                with self.capture_output() as output:
                    success = self.reports_workflow.execute_all_reports()
                
                console_output = output.getvalue()
                
                if success:
                    msg = "✅ Todos os relatórios foram executados com sucesso!"
                    self.log_message(msg)
                    
                    # Criar conteúdo para janela de resultado
                    title = "🚀 Execução de Todos os Relatórios"
                    content = console_output
                    
                    # Exibir janela de resultado
                    self.show_result_window(title, content)
                    
                else:
                    error_msg = "❌ Falha na execução dos relatórios"
                    self.log_message(error_msg)
                    messagebox.showerror("Erro", "Falha na execução dos relatórios")
                    
            except Exception as e:
                error_msg = f"Erro ao executar relatórios: {e}"
                self.log_message(f"❌ {error_msg}")
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
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 200, parent.winfo_rooty() + 100))
        
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
        title_label = ttk.Label(main_frame, text="Filtros para Consulta", font=('Arial', 12, 'bold'))
        title_label.pack(pady=(0, 15))
        
        # Tipo
        ttk.Label(main_frame, text="Filtrar por Tipo:").pack(anchor=tk.W, pady=(0, 5))
        self.tipo_var = tk.StringVar()
        self.tipo_combo = ttk.Combobox(
            main_frame, 
            textvariable=self.tipo_var,
            values=["", "ACAO", "FII", "ETF", "BDR"],
            state="readonly"
        )
        self.tipo_combo.pack(fill=tk.X, pady=(0, 15))
        self.tipo_combo.set("")
        
        # Bind para atualizar setores quando tipo mudar
        self.tipo_combo.bind('<<ComboboxSelected>>', self.on_tipo_changed)
        
        # Setor
        ttk.Label(main_frame, text="Filtrar por Setor:").pack(anchor=tk.W, pady=(0, 5))
        self.setor_var = tk.StringVar()
        self.setor_combo = ttk.Combobox(
            main_frame, 
            textvariable=self.setor_var,
            state="readonly"
        )
        self.setor_combo.pack(fill=tk.X, pady=(0, 15))
        
        # Info label
        self.info_label = ttk.Label(main_frame, text="💡 Selecione um tipo para filtrar setores disponíveis", 
                                   font=('Arial', 9), foreground='gray')
        self.info_label.pack(pady=(0, 15))
        
        # Carregar setores iniciais (todos) - DEPOIS de criar info_label
        self.load_setores()
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(
            button_frame,
            text="🔍 Consultar",
            command=self.ok_clicked
        ).pack(side=tk.RIGHT, padx=(5, 0))
        
        ttk.Button(
            button_frame,
            text="❌ Cancelar",
            command=self.cancel_clicked
        ).pack(side=tk.RIGHT)
    
    def load_setores(self, tipo_filtro=None):
        """Carrega setores disponíveis baseado no tipo selecionado"""
        try:
            from database_manager import DatabaseManager
            import pandas as pd
            db = DatabaseManager()
            
            # Primeiro verificar se há dados na tabela
            count_query = "SELECT COUNT(*) as total FROM ativos"
            count_df = pd.read_sql(count_query, db.engine)
            total_ativos = count_df.iloc[0]['total']
            
            if total_ativos == 0:
                self.setor_combo['values'] = [""]
                self.info_label.config(text="⚠️ Nenhum ativo encontrado no banco. Execute a coleta de dados primeiro.")
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
                setores = [""] + df['setor'].tolist()  # Adicionar opção vazia
                self.setor_combo['values'] = setores
                
                # Atualizar info label
                if tipo_filtro:
                    self.info_label.config(text=f"✅ {len(df)} setores encontrados para {tipo_filtro}")
                else:
                    self.info_label.config(text=f"📊 {len(df)} setores disponíveis no total")
            else:
                self.setor_combo['values'] = [""]
                if tipo_filtro:
                    self.info_label.config(text=f"⚠️ Nenhum setor encontrado para {tipo_filtro}")
                else:
                    self.info_label.config(text="⚠️ Dados sem informação de setor")
            
            # Resetar seleção
            self.setor_combo.set("")
            
        except Exception as e:
            print(f"Erro detalhado ao carregar setores: {e}")
            import traceback
            traceback.print_exc()
            self.setor_combo['values'] = [""]
            self.info_label.config(text=f"❌ Erro ao carregar setores")
    
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
            'tipo': self.tipo_var.get() if self.tipo_var.get() else None,
            'setor': self.setor_var.get() if self.setor_var.get() else None
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
        self.dialog.title("Filtros para Relatório de Dividendos")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centralizar na tela
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 200, parent.winfo_rooty() + 100))
        
        self.setup_dialog()
        
    def setup_dialog(self):
        """Configurar diálogo"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Código do ativo
        ttk.Label(main_frame, text="Código do Ativo (opcional):").pack(anchor=tk.W, pady=(0, 5))
        self.codigo_var = tk.StringVar()
        codigo_entry = ttk.Entry(main_frame, textvariable=self.codigo_var)
        codigo_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Ano
        ttk.Label(main_frame, text="Ano (opcional):").pack(anchor=tk.W, pady=(0, 5))
        self.ano_var = tk.StringVar()
        ano_entry = ttk.Entry(main_frame, textvariable=self.ano_var)
        ano_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Gerar gráfico
        self.grafico_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            main_frame,
            text="Gerar gráfico de dividendos",
            variable=self.grafico_var
        ).pack(anchor=tk.W, pady=(0, 20))
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(
            button_frame,
            text="OK",
            command=self.ok_clicked
        ).pack(side=tk.RIGHT, padx=(5, 0))
        
        ttk.Button(
            button_frame,
            text="Cancelar",
            command=self.cancel_clicked
        ).pack(side=tk.RIGHT)
        
    def ok_clicked(self):
        """Handler para botão OK"""
        codigo = self.codigo_var.get().strip().upper() if self.codigo_var.get().strip() else None
        ano_str = self.ano_var.get().strip()
        ano = int(ano_str) if ano_str and ano_str.isdigit() else None
        
        self.result = {
            'codigo': codigo,
            'ano': ano,
            'gerar_grafico': self.grafico_var.get()
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
