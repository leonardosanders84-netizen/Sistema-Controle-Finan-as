import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SistemaFinancas:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Sistema de Finanças Pessoais")
        self.raiz.geometry("1050x720")
        self.raiz.resizable(False, False)
        
        self.cor_fundo = "#ffffff"
        self.cor_verde = "#27ae60"
        self.cor_vermelho = "#e74c3c"
        self.cor_azul = "#2980b9"
        self.cor_texto = "#000000"
        
        self.fonte_texto = ("Arial", 12)
        self.fonte_destaque = ("Arial", 14, "bold")
        self.fonte_titulo = ("Arial", 16, "bold")
        self.fonte_subtitulo = ("Arial", 13, "bold")
        
        self.raiz.config(bg=self.cor_fundo)
        
        self.criar_banco_dados()
        self.criar_interface()
        self.atualizar_tabela()
        self.atualizar_saldos()

    def criar_banco_dados(self):
        self.conexao = sqlite3.connect("financas.db")
        self.cursor = self.conexao.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS lancamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                categoria TEXT NOT NULL,
                valor REAL NOT NULL,
                data TEXT NOT NULL,
                descricao TEXT
            )
        ''')
        self.conexao.commit()

    def criar_interface(self):
        titulo = tk.Label(self.raiz, text="CONTROLE DE FINANÇAS", font=self.fonte_titulo,
                         bg=self.cor_fundo, fg=self.cor_texto)
        titulo.pack(pady=20)

        quadro_saldos = tk.Frame(self.raiz, bg=self.cor_fundo)
        quadro_saldos.pack(padx=30, pady=10, fill=tk.X)
        
        self.lbl_receitas = tk.Label(quadro_saldos, text="Receitas: R$ 0,00",
                                     font=self.fonte_destaque, bg=self.cor_fundo, fg=self.cor_verde)
        self.lbl_receitas.grid(row=0, column=0, padx=50)
        
        self.lbl_despesas = tk.Label(quadro_saldos, text="Despesas: R$ 0,00",
                                     font=self.fonte_destaque, bg=self.cor_fundo, fg=self.cor_vermelho)
        self.lbl_despesas.grid(row=0, column=1, padx=50)
        
        self.lbl_saldo = tk.Label(quadro_saldos, text="Saldo Total: R$ 0,00",
                                  font=self.fonte_destaque, bg=self.cor_fundo, fg=self.cor_azul)
        self.lbl_saldo.grid(row=0, column=2, padx=50)

        quadro_cadastro = tk.LabelFrame(self.raiz, text="Novo Lançamento", font=self.fonte_subtitulo,
                                        bg=self.cor_fundo, fg=self.cor_texto, padx=20, pady=12)
        quadro_cadastro.pack(padx=30, pady=15, fill=tk.X)

        tk.Label(quadro_cadastro, text="Tipo:", font=self.fonte_texto, bg=self.cor_fundo,
                 fg=self.cor_texto).grid(row=0, column=0, padx=8, pady=6, sticky="w")
        self.cmb_tipo = ttk.Combobox(quadro_cadastro, values=["Receita", "Despesa"],
                                     state="readonly", width=18, font=self.fonte_texto)
        self.cmb_tipo.set("Receita")
        self.cmb_tipo.grid(row=0, column=1, padx=8, pady=6)

        tk.Label(quadro_cadastro, text="Categoria:", font=self.fonte_texto, bg=self.cor_fundo,
                 fg=self.cor_texto).grid(row=0, column=2, padx=8, pady=6, sticky="w")
        self.entry_categoria = ttk.Entry(quadro_cadastro, width=22, font=self.fonte_texto)
        self.entry_categoria.grid(row=0, column=3, padx=8, pady=6)

        tk.Label(quadro_cadastro, text="Valor R$:", font=self.fonte_texto, bg=self.cor_fundo,
                 fg=self.cor_texto).grid(row=0, column=4, padx=8, pady=6, sticky="w")
        self.entry_valor = ttk.Entry(quadro_cadastro, width=14, font=self.fonte_texto)
        self.entry_valor.grid(row=0, column=5, padx=8, pady=6)

        tk.Label(quadro_cadastro, text="Data:", font=self.fonte_texto, bg=self.cor_fundo,
                 fg=self.cor_texto).grid(row=1, column=0, padx=8, pady=6, sticky="w")
        self.entry_data = ttk.Entry(quadro_cadastro, width=18, font=self.fonte_texto)
        self.entry_data.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.entry_data.grid(row=1, column=1, padx=8, pady=6)

        tk.Label(quadro_cadastro, text="Descrição:", font=self.fonte_texto, bg=self.cor_fundo,
                 fg=self.cor_texto).grid(row=1, column=2, padx=8, pady=6, sticky="w")
        self.entry_descricao = ttk.Entry(quadro_cadastro, width=45, font=self.fonte_texto)
        self.entry_descricao.grid(row=1, column=3, columnspan=3, padx=8, pady=6)

        quadro_botoes = tk.Frame(self.raiz, bg=self.cor_fundo)
        quadro_botoes.pack(pady=12)
        ttk.Button(quadro_botoes, text="Adicionar", command=self.adicionar_lancamento).grid(row=0, column=0, padx=8)
        ttk.Button(quadro_botoes, text="Excluir", command=self.excluir_lancamento).grid(row=0, column=1, padx=8)
        ttk.Button(quadro_botoes, text="Gerar Gráfico", command=self.mostrar_grafico).grid(row=0, column=2, padx=8)

        quadro_principal = tk.Frame(self.raiz, bg=self.cor_fundo)
        quadro_principal.pack(padx=30, pady=15, fill=tk.BOTH, expand=True)

        colunas = ("id", "tipo", "categoria", "valor", "data", "descricao")
        estilo = ttk.Style()
        estilo.configure("Treeview.Heading", font=self.fonte_subtitulo)
        estilo.configure("Treeview", font=self.fonte_texto, rowheight=22)
        
        self.tabela = ttk.Treeview(quadro_principal, columns=colunas, show="headings", height=14)
        
        self.tabela.heading("id", text="ID")
        self.tabela.heading("tipo", text="Tipo")
        self.tabela.heading("categoria", text="Categoria")
        self.tabela.heading("valor", text="Valor")
        self.tabela.heading("data", text="Data")
        self.tabela.heading("descricao", text="Descrição")
        
        self.tabela.column("id", width=60, anchor=tk.CENTER)
        self.tabela.column("tipo", width=100, anchor=tk.CENTER)
        self.tabela.column("categoria", width=150)
        self.tabela.column("valor", width=130, anchor=tk.E)
        self.tabela.column("data", width=110, anchor=tk.CENTER)
        self.tabela.column("descricao", width=380)

        rolagem = ttk.Scrollbar(quadro_principal, orient=tk.VERTICAL, command=self.tabela.yview)
        self.tabela.configure(yscroll=rolagem.set)
        self.tabela.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        rolagem.pack(side=tk.RIGHT, fill=tk.Y)

    def adicionar_lancamento(self):
        tipo = self.cmb_tipo.get()
        categoria = self.entry_categoria.get().strip()
        valor_texto = self.entry_valor.get().strip().replace(",", ".")
        data = self.entry_data.get().strip()
        descricao = self.entry_descricao.get().strip()

        if not categoria or not valor_texto or not data:
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios!")
            return
        
        try:
            valor = float(valor_texto)
            if valor <= 0:
                raise ValueError
        except:
            messagebox.showerror("Erro", "Digite um valor válido!")
            return
        
        self.cursor.execute('''
            INSERT INTO lancamentos (tipo, categoria, valor, data, descricao)
            VALUES (?, ?, ?, ?, ?)
        ''', (tipo, categoria, valor, data, descricao))
        self.conexao.commit()
        
        self.limpar_campos()
        self.atualizar_tabela()
        self.atualizar_saldos()

    def excluir_lancamento(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showinfo("Aviso", "Selecione um lançamento!")
            return
        
        if messagebox.askyesno("Confirmação", "Deseja realmente excluir?"):
            item = self.tabela.item(selecionado[0])
            id_registro = item["values"][0]
            self.cursor.execute("DELETE FROM lancamentos WHERE id = ?", (id_registro,))
            self.conexao.commit()
            self.atualizar_tabela()
            self.atualizar_saldos()

    def mostrar_grafico(self):
        self.cursor.execute("SELECT tipo, valor FROM lancamentos")
        dados = self.cursor.fetchall()
        total_receitas = sum(v for t, v in dados if t == "Receita")
        total_despesas = sum(v for t, v in dados if t == "Despesa")
        
        plt.rcParams.update({"font.size": 12, "font.family": "Arial"})
        fig, ax = plt.subplots(figsize=(6,5))
        ax.pie([total_receitas, total_despesas], labels=["Receitas", "Despesas"],
               colors=["#27ae60", "#e74c3c"], autopct="%1.1f%%", textprops={"fontsize":12})
        ax.set_title("Distribuição de Valores", fontsize=14, fontweight="bold")
        
        janela_grafico = tk.Toplevel(self.raiz)
        janela_grafico.title("Gráfico Financeiro")
        canvas = FigureCanvasTkAgg(fig, master=janela_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def atualizar_tabela(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)
        
        self.cursor.execute("SELECT * FROM lancamentos ORDER BY data DESC")
        for reg in self.cursor.fetchall():
            self.tabela.insert("", tk.END, values=(reg[0], reg[1], reg[2],
                                                    f"R$ {reg[3]:.2f}".replace(".", ","),
                                                    reg[4], reg[5]))

    def atualizar_saldos(self):
        self.cursor.execute("SELECT SUM(valor) FROM lancamentos WHERE tipo = 'Receita'")
        rec = self.cursor.fetchone()[0] or 0
        self.cursor.execute("SELECT SUM(valor) FROM lancamentos WHERE tipo = 'Despesa'")
        desp = self.cursor.fetchone()[0] or 0
        saldo = rec - desp
        
        self.lbl_receitas.config(text=f"Receitas: R$ {rec:.2f}".replace(".", ","))
        self.lbl_despesas.config(text=f"Despesas: R$ {desp:.2f}".replace(".", ","))
        cor = self.cor_verde if saldo >=0 else self.cor_vermelho
        self.lbl_saldo.config(text=f"Saldo Total: R$ {saldo:.2f}".replace(".", ","), fg=cor)

    def limpar_campos(self):
        self.entry_categoria.delete(0, tk.END)
        self.entry_valor.delete(0, tk.END)
        self.entry_descricao.delete(0, tk.END)
        self.entry_data.delete(0, tk.END)
        self.entry_data.insert(0, datetime.now().strftime("%d/%m/%Y"))

if __name__ == "__main__":
    raiz = tk.Tk()
    app = SistemaFinancas(raiz)
    raiz.mainloop()
