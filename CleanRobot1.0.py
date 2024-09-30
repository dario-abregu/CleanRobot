import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import requests
from io import BytesIO

class AgenteLimpiador:
    def __init__(self, filas, columnas):
        self.suelo = [[random.choice(["sucio", "limpio"]) for _ in range(columnas)] for _ in range(filas)]

    def limpiar(self, fila, columna):
        self.suelo[fila][columna] = "limpio"

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Agente Limpiador")
        self.geometry("600x600")
        self.crear_ventana_ingreso()
        self.imagen_limpio = self.cargar_imagen("https://static.vecteezy.com/system/resources/thumbnails/038/780/795/small/ai-generated-wet-cleaning-of-the-floor-using-a-mop-concept-of-cleaning-housework-generated-by-artificial-intelligence-photo.jpg")
        self.imagen_sucio = self.cargar_imagen("https://www.shutterstock.com/image-photo/mud-stain-on-wooden-floor-600nw-2512184845.jpg")

    def cargar_imagen(self, url):
        response = requests.get(url)
        img_data = Image.open(BytesIO(response.content))
        img_data = img_data.resize((80, 80), Image.LANCZOS)  # Cambia el tamaño de la imagen
        return ImageTk.PhotoImage(img_data)

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

        # Crear un canvas para permitir scroll
        self.canvas = tk.Canvas(self)
        self.scroll_y = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scroll_x = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)

        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

        self.scroll_y.pack(side="right", fill="y")
        self.scroll_x.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Marco para centrar el contenido con margen a la izquierda
        center_frame = tk.Frame(self.scrollable_frame)
        center_frame.pack(expand=True)

        # Crear un marco con margen a la izquierda
        margin_frame = tk.Frame(center_frame)
        margin_frame.pack(side=tk.LEFT, padx=(self.winfo_width() * 0.05, 0))  # Margen izquierdo del 5%

        # Crear una cuadrícula centrada
        grid_frame = tk.Frame(margin_frame)
        grid_frame.pack()

        for i in range(filas):
            for j in range(columnas):
                estado = self.agente.suelo[i][j]
                imagen = self.imagen_limpio if estado == "limpio" else self.imagen_sucio
                
                # Crear un marco para cada botón
                marco = tk.Frame(grid_frame, bd=1, relief="solid", bg="white")
                marco.grid(row=i, column=j, padx=5, pady=5)

                btn = tk.Button(marco, image=imagen, width=80, height=80,
                                command=lambda fila=i, columna=j: self.limpiar_celda(fila, columna))
                btn.pack()

                self.botones[i][j] = btn

        # Botones para limpiar todo y reiniciar
        button_frame = tk.Frame(margin_frame)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Limpiar Todo", command=self.limpiar_todo).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Reiniciar", command=self.reiniciar).pack(side=tk.LEFT, padx=5)

    def limpiar_celda(self, fila, columna):
        self.agente.limpiar(fila, columna)
        self.botones[fila][columna].config(image=self.imagen_limpio)

    def limpiar_todo(self):
        self.proceso_limpiar(0, 0)

    def proceso_limpiar(self, fila, columna):
        if fila < len(self.agente.suelo):
            if self.agente.suelo[fila][columna] == "sucio":
                # Resaltar antes de cambiar el estado
                self.botones[fila][columna].config(bg="green")
                self.after(500, lambda: self.cambiar_estado(fila, columna))  # Cambiar estado después de un breve retraso

            else:
                columna += 1
                if columna >= len(self.agente.suelo[fila]):
                    columna = 0
                    fila += 1

                self.after(500, lambda: self.proceso_limpiar(fila, columna))  # Llamada recursiva con retraso
        else:
            self.mostrar_mensaje("Limpieza completada.")

    def cambiar_estado(self, fila, columna):
        self.agente.limpiar(fila, columna)
        self.botones[fila][columna].config(image=self.imagen_limpio, bg="white")  # Cambiar a la imagen de limpio y restaurar el color

        columna += 1
        if columna >= len(self.agente.suelo[fila]):
            columna = 0
            fila += 1

        self.after(500, lambda: self.proceso_limpiar(fila, columna))  # Llamada recursiva con retraso

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


