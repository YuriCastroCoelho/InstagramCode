import tkinter as tk
from tkinter import ttk, messagebox

class ReelsRecommenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Recomendação de Reels")

        self.seguidores = {}
        self.reels_assistidos = {}

        self.create_widgets()

    def create_widgets(self):
        frame1 = ttk.LabelFrame(self.root, text="Seguidores (quem segue quem)")
        frame1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(frame1, text="Usuário:").grid(row=0, column=0, sticky="w")
        self.usuario_entry = ttk.Entry(frame1)
        self.usuario_entry.grid(row=0, column=1, sticky="ew")

        ttk.Label(frame1, text="Segue (separado por vírgula):").grid(row=1, column=0, sticky="w")
        self.segue_entry = ttk.Entry(frame1)
        self.segue_entry.grid(row=1, column=1, sticky="ew")

        self.add_seguidores_btn = ttk.Button(frame1, text="Adicionar Seguidores", command=self.adicionar_seguidores)
        self.add_seguidores_btn.grid(row=2, column=0, columnspan=2, pady=5)

        self.seguidores_listbox = tk.Listbox(frame1, height=6)
        self.seguidores_listbox.grid(row=3, column=0, columnspan=2, sticky="ew")

        # --- Frame Reels ---
        frame2 = ttk.LabelFrame(self.root, text="Visualizações de Reels")
        frame2.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(frame2, text="ID do Reels:").grid(row=0, column=0, sticky="w")
        self.reels_entry = ttk.Entry(frame2)
        self.reels_entry.grid(row=0, column=1, sticky="ew")

        ttk.Label(frame2, text="Assistido por (separado por vírgula):").grid(row=1, column=0, sticky="w")
        self.assistido_entry = ttk.Entry(frame2)
        self.assistido_entry.grid(row=1, column=1, sticky="ew")

        self.add_reels_btn = ttk.Button(frame2, text="Adicionar Reels", command=self.adicionar_reels)
        self.add_reels_btn.grid(row=2, column=0, columnspan=2, pady=5)

        self.reels_listbox = tk.Listbox(frame2, height=6)
        self.reels_listbox.grid(row=3, column=0, columnspan=2, sticky="ew")

        # --- Frame Recomendar ---
        frame3 = ttk.LabelFrame(self.root, text="Recomendar Reels")
        frame3.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(frame3, text="Usuário para recomendação:").grid(row=0, column=0, sticky="w")
        self.usuario_recomenda_entry = ttk.Entry(frame3)
        self.usuario_recomenda_entry.grid(row=0, column=1, sticky="ew")

        self.recomendar_btn = ttk.Button(frame3, text="Recomendar", command=self.recomendar)
        self.recomendar_btn.grid(row=1, column=0, columnspan=2, pady=5)

        self.resultado_label = ttk.Label(frame3, text="", foreground="blue")
        self.resultado_label.grid(row=2, column=0, columnspan=2, sticky="w")

        # Configurar colunas para expansão
        for frame in (frame1, frame2, frame3):
            frame.columnconfigure(1, weight=1)

    def adicionar_seguidores(self):
        usuario = self.usuario_entry.get().strip()
        seguindo_str = self.segue_entry.get().strip()
        if not usuario:
            messagebox.showerror("Erro", "Informe o nome do usuário.")
            return
        seguindo = [s.strip() for s in seguindo_str.split(",") if s.strip()]
        self.seguidores[usuario] = seguindo
        self.atualizar_lista_seguidores()
        self.usuario_entry.delete(0, tk.END)
        self.segue_entry.delete(0, tk.END)

    def atualizar_lista_seguidores(self):
        self.seguidores_listbox.delete(0, tk.END)
        for u, seg in self.seguidores.items():
            self.seguidores_listbox.insert(tk.END, f"{u} segue: {', '.join(seg) if seg else 'ninguém'}")

    def adicionar_reels(self):
        reels = self.reels_entry.get().strip()
        assistido_str = self.assistido_entry.get().strip()
        if not reels:
            messagebox.showerror("Erro", "Informe o ID do Reels.")
            return
        assistido_por = [p.strip() for p in assistido_str.split(",") if p.strip()]
        self.reels_assistidos[reels] = assistido_por
        self.atualizar_lista_reels()
        self.reels_entry.delete(0, tk.END)
        self.assistido_entry.delete(0, tk.END)

    def atualizar_lista_reels(self):
        self.reels_listbox.delete(0, tk.END)
        for r, users in self.reels_assistidos.items():
            self.reels_listbox.insert(tk.END, f"{r} assistido por: {', '.join(users) if users else 'ninguém'}")

    def recomendar(self):
        usuario = self.usuario_recomenda_entry.get().strip()
        if not usuario:
            messagebox.showerror("Erro", "Informe o usuário para recomendação.")
            return
        if usuario not in self.seguidores:
            messagebox.showerror("Erro", "Usuário não encontrado.")
            return

        seguindo = set(self.seguidores.get(usuario, []))
        pontuacao = {}

        for reels, quem_assistiu in self.reels_assistidos.items():
            score = sum(1 for pessoa in quem_assistiu if pessoa in seguindo)
            if score > 0:
                pontuacao[reels] = score

        recomendados = sorted(pontuacao.items(), key=lambda x: -x[1])
        if recomendados:
            texto = "Reels sugeridos: " + ", ".join(r for r, _ in recomendados)
        else:
            texto = "Nenhuma sugestão encontrada."

        self.resultado_label.config(text=texto)

if __name__ == "__main__":
    root = tk.Tk()
    app = ReelsRecommenderApp(root)
    root.mainloop()
