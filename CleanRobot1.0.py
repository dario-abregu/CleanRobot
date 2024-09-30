import tkinter as tk
from tkinter import messagebox
import random

class AgenteLimpiador:
    def __init__(self, filas, columnas):
        self.suelo = [[random.choice(["Sucio", "Limpio"]) for _ in range(columnas)] for _ in range(filas)]

    def limpiar(self, fila, columna):
        self.suelo[fila][columna] = "Limpio"

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Agente Limpiador")
        self.geometry("400x400")
        self.crear_ventana_ingreso()

    def crear_ventana_ingreso(self):
        self.filas_label = tk.Label(self, text="Ingrese la cantidad de filas (máx. 12):")
        self.filas_label.pack(pady=5)
        
        self.filas_entry = tk.Entry(self)
        self.filas_entry.pack(pady=5)

        self.columnas_label = tk.Label(self, text="Ingrese la cantidad de columnas (máx. 12):")
        self.columnas_label.pack(pady=5)

        self.columnas_entry = tk.Entry(self)
        self.columnas_entry.pack(pady=5)

        self.iniciar_button = tk.Button(self, text="Iniciar", command=self.iniciar)
        self.iniciar_button.pack(pady=10)

    def validar_entrada(self, valor):
        try:
            num = int(valor)
            return 1 <= num <= 12
        except ValueError:
            return False

    def iniciar(self):
        filas = self.filas_entry.get()
        columnas = self.columnas_entry.get()

        if not self.validar_entrada(filas) or not self.validar_entrada(columnas):
            self.mostrar_mensaje("Por favor, ingrese números enteros positivos de hasta 12 para filas y columnas.")
            return

        filas = int(filas)
        columnas = int(columnas)

        self.agente = AgenteLimpiador(filas, columnas)
        self.botones = [[None for _ in range(columnas)] for _ in range(filas)]
        
        # Ajustar el tamaño de la ventana
        self.geometry(f"{columnas * 100 + 50}x{filas * 100 + 100}")

        self.crear_interfaz(filas, columnas)

    def crear_interfaz(self, filas, columnas):
        for widget in self.winfo_children():
            widget.destroy()

        self.grid_frame = tk.Frame(self)
        self.grid_frame.pack()

        for i in range(filas):
            for j in range(columnas):
                estado = self.agente.suelo[i][j]
                btn = tk.Button(self.grid_frame, text=estado.capitalize(), width=10, height=3,
                                command=lambda fila=i, columna=j: self.limpiar_celda(fila, columna))
                btn.grid(row=i, column=j)
                self.botones[i][j] = btn

        # Botones para limpiar todo y reiniciar
        button_frame = tk.Frame(self.grid_frame)
        button_frame.grid(row=filas, columnspan=columnas)

        tk.Button(button_frame, text="Limpiar Todo", command=self.limpiar_todo).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Reiniciar", command=self.reiniciar).pack(side=tk.LEFT, padx=5)

    def limpiar_celda(self, fila, columna):
        self.agente.limpiar(fila, columna)
        self.botones[fila][columna].config(text="Limpio", bg="lightgreen")

    def limpiar_todo(self):
        self.proceso_limpiar(0, 0)

    def proceso_limpiar(self, fila, columna):
        if fila < len(self.agente.suelo):
            if self.agente.suelo[fila][columna] == "sucio":
                self.agente.limpiar(fila, columna)
                self.botones[fila][columna].config(text="Limpio", bg="lightgreen")

            columna += 1
            if columna >= len(self.agente.suelo[fila]):
                columna = 0
                fila += 1

            self.after(500, lambda: self.proceso_limpiar(fila, columna))  # Llamada recursiva con retraso

        else:
            self.mostrar_mensaje("Limpieza completada.")

    def mostrar_mensaje(self, mensaje):
        messagebox.showinfo("Información", mensaje)
        self.after(2000, self.cerrar_mensaje)

    def cerrar_mensaje(self):
        pass

    def reiniciar(self):
        self.destroy()
        app = Aplicacion()

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()


