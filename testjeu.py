import pygame
pygame.init()
Font = pygame.font.Font('freesansbold.ttf', 20)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

Width, Height = 900, 60
Fenetre = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock() 
FPS = 30


class Striker:
    def __init__(self, PosX, PosY, Width, Height, Speed, Color):
        self.PosX = PosX
        self.PosY = PosY
        self.Width = Width
        self.Height = Height
        self.Speed = Speed
        self.Color = Color
        self.PlayerRect = pygame.Rect(PosX, PosY, Width, Height)
        self.Player = pygame.draw.rect(Fenetre, self.Color, self.PlayerRect)

    def display(self):
        self.Player = pygame.draw.rect(Fenetre, self.Color, self.PlayerRect)

    def update(self, y):
        self.PosY = self.PosY + self.Speed*y

        if self.PosY <= 0:
            self.PosY = 0
            
        elif self.PosY + self.Height >= Height:
            self.PosY = Height-self.Height

        self.PlayerRect = (self.PosX, self.PosY, self.Width, self.Height)

    def getRect(self):
        return self.PlayerRect

class Ball:
    def __init__(self, PosX, PosY, Rayon, Speed):
        self.PosX = PosX
        self.PosY = PosY
        self.Rayon = Rayon
        self.Speed = Speed
        self.x = 1
        self.y = -1
        self.Color = (self.PosX % 255, self.PosX % 255, self.PosX % 255)
        self.ball = pygame.draw.circle(Fenetre,self.Color, (self.PosX, self.PosY), self.Rayon)
        self.firstTime = 1
        
    def Color_Change(self):
        self.Color = (self.PosX % 255, self.PosX % 255, self.PosX % 255)

    def display(self):
        self.ball = pygame.draw.circle(Fenetre, self.Color,(self.PosX, self.PosY), self.Rayon)

    def update(self):
        self.PosX += self.Speed*self.x
        self.PosY += self.Speed*self.y

        if self.PosY <= 0 or self.PosY >= Height:
            self.y *= -1

        if self.PosX <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.PosX >= Width and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0

    def reset(self):
        self.PosX = Width//2
        self.PosY = Height//2
        self.x *= -1
        self.firstTime = 1

    def hit(self):
        self.x *= -1

    def getRect(self):
        return self.ball


def main():
    running = True

    Player1 = Striker(20, 0, 10, 100, 10, BLUE)
    Player2 = Striker(Width-30, 0, 10, 100, 10, RED)
    ball = Ball(Width//2, Height//2, 7, 7)

    listOfPlayer = [Player1, Player2]


    Player1YFac, Player2YFac = 0, 0

    while running:
        Fenetre.fill(BLACK)
        
        ball.Color_Change()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    Player2YFac = -1
                if event.key == pygame.K_DOWN:
                    Player2YFac = 1
                if event.key == pygame.K_z:
                    Player1YFac = -1
                if event.key == pygame.K_s:
                    Player1YFac = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    Player2YFac = 0
                if event.key == pygame.K_z or event.key == pygame.K_s:
                    Player1YFac = 0

        for Player in listOfPlayer:
            if pygame.Rect.colliderect(ball.getRect(), Player.getRect()):
                ball.hit()

        Player1.update(Player1YFac)
        Player2.update(Player2YFac)
        point = ball.update()


        if point: 
            ball.reset()

        Player1.display()
        Player2.display()
        ball.display()

        pygame.display.update()
        clock.tick(FPS)  


if __name__ == "__main__":
    main()
    pygame.quit()

