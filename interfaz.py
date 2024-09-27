import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
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

        # Cambiar el título de la ventana principal
        self.root.title("ADA-2-PROYECTO1")

        # Configuración de la interfaz gráfica
        self.file_label = tk.Label(root, text="No file loaded")
        self.file_label.pack()

        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

        # Crear un Frame para los botones
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.load_button = tk.Button(self.button_frame, text="Cargar Prueba", command=self.load_file)
        self.load_button.pack(pady=5)

        self.run_button = tk.Button(self.button_frame, text="Ejecutar Algoritmo", command=self.run_algorithm)
        self.run_button.pack(pady=5)

        self.save_button = tk.Button(self.button_frame, text="Guardar Resultados", command=self.save_results)
        self.save_button.pack(pady=5)

        self.clear_button = tk.Button(self.button_frame, text="Limpiar Tablas", command=self.clear_tables)
        self.clear_button.pack(pady=5)

        self.algorithm_menu = tk.OptionMenu(self.button_frame, self.algorithm, "Fuerza Bruta", "Voraz", "Programación Dinámica")
        self.algorithm_menu.pack(pady=5)

        # Título para la tabla de entrada
        self.input_label = tk.Label(root, text="Datos de Entrada")
        self.input_label.pack()

        # Widget Treeview para mostrar los datos de entrada en una tabla
        self.input_tree = ttk.Treeview(root, columns=("Agente", "Opinión", "Receptividad", "Total Agentes", "R_max"), show='headings')
        self.input_tree.heading("Agente", text="Agente")
        self.input_tree.heading("Opinión", text="Opinión")
        self.input_tree.heading("Receptividad", text="Receptividad")
        self.input_tree.heading("Total Agentes", text="Total Agentes")
        self.input_tree.heading("R_max", text="R_max")
        self.input_tree.pack(padx=10, pady=10)
        
        # Centrar los datos en las columnas de la tabla de entrada
        for col in self.input_tree["columns"]:
            self.input_tree.column(col, anchor="center")

        # Título para la tabla de salida
        self.output_label = tk.Label(root, text="Resultados")
        self.output_label.pack()

        #Widget Treeview para mostrar los resultados en una tabla
        self.tree = ttk.Treeview(root, columns=("Agente", "Opinión", "Receptividad", "Moderado", "Total Agentes", "Esfuerzo Total", "Extremismo"), show='headings')
        self.tree.heading("Agente", text="Agente")
        self.tree.heading("Opinión", text="Opinión")
        self.tree.heading("Receptividad", text="Receptividad")
        self.tree.heading("Moderado", text="Moderado")
        self.tree.heading("Total Agentes", text="Total Agentes")
        self.tree.heading("Esfuerzo Total", text="Esfuerzo Total")
        self.tree.heading("Extremismo", text="Extremismo")
        self.tree.pack(padx=10, pady=10)
        
        # Centrar los datos en las columnas de la tabla de resultados
        for col in self.tree["columns"]:
            self.tree.column(col, anchor="center")

    def load_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                self.test_data = file.read()

                # Obtener el nombre del archivo
                self.filename = os.path.basename(file_path)

                # Actualizar la etiqueta con el nombre del archivo
                self.file_label.config(text=f"Prueba cargada: {self.filename}", fg="blue")

                # Limpiar la tabla de datos de entrada
                for item in self.input_tree.get_children():
                    self.input_tree.delete(item)

                # Insertar los datos de entrada en la tabla
                data, R_max = self.parse_test_data(self.test_data)

                # Insertar los datos de resumen al inicio de la tabla de entrada
                self.input_tree.insert("", "end", values=("", "", "", len(data), R_max))

                for i, (opinion, receptivity) in enumerate(data):
                    self.input_tree.insert("", "end", values=(i + 1, opinion, receptivity, "", ""))

    def run_algorithm(self):
        if not self.test_data:
            messagebox.showerror("Error", "Por favor, carga una prueba primero.")
            return

        # Procesar la prueba
        try:
            data, R_max = self.parse_test_data(self.test_data)
            algorithm = self.algorithm.get()

            # Limpiar la tabla de resultados
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Medir tiempo de ejecución
            start_time = time.time()

            # Ejecutar el algoritmo seleccionado
            if algorithm == "Fuerza Bruta":
                strategy, effort, extremism = fuerzabruta.rocFB(data, R_max)
            elif algorithm == "Voraz":
                strategy, effort, extremism = voraz.rocV(data, R_max)
            elif algorithm == "Programación Dinámica":
                strategy, effort, extremism = dinamica.rocPD(data, R_max)
            else:
                messagebox.showerror("Error", "Algoritmo no reconocido.")
                return

            end_time = time.time()  # Fin del tiempo de ejecución
            execution_time = end_time - start_time  # Tiempo transcurrido

            # Insertar los datos de resumen al inicio de la tabla de resultados
            self.tree.insert("", "end", values=("", "", "", "", len(data), f"{effort:.2f}", f"{extremism:.2f}"))

            # Insertar los datos de resultados en la tabla
            for i, (opinion, receptivity) in enumerate(data):
                moderado = "Si" if strategy[i] == 1 else "No"
                self.tree.insert("", "end", values=(i + 1, opinion, receptivity, moderado, "", "", ""))

        except Exception as e:
            self.result_label.config(text="Error al ejecutar el algoritmo", fg="red")
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")


    def save_results(self):
        if not self.tree.get_children():
            messagebox.showerror("Error", "No hay resultados para guardar. Ejecuta un algoritmo primero.")
            return

        # Crear la carpeta 'Resultados' si no existe
        if not os.path.exists('Resultados'):
            os.makedirs('Resultados')

        # Generar el nombre del archivo de salida basado en el nombre del archivo de prueba y el algoritmo
        base_filename = os.path.splitext(self.filename)[0]
        algorithm_name = self.algorithm.get().replace(" ", "_").lower()
        output_filename = f"r-{base_filename}-{algorithm_name}.txt"
        file_path = os.path.join('Resultados', output_filename)

        with open(file_path, 'w') as file:
            # Escribir el extremismo y el esfuerzo total
            extremism = self.tree.item(self.tree.get_children()[0], 'values')[6]
            effort = self.tree.item(self.tree.get_children()[0], 'values')[5]
            file.write(f"Extremismo {extremism}\n\n")
            file.write(f"Esfuerzo {effort}\n\n")

            # Escribir los agentes moderados y no moderados
            for item in self.tree.get_children()[1:]:
                values = self.tree.item(item, 'values')
                moderado = 0
                if values[3] == "Si": 
                    moderado = 1
                
                file.write(f"{moderado}\n")

        messagebox.showinfo("Guardado", f"Resultados guardados en {file_path}")
    def clear_tables(self):
        # Limpiar la tabla de datos de entrada
        for item in self.input_tree.get_children():
            self.input_tree.delete(item)

        # Limpiar la tabla de resultados
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Limpiar la etiqueta de archivo cargado
        self.file_label.config(text="No file loaded", fg="black")

        # Limpiar los datos de prueba
        self.test_data = ""
        self.filename = ""

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


root = tk.Tk()
app = MyApp(root)
root.mainloop()