import heapq

# Hàm tính khoảng cách Euclid giữa hai điểm.
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# Hàm tìm đường đi ngắn nhất từ lối vào đến lối ra bằng thuật toán A*
def astar(maze, entry, exit):
    # Các hướng di chuyển (phải, dưới, trái, trên)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # Hàng đợi ưu tiên
    queue = [(0, entry)]
    # Điểm đã thăm
    visited = set()
    # Điểm trước đó
    previous = {entry: None}

    # Chi phí di chuyển đến điểm hiện tại
    cost = {entry: 0}

    while queue:
        # Lấy điểm có chi phí thấp nhất
        _, current = heapq.heappop(queue)

        # Đã tìm thấy lối ra
        if current == exit:
            path = []
            while current:
                path.append(current)
                current = previous[current]
            return path[::-1]

        # Điểm đã thăm
        visited.add(current)

        # Kiểm tra các hướng
        for dx, dy in directions:
            nx, ny = current[0] + dx, current[1] + dy

            # Hợp lệ và chưa thăm
            if (0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and
                    maze[ny, nx] == 0 and (nx, ny) not in visited):
                # Tính chi phí
                new_cost = cost[current] + 1
                # Cập nhật chi phí và điểm trước đó
                if (nx, ny) not in cost or new_cost < cost[(nx, ny)]:
                    cost[(nx, ny)] = new_cost
                    priority = new_cost + heuristic(exit, (nx, ny))
                    heapq.heappush(queue, (priority, (nx, ny)))
                    previous[(nx, ny)] = current

    # Không tìm thấy đường đi
    return None

