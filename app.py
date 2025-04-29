import tkinter as tk
from tkinter import messagebox

class Cronometro:
    def __init__(self, root):
        self.root = root
        self.root.title("Cronômetro")
        self.root.geometry("400x160")
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)

        # Fundo transparente (Windows apenas)
        self.root.config(bg='white')
        self.root.wm_attributes('-transparentcolor', 'black')

        # Inicialmente translúcido
        self.root.wm_attributes('-alpha', 0.5)

        self.frame = tk.Frame(self.root, bg='black')
        self.frame.pack(fill='both', expand=True)

        self.label = tk.Label(
            self.frame,
            text="0:00:00",
            font=("Torus", 60),
            fg="white",
            bg='black'
        )
        self.label.pack(expand=True)

        self.tempo = 0
        self.rodando = False
        self.offset_x = 0
        self.offset_y = 0

        # Clique para iniciar/pausar
        self.frame.bind("<Button-1>", self.iniciar_pausa)
        self.label.bind("<Button-1>", self.iniciar_pausa)

        # Arrastar janela
        self.frame.bind("<B1-Motion>", self.mover_janela)
        self.label.bind("<B1-Motion>", self.mover_janela)

        # Clique com o botão direito = menu de contexto
        self.frame.bind("<Button-3>", self.mostrar_menu)
        self.label.bind("<Button-3>", self.mostrar_menu)

        # Tecla F12 = alternar borda
        self.root.bind("<F12>", self.toggle_borda)

        # Hover do mouse (opacidade dinâmica)
        self.frame.bind("<Enter>", self.mouse_entrar)
        self.frame.bind("<Leave>", self.mouse_sair)
        self.label.bind("<Enter>", self.mouse_entrar)
        self.label.bind("<Leave>", self.mouse_sair)
        
        # Menu de contexto
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="Iniciar/Pausar", command=self.iniciar_pausa)
        self.menu.add_command(label="Copiar Tempo", command=self.copiar_tempo)
        self.menu.add_command(label="Zerar", command=self.zerar)
        self.menu.add_separator()
        self.menu.add_command(label="Fechar", command=self.fechar)



        self.atualizar()

    def iniciar_pausa(self, event=None):
        self.rodando = not self.rodando
        if self.rodando:
            self.label.config(fg="lime")  # Muda a cor para verde quando o cronômetro estiver ativo
        else:
            self.label.config(fg="white")  # Muda a cor para branco quando o cronômetro estiver pausado
        if event:
            self.offset_x = event.x_root - self.root.winfo_x()
            self.offset_y = event.y_root - self.root.winfo_y()


    def mover_janela(self, event):
        x = event.x_root - self.offset_x
        y = event.y_root - self.offset_y
        self.root.geometry(f"+{x}+{y}")

    def mouse_entrar(self, event):
        self.root.wm_attributes('-alpha', 1.0)

    def mouse_sair(self, event):
        self.root.wm_attributes('-alpha', 0.5)

    def atualizar(self):
        if self.rodando:
            self.tempo += 1
            horas = self.tempo // 3600  # Converte para horas
            minutos = (self.tempo % 3600) // 60  # Converte o restante para minutos
            segundos = self.tempo % 60  # O que sobrou é o número de segundos
            self.label.config(text=f"{horas:2}:{minutos:02}:{segundos:02}")
        self.root.after(1000, self.atualizar)

    def mostrar_menu(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def copiar_tempo(self):
        horas = self.tempo // 3600  # Calcula as horas
        minutos = (self.tempo % 3600) // 60  # Calcula os minutos restantes após remover as horas
        segundos = self.tempo % 60  # Calcula os segundos restantes após remover minutos
        tempo_formatado = f"{horas:02}:{minutos:02}:{segundos:02}"  # Exibe no formato HH:MM:SS
        self.root.clipboard_clear()  # Limpa a área de transferência
        self.root.clipboard_append(tempo_formatado)  # Copia o tempo formatado para a área de transferência
        self.root.update()  # Garante que o conteúdo seja atualizado na área de transferência

      
    def zerar(self):
        if messagebox.askyesno("Zerar cronômetro", "Tem certeza que deseja zerar o cronômetro?"):
            self.tempo = 0
            self.label.config(text="0:00:00")

    def fechar(self):
        if messagebox.askokcancel("Fechar", "Deseja realmente sair?"):
            self.root.destroy()

    def toggle_borda(self, event=None):
        atual = self.root.overrideredirect()
        self.root.overrideredirect(not atual)

        
if __name__ == "__main__":
    root = tk.Tk()
    Cronometro(root)
    root.mainloop()
