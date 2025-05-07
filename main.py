import pygame as pg
import pygame_menu


pg.init()
pg.mixer.init()
pg.font.init()


class GameSprite(pg.sprite.Sprite):
    def __init__(self, filename, x, y, width, height, speed):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(filename), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def draw(self):
        window.blit(self.image, self.rect)
class Platform(GameSprite):
    def updateL(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_DOWN] and self.rect.bottom < (H):
            self.rect.y += self.speed
        if keys[pg.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
    def updateR(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_s] and self.rect.bottom < (H):
            self.rect.y += self.speed
        if keys[pg.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
class Ball(GameSprite):
    def __init__(self, filename, x, y, width, height, speed_x, speed_y):
        self.image = pg.transform.scale(pg.image.load(filename), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.bottom >= (H) or self.rect.top <= 0:
            self.speed_y *= -1


W, H = (1920, 1080)
BLACK = (0, 0, 0)
FPS = 360
clock = pg.time.Clock()
BACK_IMAGE = pg.transform.scale(pg.image.load('YellowBackground.jpg'), (W, H))
window = pg.display.set_mode((W, H))
pg.display.set_caption('Понг')
playerL = Platform('platform.png', 100, 540, 50, 150, 2)
playerR = Platform('platform.png', 1820, 540, 50, 150, 2)
ball = Ball('ball.png', W/2, H/2, 50, 50, 2, 2)
players = pg.sprite.Group()
players.add(playerL, playerR)
collide = pg.mixer.Sound('zvuk-udara-po-myachiku.mp3')
fsize = 50


def main():
    pg.mixer.music.load('gamemusic.mp3')
    font = pg.font.SysFont('Arial', fsize)
    text = font.render('Счёт: 0', True, BLACK)
    score = 0
    pg.mixer.music.set_volume(0.2)
    pg.mixer.music.play(10)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        window.blit(BACK_IMAGE, (0, 0))
        window.blit(text, (W - 300, 50))
        playerL.draw()
        playerL.updateL()
        playerR.draw()
        playerR.updateR()
        ball.draw()
        ball.update()
        if pg.sprite.spritecollide(ball, players, False):
            ball.speed_x *= -1
            collide.set_volume(0.2)
            collide.play()
            score += 1
            text = font.render('Счёт: ' + str(score), True, BLACK)
        if ball.rect.left <= 0:
            pg.mixer.music.stop()
            end_menu('Player 1', 'Player 2')
        elif ball.rect.right >= W:
            pg.mixer.music.stop()
            end_menu('Player 2', 'Player 1')   
        pg.display.update()
        clock.tick(FPS)


def start_menu():
    pg.mixer.music.load('start_menu_music.mp3')
    pg.mixer.music.set_volume(0.2)
    pg.mixer.music.play()
    menu = pygame_menu.Menu('Понг', 400, 200, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Играть', main)

    menu.add.button('Выйти из игры', pygame_menu.events.EXIT)
    menu.mainloop(window)
def end_menu(loser, winner):
    pg.mixer.music.load('lose.mp3')
    pg.mixer.music.set_volume(0.2)
    pg.mixer.music.play()
    menu = pygame_menu.Menu(loser + 'проиграл!' + winner + 'Победил!', 800, 400, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Сыграть еще раз', main)

    menu.add.button('Выйти в меню', start_menu)
    menu.mainloop(window)
if __name__ == '__main__':
    start_menu()
