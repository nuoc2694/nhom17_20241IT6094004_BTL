import pygame
from maze import create_maze
from astar import astar

# Kích thước mê cung
WIDTH = HEIGHT = 65  # Mê cung là hình vuông, rộng và cao đều là 65 ô

# Kích thước mỗi ô
BLOCK_SIZE = int(720 // WIDTH)  # Kích thước ô được tính sao cho mê cung vừa khung hình 720x720

# Tọa độ lối vào và lối ra
ENTRY = (1, 0)  # Lối vào tại cột thứ 1 hàng thứ 0
EXIT = (WIDTH - 2, HEIGHT - 1)  # Lối ra tại cột thứ 63, hàng thứ 64

# Tạo mê cung
maze = create_maze(WIDTH, HEIGHT, ENTRY, EXIT)

# Cài đặt pygame
pygame.init()  # Khởi tạo PyGame
WINDOW_WIDTH = WIDTH * BLOCK_SIZE * 2  # Chiều ngang cửa sổ (2 phần: người chơi và A*)
WINDOW_HEIGHT = HEIGHT * BLOCK_SIZE  # Chiều cao cửa sổ
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)  # Kích thước cửa sổ
WINDOW = pygame.display.set_mode(WINDOW_SIZE)  # Thiết lập cửa sổ hiển thị
pygame.display.set_caption("Trò chơi mê cung : Player vs A*")  # Đặt tên cho cửa sổ

# Màu sắc
BLACK = (0, 0, 0)  # Màu tường
WHITE = (255, 255, 255)  # Màu đường đi
BLUE = (0, 0, 255)  # Màu người chơi
GREEN = (0, 255, 0)  # Màu đường đi của A*
RED = (255, 0, 0)  # Màu đích

# Khởi tạo vị trí người chơi và A*
player_pos = list(ENTRY)  # Vị trí hiện tại của người chơi (lấy từ ENTRY)
astar_path = astar(maze, ENTRY, EXIT)  # Đường đi được tính toán bởi thuật toán A*
astar_index = 0  # Bước hiện tại của A*

# Vẽ mê cung và điểm kết thúc
def draw_maze(surface, offset_x):
    """Vẽ mê cung trên cửa sổ."""
    for y in range(HEIGHT):
        for x in range(WIDTH):
            color = WHITE if maze[y][x] == 0 else BLACK  # Trắng cho đường đi, đen cho tường
            pygame.draw.rect(surface, color, (x * BLOCK_SIZE + offset_x, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    # Vẽ điểm kết thúc (lối ra)
    pygame.draw.rect(surface, RED, (EXIT[0] * BLOCK_SIZE + offset_x, EXIT[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Kích thước viewport (10% kích thước mê cung)
VIEWPORT_WIDTH = max(3, WIDTH // 10)  # Ít nhất là 3 ô
VIEWPORT_HEIGHT = max(3, HEIGHT // 10)  # Ít nhất là 3 ô

# Tính toán vị trí viewport nhằm căn giữa người chơi
def calculate_viewport():
    x, y = player_pos
    half_width = VIEWPORT_WIDTH // 2
    half_height = VIEWPORT_HEIGHT // 2

    # Giới hạn viewport không vượt ra ngoài mê cung
    start_x = max(0, min(WIDTH - VIEWPORT_WIDTH, x - half_width))
    start_y = max(0, min(HEIGHT - VIEWPORT_HEIGHT, y - half_height))
    return start_x, start_y

# Vẽ mê cung trong viewport 
def draw_maze_with_viewport(surface, viewport_x, viewport_y):
    for y in range(viewport_y, viewport_y + VIEWPORT_HEIGHT):
        for x in range(viewport_x, viewport_x + VIEWPORT_WIDTH):
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                color = WHITE if maze[y][x] == 0 else BLACK
                draw_x = (x - viewport_x) * BLOCK_SIZE * SCALE_FACTOR
                draw_y = (y - viewport_y) * BLOCK_SIZE * SCALE_FACTOR
                pygame.draw.rect(surface, color, (draw_x, draw_y, BLOCK_SIZE * SCALE_FACTOR, BLOCK_SIZE * SCALE_FACTOR))

    # Vẽ điểm kết thúc nếu nằm trong viewport
    if viewport_x <= EXIT[0] < viewport_x + VIEWPORT_WIDTH and viewport_y <= EXIT[1] < viewport_y + VIEWPORT_HEIGHT:
        draw_x = (EXIT[0] - viewport_x) * BLOCK_SIZE * SCALE_FACTOR
        draw_y = (EXIT[1] - viewport_y) * BLOCK_SIZE * SCALE_FACTOR
        pygame.draw.rect(surface, RED, (draw_x, draw_y, BLOCK_SIZE * SCALE_FACTOR, BLOCK_SIZE * SCALE_FACTOR))

# Vẽ người chơi trong viewport
def draw_player_with_viewport(surface, viewport_x, viewport_y):
    """Vẽ người chơi trong viewport (phóng to)."""
    draw_x = (player_pos[0] - viewport_x) * BLOCK_SIZE * SCALE_FACTOR
    draw_y = (player_pos[1] - viewport_y) * BLOCK_SIZE * SCALE_FACTOR
    pygame.draw.rect(surface, BLUE, (draw_x, draw_y, BLOCK_SIZE * SCALE_FACTOR, BLOCK_SIZE * SCALE_FACTOR))



# Vẽ đường đi A* đến vị trí hiện tại
def draw_astar(surface, index, offset_x):
    """Vẽ các bước đường đi của A* đến bước hiện tại."""
    for step in astar_path[:index]:
        pygame.draw.rect(surface, GREEN, (step[0] * BLOCK_SIZE + offset_x, step[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


# Di chuyển người chơi một ô khi nhấn một lần phím
def move_player(direction):
    """Di chuyển người chơi dựa trên hướng phím bấm."""
    x, y = player_pos
    if direction == pygame.K_UP and maze[y - 1][x] == 0:  # Di chuyển lên nếu không phải tường
        player_pos[1] -= 1
    elif direction == pygame.K_DOWN and maze[y + 1][x] == 0:  # Di chuyển xuống
        player_pos[1] += 1
    elif direction == pygame.K_LEFT and maze[y][x - 1] == 0:  # Di chuyển trái
        player_pos[0] -= 1
    elif direction == pygame.K_RIGHT and maze[y][x + 1] == 0:  # Di chuyển phải
        player_pos[0] += 1

# Kiểm tra xem ai là người đến lối ra trước
def check_winner():
    """Kiểm tra nếu người chơi hoặc A* đã đến đích."""
    if tuple(player_pos) == EXIT:
        return "Player"  # Người chơi thắng
    if astar_index < len(astar_path) and astar_path[astar_index] == EXIT:
        return "A*"  # A* thắng
    return None

# Vòng lặp chính
running = True  # Biến điều khiển vòng lặp chính
clock = pygame.time.Clock()  # Đồng hồ để điều khiển tốc độ khung hình
astar_timer = 0  # Thời gian giữa các bước di chuyển của A*
key_hold_timer = 0  # Thời gian giữ phím
key_last_pressed = None  # Lưu phím cuối cùng được nhấn
astar_speed = 100  # Tốc độ di chuyển của A* (ms)
sensitivity = 250  # Độ nhạy khi giữ phím (ms)
player_speed = 200  # Tốc độ di chuyển khi giữ phím (ms)
SCALE_FACTOR = 11   # Phóng tầm nhìn người chơi

while running:
    delta_time = clock.get_time()  # Thời gian giữa các khung hình
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            key_last_pressed = event.key  # Ghi lại phím đang nhấn
            key_hold_timer = 0  # Reset bộ đếm thời gian giữ phím
            move_player(event.key)  # Di chuyển ngay lập tức

        if event.type == pygame.KEYUP:
            if event.key == key_last_pressed:
                key_last_pressed = None  # Hủy theo dõi nếu phím được nhả

    # Nếu một phím được giữ, tiếp tục di chuyển theo thời gian
    if key_last_pressed:
        key_hold_timer += delta_time
        if key_hold_timer >= sensitivity:  # Nếu giữ phím đủ lâu
            move_player(key_last_pressed)  # Di chuyển người chơi
            key_hold_timer = player_speed  # Reset bộ đếm để di chuyển nhanh hơn

    # Di chuyển A* nếu thời gian đã đủ
    astar_timer += delta_time
    if astar_timer >= astar_speed and astar_index < len(astar_path):
        astar_index += 1  # Chuyển sang bước tiếp theo của A*
        astar_timer = 0  # Reset bộ đếm thời gian của A*

    # Kiểm tra kết thúc trò chơi
    winner = check_winner()
    if winner:
        print(f"{winner} đã đến đích trước!")
        running = False

    # Tính toán viewport
    viewport_x, viewport_y = calculate_viewport()

    # Vẽ phần viewport (phóng to)
    WINDOW.fill(WHITE)
    draw_maze_with_viewport(WINDOW, viewport_x, viewport_y)
    draw_player_with_viewport(WINDOW, viewport_x, viewport_y)

    # Vẽ phần A* bên phải (không thay đổi)
    draw_maze(WINDOW, WIDTH * BLOCK_SIZE)
    draw_astar(WINDOW, astar_index, WIDTH * BLOCK_SIZE)

    pygame.display.update()  # Cập nhật màn hình

    # Điều chỉnh tốc độ khung hình
    clock.tick(120)

pygame.quit()
