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

        # Añadir el widget Treeview para mostrar los resultados en una tabla
        self.tree = ttk.Treeview(root, columns=("Agente", "Opinión", "Receptividad", "Moderado"), show='headings')
        self.tree.heading("Agente", text="Agente")
        self.tree.heading("Opinión", text="Opinión")
        self.tree.heading("Receptividad", text="Receptividad")
        self.tree.heading("Moderado", text="Moderado")
        self.tree.pack()

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

            # Limpiar la tabla de resultados
            for item in self.tree.get_children():
                self.tree.delete(item)

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
            self.result_text += f"Tiempo de ejecución: {execution_time:.4f} segundos\n"
            self.result_text += f"Total de agentes: {len(data)}\n"
            self.result_text += f"Recurso máximo: {R_max}\n"
            self.result_text += f"Estrategia: {strategy}\n"
            self.result_text += f"Esfuerzo total: {effort:.6f}\n"
            self.result_text += f"Extremismo: {extremism:.6f}\n\n"
            self.result_text += "Agentes moderados:\n"
            for i, (opinion, receptivity) in enumerate(data):
                moderado = "Sí" if strategy[i] == 1 else "No"
                self.result_text += f"Agente {i + 1}: Opinión = {opinion}, Receptividad = {receptivity}, Moderado = {moderado}\n"
                # Insertar los datos en la tabla
                self.tree.insert("", "end", values=(i + 1, opinion, receptivity, moderado))

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