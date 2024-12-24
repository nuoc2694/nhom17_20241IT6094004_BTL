import numpy as np
import random

# Tạo mê cung với kích thước cho trước và lối vào/ra
def create_maze(width, height, entry, exit):
    # Tạo ma trận mê cung với tất cả các ô là tường (1)
    maze = np.ones((height, width), dtype=int)

    # Hướng di chuyển (phải, dưới, trái, trên)
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]

    def is_valid_cell(x, y):
        # Kiểm tra xem ô có hợp lệ không
        return 0 < x < width - 1 and 0 < y < height - 1 and maze[y, x] == 1

    def generate_maze(x, y):
        stack = [(x, y)]
        maze[y, x] = 0  # Đặt ô hiện tại là đường đi

        while stack:
            cx, cy = stack[-1]
            random.shuffle(directions)  # Ngẫu nhiên hóa thứ tự duyệt

            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if is_valid_cell(nx, ny):
                    maze[cy + dy // 2, cx + dx // 2] = 0  # Phá tường giữa hai ô
                    maze[ny, nx] = 0  # Đặt ô tiếp theo là đường đi
                    stack.append((nx, ny))
                    break
            else:
                stack.pop()

            # Tạo đường cụt sâu với xác suất nhất định
            if random.random() < 0.5:  # 50% cơ hội tạo đường cụt
                for dx, dy in directions:
                    nx, ny = cx + dx, cy + dy
                    if is_valid_cell(nx, ny) and np.sum(maze[ny-1:ny+2, nx-1:nx+2]) == 1:
                        maze[ny, nx] = 0  # Tạo thành đường cụt

    # Bắt đầu từ ô (1, 1)
    generate_maze(1, 1)

    # Thêm lối vào và lối ra
    maze[entry[1], entry[0]] = 0  # Lối vào
    maze[exit[1], exit[0]] = 0  # Lối ra

    return maze
