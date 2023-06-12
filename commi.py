import tkinter as tk
import math


def solve_tsp(points):
    """
    B этой функции решается задача коммивояжера (TSP) c помощью метода "ветвей и границ".
    """
    num_cities = len(points)  # количество городов
    shortest_distance = math.inf  # кратчайшее расстояние (inf изначально)
    shortest_path = None  # кратчайший путь
    visited = [False] * num_cities  # список, отслеживающий, посещен ли город
    path = []  # текущий путь

    def tsp_helper(current_city, current_distance, depth):
        """
        Вспомогательная функция, которая рекурсивно исследует все пути и находит кратчайший.
        """
        nonlocal shortest_distance, shortest_path

        # проверяется, достигнутa ли максимальная глубина
        if depth == num_cities:
            # проверяется, существует ли допустимый маршрут от текущего города к начальному городу
            if points[current_city][0] != 0:
                # текущее расстояние увеличивается на расстояние от текущего города до начального города
                current_distance += points[current_city][0]
                # Если текущее расстояние меньше кратчайшего расстояния, то кратчайшее расстояние и путь обновляются
                if current_distance < shortest_distance:
                    shortest_distance = current_distance
                    shortest_path = path[:]
            return

        # Если максимальная глубина не достигнута, цикл по всем городам
        for i in range(num_cities):
            # Для каждого города проверяется, не посещался ли он ранее и существует ли допустимый маршрут от текущего города1 до города2
            if not visited[i] and points[current_city][i] != 0:
                path.append(i)  # Для каждого допустимого города_i он добавляется в путь
                visited[i] = True  # отмечается как посещенный
                tsp_helper(i, current_distance + points[current_city][i], depth + 1)  # повторяем
                visited[i] = False  # город помечается как непосещенный
                path.pop()  # удаляется из пути

    path.append(0)  # начальный город помечается как посещенный
    visited[0] = True
    tsp_helper(0, 0, 1)

    if shortest_path:
        shortest_path = [sp + 1 for sp in shortest_path]

    # Вот и все! Возвращаются кратчайшее расстояние и кратчайший путь
    return shortest_distance, shortest_path


def init_tk() -> tk.PanedWindow:
    def solve_tsp_button_click():
        num_cities = int(num_cities_entry.get())
        distances = [[0 for _ in range(num_cities)] for _ in range(num_cities)]

        for i in range(num_cities):
            for j in range(num_cities):
                entry: tk.Entry = distance_entries[i][j]
                if entry.get().isnumeric():
                    distances[i][j] = int(entry.get())
                else:
                    distances[i][j] = 0

        # Exclude routes from a city to itself
        for i in range(num_cities):
            distances[i][i] = 0

        shortest_distance, shortest_path = solve_tsp(distances)

        result_text.set(f"Shortest Distance: {shortest_distance}\n" f"Shortest Path: {shortest_path}")

    def create_distance_entries(num_cities):
        for i in range(num_cities):
            row_entries = []
            for j in range(num_cities):
                if i == j:
                    entry = tk.Entry(window)
                    entry.insert(tk.END, "X")  # Prefill entry with "X"
                else:
                    entry = tk.Entry(window)
                entry.grid(row=i + 2, column=j + 1, padx=5, pady=5)
                row_entries.append(entry)
            distance_entries.append(row_entries)

    window = tk.Tk()
    window.title("TSP Solver")

    # Create the input widgets
    num_cities_label = tk.Label(window, text="Number of Cities:")
    num_cities_label.grid(row=0, column=0, padx=5, pady=5)

    num_cities_entry = tk.Entry(window)
    num_cities_entry.grid(row=0, column=1, padx=5, pady=5)

    distance_entries = []

    def update_distance_entries():
        nonlocal distance_entries
        for row in distance_entries:
            for entry in row:
                entry.destroy()
        distance_entries = []
        num_cities = int(num_cities_entry.get())
        create_distance_entries(num_cities)

    update_button = tk.Button(window, text="Update", command=update_distance_entries)
    update_button.grid(row=0, column=2, padx=5, pady=5)

    solve_button = tk.Button(window, text="Solve TSP", command=solve_tsp_button_click)
    solve_button.grid(row=1, column=0, columnspan=10, padx=5, pady=10)

    result_text = tk.StringVar()
    result_label = tk.Label(window, textvariable=result_text)
    result_label.grid(row=8, column=0, columnspan=10, padx=5, pady=10)

    return window


if __name__ == "__main__":
    window = init_tk()
    window.mainloop()
