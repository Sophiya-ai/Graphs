import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter.ttk import Combobox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GraphVisualizationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Визуализация поиска путей в графах")

        # Инициализация графа
        self.graph = None
        self.is_directed = False
        self.is_weighted = False

        # Создаем холст для отображения графа
        self.create_canvas()

        # Сброс графа после создания холста
        self.reset_graph()

        # Интерфейс
        self.create_widgets()

    def create_canvas(self):
        """Создает холст для отображения графа."""
        self.figure = plt.Figure(figsize=(6, 6))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, padx=10, pady=10)

    def reset_graph(self):
        """Инициализирует граф в зависимости от типа (орграф/неорграф)."""
        if self.is_directed:
            self.graph = nx.DiGraph()
        else:
            self.graph = nx.Graph()
        self.draw_graph()

    def create_widgets(self):
        """Создает элементы управления в интерфейсе."""
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Выбор типа графа
        tk.Label(control_frame, text="Тип графа:").pack(anchor=tk.W)
        self.graph_type_var = tk.StringVar(value="Неорграф")
        tk.Radiobutton(control_frame, text="Неорграф", variable=self.graph_type_var, value="Неорграф",
                       command=self.update_graph_type).pack(anchor=tk.W)
        tk.Radiobutton(control_frame, text="Орграф", variable=self.graph_type_var, value="Орграф",
                       command=self.update_graph_type).pack(anchor=tk.W)

        # Выбор весов
        tk.Label(control_frame, text="Веса:").pack(anchor=tk.W)
        self.weight_var = tk.BooleanVar(value=False)
        tk.Checkbutton(control_frame, text="Взвешенный", variable=self.weight_var,
                       command=self.update_weights).pack(anchor=tk.W)

        # Выбор алгоритма
        tk.Label(control_frame, text="Алгоритм поиска пути:").pack(anchor=tk.W)
        self.algorithm_var = tk.StringVar(value="Dijkstra")
        algorithms = ["Dijkstra", "BFS", "Bellman-Ford"]
        self.algorithm_combo = Combobox(control_frame, textvariable=self.algorithm_var, values=algorithms, state="readonly")
        self.algorithm_combo.pack(fill=tk.X, pady=5)

        # Кнопки управления
        tk.Button(control_frame, text="Добавить вершину", command=self.add_node).pack(fill=tk.X, pady=5)
        tk.Button(control_frame, text="Добавить ребро", command=self.add_edge).pack(fill=tk.X, pady=5)
        tk.Button(control_frame, text="Удалить вершину", command=self.remove_node).pack(fill=tk.X, pady=5)
        tk.Button(control_frame, text="Удалить ребро", command=self.remove_edge).pack(fill=tk.X, pady=5)
        tk.Button(control_frame, text="Построить матрицу смежности", command=self.show_adjacency_matrix).pack(fill=tk.X,
                                                                                                              pady=5)
        tk.Button(control_frame, text="Построить матрицу инцидентности", command=self.show_incidence_matrix).pack(
            fill=tk.X, pady=5)
        tk.Button(control_frame, text="Поиск пути", command=self.find_path).pack(fill=tk.X, pady=5)

    def update_graph_type(self):
        graph_type = self.graph_type_var.get()
        if graph_type == "Орграф":
            self.is_directed = True
        else:
            self.is_directed = False
        self.reset_graph()

    def update_weights(self):
        self.is_weighted = self.weight_var.get()
        self.reset_graph()

    def add_node(self):
        if self.graph is None:  # Проверяем, инициализирован ли граф
            messagebox.showwarning("Предупреждение", "Граф не инициализирован!")
            return

        node_name = simpledialog.askstring("Добавление вершины", "Введите имя вершины:")
        if node_name and node_name not in self.graph.nodes:
            self.graph.add_node(node_name)
            self.draw_graph()
        elif node_name in self.graph.nodes:
            messagebox.showwarning("Предупреждение", "Вершина уже существует!")

    def add_edge(self):
        if self.graph is None:  # Проверяем, инициализирован ли граф
            messagebox.showwarning("Предупреждение", "Граф не инициализирован!")
            return

        if self.is_weighted:
            edge_input = simpledialog.askstring("Добавление ребра", "Введите ребро (формат: 'A B вес'):")
            if edge_input:
                try:
                    u, v, weight = edge_input.split()
                    weight = float(weight)
                    self.graph.add_edge(u, v, weight=weight)
                    self.draw_graph()
                except ValueError:
                    messagebox.showerror("Ошибка", "Неверный формат ввода!")
        else:
            edge_input = simpledialog.askstring("Добавление ребра", "Введите ребро (формат: 'A B'):")
            if edge_input:
                try:
                    u, v = edge_input.split()
                    self.graph.add_edge(u, v)
                    self.draw_graph()
                except ValueError:
                    messagebox.showerror("Ошибка", "Неверный формат ввода!")

    def remove_node(self):
        if self.graph is None:  # Проверяем, инициализирован ли граф
            messagebox.showwarning("Предупреждение", "Граф не инициализирован!")
            return

        node_name = simpledialog.askstring("Удаление вершины", "Введите имя вершины:")
        if node_name and node_name in self.graph.nodes:
            self.graph.remove_node(node_name)
            self.draw_graph()
        elif node_name not in self.graph.nodes:
            messagebox.showwarning("Предупреждение", "Такой вершины нет!")

    def remove_edge(self):
        if self.graph is None:  # Проверяем, инициализирован ли граф
            messagebox.showwarning("Предупреждение", "Граф не инициализирован!")
            return

        edge_input = simpledialog.askstring("Удаление ребра", "Введите ребро (формат: 'A B'):")
        if edge_input:
            try:
                u, v = edge_input.split()
                if self.graph.has_edge(u, v):
                    self.graph.remove_edge(u, v)
                    self.draw_graph()
                else:
                    messagebox.showwarning("Предупреждение", "Такого ребра нет!")
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат ввода!")

    def show_adjacency_matrix(self):
        if self.graph is None or len(self.graph.nodes) == 0:
            messagebox.showwarning("Предупреждение", "Граф пуст! Добавьте вершины и рёбра.")
            return

        adj_matrix = nx.to_numpy_array(self.graph)  # Используем NumPy вместо scipy.sparse
        messagebox.showinfo("Матрица смежности", str(adj_matrix))

    def show_incidence_matrix(self):
        if self.graph is None or len(self.graph.nodes) == 0:
            messagebox.showwarning("Предупреждение", "Граф пуст! Добавьте вершины и рёбра.")
            return

        inc_matrix = nx.incidence_matrix(self.graph).todense()
        messagebox.showinfo("Матрица инцидентности", str(inc_matrix))

    def find_path(self):
        if self.graph is None or len(self.graph.nodes) == 0:
            messagebox.showwarning("Предупреждение", "Граф пуст! Добавьте вершины и рёбра.")
            return

        start_node = simpledialog.askstring("Поиск пути", "Введите начальную вершину:")
        end_node = simpledialog.askstring("Поиск пути", "Введите конечную вершину:")

        if start_node and end_node:
            if start_node not in self.graph.nodes or end_node not in self.graph.nodes:
                messagebox.showwarning("Предупреждение", "Одна из вершин не существует!")
                return

            algorithm = self.algorithm_var.get()
            try:
                if algorithm == "Dijkstra":
                    if self.is_weighted:
                        path = nx.dijkstra_path(self.graph, start_node, end_node, weight='weight')
                    else:
                        path = nx.dijkstra_path(self.graph, start_node, end_node)
                elif algorithm == "BFS":
                    path = nx.shortest_path(self.graph, start_node, end_node, method='bfs')
                elif algorithm == "Bellman-Ford":
                    if self.is_weighted:
                        path = nx.bellman_ford_path(self.graph, start_node, end_node, weight='weight')
                    else:
                        path = nx.bellman_ford_path(self.graph, start_node, end_node)
                else:
                    messagebox.showwarning("Предупреждение", "Выбранный алгоритм недоступен!")
                    return

                messagebox.showinfo("Путь", f"Кратчайший путь ({algorithm}): {path}")
            except nx.NetworkXNoPath:
                messagebox.showwarning("Предупреждение", "Пути между вершинами не существует!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

    def draw_graph(self):
        self.ax.clear()
        pos = nx.spring_layout(self.graph)
        edge_labels = {(u, v): d['weight'] for u, v, d in self.graph.edges(data=True)} if self.is_weighted else None
        nx.draw(self.graph, pos, with_labels=True, ax=self.ax)
        if self.is_weighted:
            nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, ax=self.ax)
        self.canvas.draw()


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = GraphVisualizationApp(root)
    root.mainloop()