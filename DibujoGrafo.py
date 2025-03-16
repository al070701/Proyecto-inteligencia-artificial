import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class InterfazGrafo:
    def __init__(self, grafo, posiciones):
        self.hospital = grafo
        self.posiciones = posiciones
        self.root = tk.Tk()
        self.root.title("Hospital")
        self.root.state('zoomed') 

        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.figura, self.ax = plt.subplots(figsize=(12, 12))
        self.node_colors = {f"Paciente{i}": 'red' for i in range(len(self.hospital.nodes()))}  # Inicialmente todos los nodos en rojo
        self.canvas_figure = FigureCanvasTkAgg(self.figura, self.canvas)
        self.canvas_figure.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

        self.dibujar_grafo()

    def actualizar_ruta(self, ruta_atencion):
        # Añadir nodos
        for paciente in ruta_atencion:
            self.hospital.add_node(f"Paciente{paciente[0]}")

        # Redibujar el grafo sin aristas iniciales
        self.dibujar_grafo()

        # Iniciar la atención de pacientes (comienza con el primer paciente)
        self.atender_paciente(ruta_atencion, 0)

    def atender_paciente(self, ruta_atencion, index):
        if index < len(ruta_atencion):
            paciente = ruta_atencion[index]
            nodo1 = f"Paciente{paciente[0]}"
            
            # Cambiar el color del nodo a verde (atendido)
            self.node_colors[nodo1] = 'green'

            # Si no es el último paciente, crear la arista hacia el siguiente
            if index < len(ruta_atencion) - 1:
                siguiente_paciente = ruta_atencion[index + 1]
                nodo2 = f"Paciente{siguiente_paciente[0]}"
                self.hospital.add_edge(nodo1, nodo2)

            # Borrar arista anterior. Si quieres que aparezca el recorrido, solo comenta estas lineas.
           # if index > 0:
           #     anterior_paciente = ruta_atencion[index - 1]
           #     nodo_anterior = f"Paciente{anterior_paciente[0]}"
           #     self.hospital.remove_edge(nodo_anterior, nodo1)

            # Redibujar el grafo con el nodo actualizado
            self.dibujar_grafo()

            # Llamar a la siguiente atención después de 2 segundos
            self.root.after(2000, self.atender_paciente, ruta_atencion, index + 1)

    def dibujar_grafo(self):
        # Limpiar la figura y los ejes antes de dibujar de nuevo
        self.ax.clear()
        nodos_colores = [self.node_colors.get(nodo, 'red') for nodo in self.hospital.nodes()]  # Colores actualizados
        nx.draw(self.hospital, pos=self.posiciones, with_labels=True, ax=self.ax, node_color=nodos_colores)
        edge_labels = nx.get_edge_attributes(self.hospital, 'weight')
        nx.draw_networkx_edge_labels(self.hospital, pos=self.posiciones, edge_labels=edge_labels, ax=self.ax)
        self.canvas_figure.draw()

    def cerrar_aplicacion(self):
        self.root.quit()  # Detiene el mainloop
        self.root.destroy()  # Cierra la ventana 
    
    def ejecutar(self):
        self.root.mainloop() # Muestra la ventana

    
