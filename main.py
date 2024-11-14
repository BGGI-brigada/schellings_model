import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.colors as colors

n = 50
empty_ratio = 0.10
red_ratio = 0.45
blue_ratio = 0.45
num_steps = 1000
similarity_threshold = 2

def create_grid(n, empty_ratio, red_ratio, blue_ratio):
    total_cells = n * n
    num_empty = int(empty_ratio * total_cells)
    num_red = int(red_ratio * total_cells)
    num_blue = total_cells - num_empty - num_red
    cells = [0] * num_empty + [1] * num_red + [2] * num_blue
    random.shuffle(cells)
    grid = np.array(cells).reshape((n, n))
    return grid

def is_happy(grid, x, y, threshold):
    cell = grid[x, y]
    if cell == 0:
        return True
    similar_neighbors = 0
    total_neighbors = 0
    neighbors = [(-1, -1), (-1, 0), (-1, 1),
                 (0, -1),          (0, 1),
                 (1, -1),  (1, 0), (1, 1)]
    for dx, dy in neighbors:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < n:
            neighbor = grid[nx, ny]
            if neighbor != 0:
                total_neighbors += 1
                if neighbor == cell:
                    similar_neighbors += 1
    if total_neighbors == 0:
        return True
    return similar_neighbors >= threshold

def plot_grid(grid, step):
    plt.figure(figsize=(6, 6))
    cmap = colors.ListedColormap(['white', 'red', 'blue'])
    plt.imshow(grid, cmap=cmap, interpolation='none')
    plt.title(f"Шаг {step}")
    plt.axis('off')
    plt.show()

def segregation_index(grid):
    segregation = []
    for x in range(n):
        for y in range(n):
            cell = grid[x, y]
            if cell == 0:
                continue
            similar_neighbors = 0
            total_neighbors = 0
            neighbors = [(-1, -1), (-1, 0), (-1, 1),
                         (0, -1),          (0, 1),
                         (1, -1),  (1, 0), (1, 1)]
            for dx, dy in neighbors:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < n:
                    neighbor = grid[nx, ny]
                    if neighbor != 0:
                        total_neighbors += 1
                        if neighbor == cell:
                            similar_neighbors += 1
            if total_neighbors > 0:
                segregation.append(similar_neighbors / total_neighbors)
    return np.mean(segregation)

def simulate(grid, num_steps, threshold):
    empty_cells = list(zip(*np.where(grid == 0)))
    segregation_indices = []
    for step in range(1, num_steps + 1):
        unhappy_cells = []
        for x in range(n):
            for y in range(n):
                if grid[x, y] != 0 and not is_happy(grid, x, y, threshold):
                    unhappy_cells.append((x, y))
        if not unhappy_cells:
            print(f"Моделирование завершено на шаге {step}, все клетки счастливы.")
            break
        x, y = random.choice(unhappy_cells)
        if not empty_cells:
            print("Нет доступных пустых клеток для перемещения.")
            break
        new_x, new_y = random.choice(empty_cells)
        grid[new_x, new_y] = grid[x, y]
        grid[x, y] = 0
        empty_cells.remove((new_x, new_y))
        empty_cells.append((x, y))
        seg_index = segregation_index(grid)
        segregation_indices.append(seg_index)
        if step % (num_steps // 5) == 0 or step == 1 or step == num_steps:
            plot_grid(grid, step)
            print(f"Шаг {step}, индекс сегрегации: {seg_index:.4f}")
    plot_grid(grid, step)
    print(f"Итоговый индекс сегрегации: {segregation_index(grid):.4f}")
    plt.figure()
    plt.plot(segregation_indices)
    plt.xlabel('Шаг моделирования')
    plt.ylabel('Индекс сегрегации')
    plt.title('Изменение индекса сегрегации во времени')
    plt.show()

grid = create_grid(n, empty_ratio, red_ratio, blue_ratio)
simulate(grid, num_steps, similarity_threshold)
