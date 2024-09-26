""" import tkinter as tk
from tkinter import filedialog, messagebox
import time
import os  # Importar os para obtener el nombre del archivo
import fuerzabruta
import voraz
import dinamica

class ModExApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ModEx - Moderación de Extremismo")
        
        # Variables
        self.test_data = ""
        self.algorithm = tk.StringVar(value="Fuerza Bruta")
        self.R_max = 0  # Variable para R_max
        self.filename = ""  # Variable para almacenar el nombre del archivo
        
        # UI Components
        self.create_widgets()

    def create_widgets(self):
        # Etiqueta para mostrar el nombre del archivo
        self.file_label = tk.Label(self.root, text="No se ha cargado ninguna prueba", fg="blue")
        self.file_label.pack(pady=10)

        # Cargar archivo
        load_button = tk.Button(self.root, text="Cargar Prueba", command=self.load_file)
        load_button.pack(pady=10)
        
        # Mostrar archivo cargado
        self.text_area = tk.Text(self.root, height=10, width=50)
        self.text_area.pack(pady=10)

        # Seleccionar algoritmo
        tk.Label(self.root, text="Selecciona Algoritmo").pack()
        algorithm_menu = tk.OptionMenu(self.root, self.algorithm, "Fuerza Bruta", "Voraz", "Programación Dinámica")
        algorithm_menu.pack(pady=10)

        # Botón de ejecución
        run_button = tk.Button(self.root, text="Ejecutar", command=self.run_algorithm)
        run_button.pack(pady=10)

        # Mostrar resultados
        self.result_label = tk.Label(self.root, text="", fg="green")
        self.result_label.pack(pady=10)

        # Área de texto para los resultados detallados
        self.result_text_area = tk.Text(self.root, height=10, width=50)
        self.result_text_area.pack(pady=10)

    def load_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                self.test_data = file.read()

            # Obtener el nombre del archivo
            self.filename = os.path.basename(file_path)

            # Actualizar la etiqueta con el nombre del archivo
            self.file_label.config(text=f"Prueba cargada: {self.filename}", fg="blue")

            # Mostrar el contenido del archivo en el área de texto
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, self.test_data)

    def run_algorithm(self):
        if not self.test_data:
            messagebox.showerror("Error", "Por favor, carga una prueba primero.")
            return

        # Procesar la prueba (adaptar esta parte según sea necesario)
        try:
            data, R_max = self.parse_test_data(self.test_data)
            algorithm = self.algorithm.get()

            # Limpiar el área de texto de resultados
            self.result_text_area.delete(1.0, tk.END)

            # Medir tiempo de ejecución
            start_time = time.time()

            # Ejecutar el algoritmo seleccionado
            if algorithm == "Fuerza Bruta":
                result = fuerzabruta.modexFB(data, R_max)
            elif algorithm == "Voraz":
                result = voraz.modexGreedy(data, R_max)
            elif algorithm == "Programación Dinámica":
                result = dinamica.modexPD(data, R_max)

            end_time = time.time()  # Fin del tiempo de ejecución
            execution_time = end_time - start_time  # Tiempo transcurrido

            # Mostrar los resultados en la etiqueta y en el área de texto
            self.result_label.config(text=f"Algoritmo: {algorithm} ejecutado con éxito", fg="green")
            self.result_text_area.insert(tk.END, f"Resultados:\n{result}\n")
            self.result_text_area.insert(tk.END, f"Tiempo de ejecución: {execution_time:.4f} segundos\n")
        
        except Exception as e:
            self.result_label.config(text="Error al ejecutar el algoritmo", fg="red")
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    def parse_test_data(self, test_data):
        # Parsear el archivo de texto y extraer R_max
        lines = test_data.strip().split("\n")
        n = int(lines[0])
        agents = [tuple(map(float, line.split(','))) for line in lines[1:n+1]]
        R_max = int(lines[n+1])
        return agents, R_max  # Devuelve la lista de agentes y R_max

if __name__ == "__main__":
    root = tk.Tk()
    app = ModExApp(root)
    root.mainloop() """


############33
import tkinter as tk
from tkinter import messagebox, filedialog
import time
import os


import fuerzabruta
import voraz
import dinamica

class MyApp:
    def __init__(self, root):
        self.root = root
        self.test_data = ""
        self.filename = ""
        self.algorithm = tk.StringVar()
        self.algorithm.set("Fuerza Bruta")  # Valor por defecto
        
        self.root.title("ADA-II")

        # Configuración de la interfaz gráfica
        self.file_label = tk.Label(root, text="No file loaded")
        self.file_label.pack()

        self.text_area = tk.Text(root, height=10, width=50)
        self.text_area.pack()

        self.result_text_area = tk.Text(root, height=10, width=50)
        self.result_text_area.pack()

        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

        self.load_button = tk.Button(root, text="Cargar Prueba", command=self.load_file)
        self.load_button.pack()

        self.run_button = tk.Button(root, text="Ejecutar Algoritmo", command=self.run_algorithm)
        self.run_button.pack()

        self.save_button = tk.Button(root, text="Guardar Resultados", command=self.save_results)
        self.save_button.pack()

        self.algorithm_menu = tk.OptionMenu(root, self.algorithm, "Fuerza Bruta", "Voraz", "Programación Dinámica")
        self.algorithm_menu.pack()

    def load_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                self.test_data = file.read()

                # Obtener el nombre del archivo
                self.filename = os.path.basename(file_path)

                # Actualizar la etiqueta con el nombre del archivo
                self.file_label.config(text=f"Prueba cargada: {self.filename}", fg="blue")

                # Mostrar el contenido del archivo en el área de texto
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, self.test_data)

    def run_algorithm(self):
        if not self.test_data:
            messagebox.showerror("Error", "Por favor, carga una prueba primero.")
            return

        # Procesar la prueba
        try:
            data, R_max = self.parse_test_data(self.test_data)
            algorithm = self.algorithm.get()

            # Limpiar el área de texto de resultados
            self.result_text_area.delete(1.0, tk.END)

            # Medir tiempo de ejecución
            start_time = time.time()

            # Ejecutar el algoritmo seleccionado
            if algorithm == "Fuerza Bruta":
                strategy, effort, extremism = fuerzabruta.modexFB(data, R_max)
            elif algorithm == "Voraz":
                strategy, effort, extremism = voraz.modexGreedy(data, R_max)
            elif algorithm == "Programación Dinámica":
                strategy, effort, extremism = dinamica.modexPD(data, R_max)
            else:
                messagebox.showerror("Error", "Algoritmo no reconocido.")
                return

            end_time = time.time()  # Fin del tiempo de ejecución
            execution_time = end_time - start_time  # Tiempo transcurrido

            # Formatear los resultados
            self.result_text = f"Algoritmo: {algorithm}\n"
            self.result_text += f"Tiempo de ejecucion: {execution_time:.4f} segundos\n"
            self.result_text += f"Total de agentes: {len(data)}\n"
            self.result_text += f"Recurso maximo: {R_max}\n"
            self.result_text += f"Estrategia: {strategy}\n"
            self.result_text += f"Esfuerzo total: {effort:.6f}\n"
            self.result_text += f"Extremismo: {extremism:.6f}\n\n"
            self.result_text += "Agentes moderados:\n"
            for i, (opinion, receptivity) in enumerate(data):
                if strategy[i] == 1:
                    self.result_text += f"Agente {i + 1}: Opinion = {opinion}, Receptividad = {receptivity}\n"

            # Mostrar los resultados en el área de texto
            self.result_text_area.insert(tk.END, self.result_text)

        except Exception as e:
            self.result_label.config(text="Error al ejecutar el algoritmo", fg="red")
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    def save_results(self):
        if not hasattr(self, 'result_text'):
            messagebox.showerror("Error", "No hay resultados para guardar. Ejecuta un algoritmo primero.")
            return

        # Crear la carpeta 'resultados' si no existe
        if not os.path.exists('Resultados'):
            os.makedirs('Resultados')

        # Generar el nombre del archivo de salida basado en el nombre del archivo de prueba y el algoritmo
        base_filename = os.path.splitext(self.filename)[0]
        algorithm_name = self.algorithm.get().replace(" ", "_").lower()
        output_filename = f"r-{base_filename}-{algorithm_name}.txt"
        file_path = os.path.join('Resultados', output_filename)

        with open(file_path, 'w') as file:
            file.write(self.result_text)
        messagebox.showinfo("Guardado", f"Resultados guardados en {file_path}")

    def parse_test_data(self, test_data):
        lines = test_data.strip().split('\n')
        agentnumber = int(lines[0].strip())
        rmax = int(lines[-1].strip())
        datos = []
        for line in lines[1:agentnumber + 1]:
            line = line.strip()
            if line:
                elementos = line.split(',')
                datos.append((int(elementos[0]), float(elementos[1])))
        return datos, rmax

# Ejemplo de uso
root = tk.Tk()
app = MyApp(root)
root.mainloop()