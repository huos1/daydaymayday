import pygame
import random
import os

# 初始化Pygame
pygame.init()

# 设置游戏窗口大小
screen_width, screen_height = 1000, 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('daydaymayday')

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)  # 光圈颜色，黄色

# 定义游戏参数
block_size = 70  # 初始图案大小
block_padding = 10
time_limit = 200
slot_limit = 7
current_level = 1
selected_mode = None  # 当前选择的模式
leaderboard = []  # 排行榜数据

# 加载支持中文的字体
font_path = 'STKAITI.TTF'  # 检查字体路径是否正确
font = pygame.font.Font(font_path, 48)  # 加载字体并设置字号

# 加载背景图片，并调整为适应屏幕大小
menu_background = pygame.transform.scale(pygame.image.load('background1.png'), (screen_width, screen_height))
game_background = pygame.transform.scale(pygame.image.load('background2.png'), (screen_width, screen_height))
end_background = pygame.transform.scale(pygame.image.load('background3.png'), (screen_width, screen_height))
mode_selection_background = pygame.transform.scale(pygame.image.load('background4.png'), (screen_width, screen_height))
leaderboard_background = pygame.transform.scale(pygame.image.load('background5.png'), (screen_width, screen_height))
# 加载成功和失败的背景图片
success_background = pygame.transform.scale(pygame.image.load('success_background.png'), (screen_width, screen_height))
failure_background = pygame.transform.scale(pygame.image.load('failure_background.png'), (screen_width, screen_height))

# 计算槽的背景图尺寸，槽的宽度要刚好可以放下 7 个图案
slot_width = (block_size + block_padding) * slot_limit - block_padding
slot_background = pygame.transform.scale(pygame.image.load('back.png'), (slot_width, block_size))

# 加载圆形图案集合函数
def load_patterns(mode, block_size):
    patterns = []
    folder_path = f"mode{mode}"  # 根据选择的模式加载对应文件夹
    for i in range(1, 7):
        pattern_path = os.path.join(folder_path, f"pattern_{i}.png")
        pattern_image = pygame.image.load(pattern_path)
        pattern_image = pygame.transform.scale(pattern_image, (block_size, block_size))  # 调整图案大小
        patterns.append(pattern_image)
    return patterns

# 定义方块类
class Block:
    def __init__(self, x, y, pattern_index, layer):
        # 在创建方块时，应用随机偏移
        offset_x = random.randint(-40, 40)  # 调整图案随机位置偏移
        offset_y = random.randint(-40, 40)
        self.rect = pygame.Rect(x + offset_x, y + offset_y, block_size, block_size)
        self.pattern_index = pattern_index
        self.clicked = False
        self.layer = layer
        self.mask = pygame.mask.from_surface(patterns[self.pattern_index])  # 为每个图案生成遮罩

# 在主菜单函数中进行修改

# 主菜单函数
def main_menu():
    menu_running = True
    
    # 加载字体背景图片
    font_background = pygame.image.load('font_background.png')  # 替换为你自己的背景图片路径

    while menu_running:
        # 绘制菜单背景
        screen.blit(menu_background, (0, 0))

        # 渲染文本
        title_text = font.render("DAYDAYMAYDAY", True, BLACK)
        play_text = font.render("开始游戏", True, BLACK)
        leaderboard_text = font.render("排行榜", True, BLACK)
        quit_text = font.render("退出游戏", True, BLACK)

        # 获取字体背景图片的大小，并调整背景图片的大小以适应文本
        play_background = pygame.transform.scale(font_background, (play_text.get_width(), play_text.get_height()))
        leaderboard_background = pygame.transform.scale(font_background, (leaderboard_text.get_width(), leaderboard_text.get_height()))
        quit_background = pygame.transform.scale(font_background, (quit_text.get_width(), quit_text.get_height()))

        # 在字体显示位置之前绘制背景
        screen.blit(play_background, (screen_width // 2 - play_text.get_width() // 2, 300))
        screen.blit(leaderboard_background, (screen_width // 2 - leaderboard_text.get_width() // 2, 400))
        screen.blit(quit_background, (screen_width // 2 - quit_text.get_width() // 2, 500))

        # 绘制文本
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 200))
        screen.blit(play_text, (screen_width // 2 - play_text.get_width() // 2, 300))
        screen.blit(leaderboard_text, (screen_width // 2 - leaderboard_text.get_width() // 2, 400))
        screen.blit(quit_text, (screen_width // 2 - quit_text.get_width() // 2, 500))

        pygame.display.flip()

        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_text.get_rect(topleft=(screen_width // 2 - play_text.get_width() // 2, 300)).collidepoint(mouse_pos):
                    menu_running = False  # 进入模式选择
                elif leaderboard_text.get_rect(topleft=(screen_width // 2 - leaderboard_text.get_width() // 2, 400)).collidepoint(mouse_pos):
                    show_leaderboard()  # 显示排行榜
                elif quit_text.get_rect(topleft=(screen_width // 2 - quit_text.get_width() // 2, 500)).collidepoint(mouse_pos):
                    pygame.quit()
                    quit()  # 退出游戏


# 显示排行榜函数
def show_leaderboard():
    running = True
    while running:
        screen.blit(leaderboard_background, (0, 0))  # 绘制排行榜背景
        title_text = font.render("排行榜", True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 100))

        # 排行榜数据按时间排序
        sorted_leaderboard = sorted(leaderboard, key=lambda x: x[1])

        # 显示排行榜前 5 名
        for i, (name, score) in enumerate(sorted_leaderboard[:5]):
            entry_text = font.render(f"{i + 1}. {name}: {score:.2f} 秒", True, BLACK)
            screen.blit(entry_text, (screen_width // 2 - entry_text.get_width() // 2, 200 + i * 50))

        back_text = font.render("返回主菜单", True, BLACK)
        screen.blit(back_text, (screen_width // 2 - back_text.get_width() // 2, 500))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_text.get_rect(topleft=(screen_width // 2 - back_text.get_width() // 2, 500)).collidepoint(mouse_pos):
                    running = False  # 返回主菜单

# 模式选择函数
def mode_selection():
    mode_running = True

    while mode_running:
        screen.blit(mode_selection_background, (0, 0))  # 绘制模式选择背景
        
        title_text = font.render("选择模式", True, BLACK)
        mode_texts = [font.render(f"模式 {i+1}", True, BLACK) for i in range(6)]

        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 100))

        for i, mode_text in enumerate(mode_texts):
            screen.blit(mode_text, (screen_width // 2 - mode_text.get_width() // 2, 200 + i * 80))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, mode_text in enumerate(mode_texts):
                    if mode_text.get_rect(topleft=(screen_width // 2 - mode_text.get_width() // 2, 200 + i * 80)).collidepoint(mouse_pos):
                        global selected_mode
                        selected_mode = i + 1  # 选择的模式
                        mode_running = False
                        return




# 创建网格函数，生成位置向中心靠拢
def create_grid(level):
    if level == 1:
        num_blocks_per_row = 6
        num_blocks_per_col = 6
        num_layers = 3
    elif level == 2:
        num_blocks_per_row = 9
        num_blocks_per_col = 9
        num_layers = 3
        global block_size
        block_size = 60  # 适应第二关的图案大小

    grid = [[[None for _ in range(num_blocks_per_col)] for _ in range(num_blocks_per_row)] for _ in range(num_layers)]
    pattern_combinations = []
    total_blocks = num_blocks_per_row * num_blocks_per_col * num_layers

    for _ in range(total_blocks // 3):
        pattern_index = random.randint(0, 5)
        pattern_combinations.extend([pattern_index] * 3)

    while len(pattern_combinations) < total_blocks:
        pattern_combinations.append(random.randint(0, 5))

    random.shuffle(pattern_combinations)  # 打乱图案分布顺序，增加随机性

    center_x = screen_width // 2 - (num_blocks_per_row * (block_size + block_padding)) // 2
    center_y = screen_height // 2 - (num_blocks_per_col * (block_size + block_padding)) // 2

    for layer in range(num_layers):
        for row in range(num_blocks_per_row):
            for col in range(num_blocks_per_col):
                pattern_index = pattern_combinations.pop(0)
                grid[layer][row][col] = Block(center_x + col * (block_size + block_padding),
                                              center_y + row * (block_size + block_padding),
                                              pattern_index, layer)
    
    return grid

# 使用遮罩进行碰撞检测，确保遮挡时图案不可点击
def is_clickable(grid, block):
    if block.layer == len(grid) - 1:
        return True

    above_layer = grid[block.layer + 1]
    for row in above_layer:
        for above_block in row:
            if above_block and above_block.pattern_index is not None:
                offset_x = block.rect.x - above_block.rect.x
                offset_y = block.rect.y - above_block.rect.y
                if above_block.mask.overlap(block.mask, (offset_x, offset_y)):
                    return False
    return True

# 消除匹配的方块
def remove_matched_blocks(selected_blocks):
    pattern_count = {}
    for block in selected_blocks:
        pattern_count[block.pattern_index] = pattern_count.get(block.pattern_index, 0) + 1

    matched_blocks = [block for block in selected_blocks if pattern_count[block.pattern_index] >= 3]

    if len(matched_blocks) >= 3:
        for block in matched_blocks:
            selected_blocks.remove(block)
        return True
    return False

# 结束页面
def end_screen(message, success):
    end_running = True

    # 根据游戏结果选择背景图片
    if success:
        screen.blit(success_background, (0, 0))  # 成功时显示成功背景
    else:
        screen.blit(failure_background, (0, 0))  # 失败时显示失败背景

    while end_running:
        end_text = font.render(message, True, BLACK)
        retry_text = font.render("重新开始", True, BLACK)
        quit_text = font.render("退出游戏", True, BLACK)

        screen.blit(end_text, (screen_width // 2 - end_text.get_width() // 2, 200))
        screen.blit(retry_text, (screen_width // 2 - retry_text.get_width() // 2, 300))
        screen.blit(quit_text, (screen_width // 2 - quit_text.get_width() // 2, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if retry_text.get_rect(topleft=(screen_width // 2 - retry_text.get_width() // 2, 300)).collidepoint(mouse_pos):
                    global current_level, block_size, slot_width, slot_background  # 重新开始游戏时重置关卡和图案大小
                    current_level = 1  
                    block_size = 70  
                    # 重新计算槽的宽度
                    slot_width = (block_size + block_padding) * slot_limit - block_padding
                    slot_background = pygame.transform.scale(pygame.image.load('back.png'), (slot_width, block_size))  # 重新计算槽背景尺寸
                    return True  # 重新开始游戏
                elif quit_text.get_rect(topleft=(screen_width // 2 - quit_text.get_width() // 2, 400)).collidepoint(mouse_pos):
                    pygame.quit()
                    quit()  # 退出游戏

# 游戏循环函数
def game_loop():
    running = True
    clock = pygame.time.Clock()

    global current_level
    global block_size
    global patterns
    global slot_width, slot_background  # 添加对槽宽度和槽背景的全局访问权限

    patterns = load_patterns(selected_mode, block_size)  # 根据选择的模式加载图案
    grid = create_grid(current_level)
    selected_blocks = []
    start_ticks = pygame.time.get_ticks()

    while running:
        screen.blit(game_background, (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for layer in grid:
                    for row in layer:
                        for block in row:
                            if block and not block.clicked and block.rect.collidepoint(mouse_pos):
                                if is_clickable(grid, block):
                                    if len(selected_blocks) < slot_limit:
                                        selected_blocks.append(Block(0, 0, block.pattern_index, block.layer))
                                        block.clicked = True
                                        block.pattern_index = None
                                        remove_matched_blocks(selected_blocks)
                                break

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    grid = create_grid(current_level)  # 关卡刷新
                    start_ticks = pygame.time.get_ticks()  # 时间重置
                    selected_blocks.clear()  # 槽清空

                if event.key == pygame.K_u:
                    selected_blocks.clear()  # 按下U键直接消除槽里的图案

        if len(selected_blocks) == slot_limit:
            if not remove_matched_blocks(selected_blocks):
                if end_screen("游戏结束！",success=False):                    
                    return True  # 重新开始游戏
                else:
                    return False  # 退出游戏

        all_cleared = True

        # 先绘制方块的图案
        for layer in grid:
            for row in layer:
                for block in row:
                    if block and block.pattern_index is not None:
                        screen.blit(patterns[block.pattern_index], block.rect)
                        all_cleared = False

        # 绘制光圈，并确保光圈大小与图案匹配
        for layer in grid:
            for row in layer:
                for block in row:
                    if block and block.pattern_index is not None and is_clickable(grid, block):
                        if block.rect.collidepoint(mouse_pos):
                            pygame.draw.circle(screen, YELLOW, block.rect.center, block.rect.width // 2 + 5, 4)  # 调整光圈大小

        # 当进入第二关时，重新调整槽的宽度和背景大小
        if current_level == 2:
            slot_width = (block_size + block_padding) * slot_limit - block_padding  # 根据新的图案大小重新计算槽的宽度
            slot_background = pygame.transform.scale(pygame.image.load('back.png'), (slot_width, block_size))  # 调整槽背景

        # 绘制槽背景
        slot_start_x = (screen_width - slot_width) // 2
        slot_y = screen_height - block_size - 50
        screen.blit(slot_background, (slot_start_x, slot_y))  # 绘制槽背景

        # 显示选中的方块
        for i, block in enumerate(selected_blocks):
            slot_x = slot_start_x + i * (block_size + block_padding)
            screen.blit(patterns[block.pattern_index], (slot_x, slot_y))

        # 显示计时器
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        font = pygame.font.SysFont(None, 36)
        time_text = font.render(f"Time: {seconds}/{time_limit}", True, BLACK)
        screen.blit(time_text, (10, 10))

        # 当游戏时间用尽时调用失败背景
        if seconds > time_limit:
            if end_screen("时间用尽！", success=False):  # 失败背景
                return True  # 重新开始游戏
            else:
                return False  # 退出游戏

        if all_cleared:
            if current_level == 1:
                current_level = 2
                block_size = 60  # 调整第二关图案大小
                patterns = load_patterns(selected_mode, block_size)  # 重新加载图案
                grid = create_grid(current_level)
                start_ticks = pygame.time.get_ticks()
                print("恭喜！进入第二关 9x9！")
            else:
                completion_time = (pygame.time.get_ticks() - start_ticks) / 1000
                leaderboard.append(("玩家", completion_time))  # 添加到排行榜
                if end_screen("恭喜通关！", success=True):
                    return True  # 重新开始游戏
                else:
                    return False  # 退出游戏

        pygame.display.flip()
        clock.tick(60)
        
# 程序入口
if __name__ == "__main__":
    while True:
        main_menu()  # 先显示主菜单
        mode_selection()  # 选择模式
        if not game_loop():  # 如果游戏结束时返回False，退出游戏
            break
    pygame.quit()