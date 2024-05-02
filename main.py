from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import random
import sys

# 初期化
pygame.init()

# 画面の設定
WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("stone Run")

# 色の設定
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# フォントの設定
FONT = pygame.font.SysFont(None, 40)

# 画像の読み込み
stone_img = pygame.image.load("stone.png")
stone_img = pygame.transform.scale(stone_img, (60, 60))
obstacle_img = pygame.image.load("tree.png")
obstacle_img = pygame.transform.scale(obstacle_img, (60, 60))

# ゲームの設定
GRAVITY = 0.6
DINO_JUMP = -15
OBSTACLE_SPEED = 5
OBSTACLE_FREQUENCY = 80

class Dino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.jump_strength = DINO_JUMP
        self.rect = stone_img.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity = self.jump_strength

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

        if self.y >= HEIGHT - self.rect.height:
            self.y = HEIGHT - self.rect.height
            self.velocity = 0
            self.is_jumping = False

        self.rect.topleft = (self.x, self.y)

    def draw(self):
        WIN.blit(stone_img, (self.x, self.y))

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = obstacle_img.get_rect()
        self.rect.topleft = (self.x, self.y)

    def update(self):
        self.x -= OBSTACLE_SPEED
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        WIN.blit(obstacle_img, (self.x, self.y))

def main():
    global OBSTACLE_FREQUENCY
    clock = pygame.time.Clock()
    dino = Dino(60, HEIGHT - 100)
    obstacles = []

    score = 0
    obstacle_counter = 0
    game_started = False  # ゲームの開始状態

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game_started:  # スペースキーでゲームを開始
                        game_started = True
                    dino.jump()

        if game_started:
            WIN.fill(WHITE)

            # 障害物を追加
            if obstacle_counter == OBSTACLE_FREQUENCY:
                OBSTACLE_FREQUENCY = random.randint(20,90)
                obstacle_counter = 0
                obstacle = Obstacle(WIDTH, HEIGHT - 60)
                obstacles.append(obstacle)

            # 障害物の更新と描画
            for obstacle in obstacles:
                obstacle.update()
                obstacle.draw()

                if obstacle.x < -obstacle.rect.width:
                    obstacles.remove(obstacle)
                    score += 1

                if dino.rect.colliderect(obstacle.rect):
                    
                    # 繰り返し
                    main()

            # 恐竜の更新と描画
            dino.update()
            dino.draw()

            # スコアの表示
            score_text = FONT.render(f"Score: {score}", True, BLACK)
            WIN.blit(score_text, (10, 10))

        else:
            # ゲームが開始されていない場合は、スタートメッセージを表示
            start_text = FONT.render("Press SPACE to start", True, BLACK)
            score_text = FONT.render(f"Score: {score}",True,BLACK)
            WIN.fill(WHITE)  # ゲーム開始前の背景を白にする
            WIN.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - start_text.get_height() // 2))
           # WIN.blit(score_text,(10,10))

        pygame.display.flip()
        clock.tick(60)
        obstacle_counter += 1

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
