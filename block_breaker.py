
import pygame
import random
import math
import os

pygame.init()
pygame.mixer.init()

# 1. Dimensions and Colors
WIDTH, HEIGHT = 600, 500

BLACK = (10, 15, 35)
WHITE = (255, 255, 255)
GREEN = (0, 220, 130)
RED = (255, 80, 80)
BLUE = (60, 140, 255)
YELLOW = (255, 210, 70)
PURPLE = (180, 100, 255)

font = pygame.font.Font('freesansbold.ttf', 18)
titleFont = pygame.font.Font('freesansbold.ttf', 35)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Breaker - Star Edition")

clock = pygame.time.Clock()
FPS = 30


# 2. Sound Effects
hitSound = None

if os.path.exists("suara_bola_kena_balok.wav"):
    hitSound = pygame.mixer.Sound(
        "suara_bola_kena_balok.wav"
    )
    hitSound.set_volume(0.5)

# Background music (optional)
if os.path.exists("background.mp3"):
    pygame.mixer.music.load("background.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)


# 3. Helper Functions

def collisionChecker(rect, ball):
    return rect.colliderect(ball)


def populateBlocks(blockWidth, blockHeight,
                   horizontalGap, verticalGap):

    listOfBlocks = []
    colors = [WHITE, GREEN, BLUE, YELLOW, PURPLE]

    for i in range(10, WIDTH - blockWidth,
                   blockWidth + horizontalGap):

        for j in range(40, HEIGHT // 2,
                       blockHeight + verticalGap):

            color = random.choice(colors)

            listOfBlocks.append(
                Block(i, j, blockWidth, blockHeight, color)
            )

    return listOfBlocks


# 4. Striker Class

class Striker:

    def __init__(self, posx, posy, width,
                 height, speed, color):

        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.speed = speed
        self.color = color

        self.strikerRect = pygame.Rect(
            posx, posy, width, height
        )

    def display(self):

        pygame.draw.rect(
            screen, self.color,
            self.strikerRect,
            border_radius=8
        )

    def update(self, xFac):

        self.posx += self.speed * xFac

        self.posx = max(
            0, min(WIDTH - self.width, self.posx)
        )

        self.strikerRect = pygame.Rect(
            self.posx, self.posy,
            self.width, self.height
        )

    def getRect(self):
        return self.strikerRect


# 5. Block Class

class Block:

    def __init__(self, posx, posy, width, height, color):

        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.color = color

        self.damage = 100

        if color == WHITE:
            self.health = 200
        else:
            self.health = 100

        self.blockRect = pygame.Rect(
            posx, posy, width, height
        )

    def display(self):

        if self.health > 0:

            pygame.draw.rect(
                screen, self.color,
                self.blockRect,
                border_radius=4
            )

    def hit(self):
        self.health -= self.damage

    def getRect(self):
        return self.blockRect

    def getHealth(self):
        return self.health


# 6. Ball Class - Star Shape

class Ball:

    def __init__(self, posx, posy, radius, speed, color):

        self.posx, self.posy = posx, posy
        self.radius = radius
        self.speed = speed
        self.color = color

        self.xFac, self.yFac = 1, -1

    # Draw star-shaped ball
    def display(self):

        points = []

        for i in range(10):

            angle = -math.pi / 2 + i * math.pi / 5

            if i % 2 == 0:
                radius = self.radius
            else:
                radius = self.radius * 0.45

            x = self.posx + radius * math.cos(angle)
            y = self.posy + radius * math.sin(angle)

            points.append((int(x), int(y)))

        pygame.draw.polygon(
            screen, self.color, points
        )

    # Ball movement
    def update(self):

        self.posx += self.xFac * self.speed
        self.posy += self.yFac * self.speed

        if self.posx - self.radius <= 0:
            self.posx = self.radius
            self.xFac *= -1

        elif self.posx + self.radius >= WIDTH:
            self.posx = WIDTH - self.radius
            self.xFac *= -1

        if self.posy - self.radius <= 0:
            self.posy = self.radius
            self.yFac *= -1

        if self.posy - self.radius >= HEIGHT:
            return True

        return False

    def reset(self):

        self.posx = WIDTH // 2
        self.posy = HEIGHT - 100

        self.xFac, self.yFac = 1, -1

    def getRect(self):

        return pygame.Rect(
            int(self.posx - self.radius),
            int(self.posy - self.radius),
            self.radius * 2,
            self.radius * 2
        )


# 7. Game Manager

def main():

    running = True
    gameState = "playing"

    score = 0
    lives = 3

    # Reset game
    def resetGame():

        newStriker = Striker(
            WIDTH // 2 - 50,
            HEIGHT - 50,
            100, 15, 10, WHITE
        )

        newBall = Ball(
            WIDTH // 2,
            HEIGHT - 100,
            12, 5, YELLOW
        )

        newBlocks = populateBlocks(
            45, 15, 10, 20
        )

        return newStriker, newBall, newBlocks

    striker, ball, listOfBlocks = resetGame()

    strikerXFac = 0

    # Main game loop
    while running:

        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if gameState != "playing":

                    if event.key == pygame.K_SPACE:

                        score = 0
                        lives = 3

                        striker, ball, listOfBlocks = resetGame()

                        strikerXFac = 0
                        gameState = "playing"

                else:

                    if event.key == pygame.K_LEFT:
                        strikerXFac = -1

                    if event.key == pygame.K_RIGHT:
                        strikerXFac = 1

            if event.type == pygame.KEYUP:

                if event.key in (
                    pygame.K_LEFT,
                    pygame.K_RIGHT
                ):
                    strikerXFac = 0

        # Playing state
        if gameState == "playing":

            # Display score and lives
            scoreText = font.render(
                "Score: " + str(score), True, WHITE
            )

            livesText = font.render(
                "Lives: " + str(lives), True, WHITE
            )

            screen.blit(scoreText, (15, HEIGHT - 28))
            screen.blit(livesText, (500, HEIGHT - 28))

            # Update striker
            striker.update(strikerXFac)

            # Collision with striker
            if collisionChecker(
                striker.getRect(), ball.getRect()
            ):

                if ball.yFac > 0:

                    ball.yFac = -1

                    hitPosition = (
                        ball.posx -
                        (striker.posx + striker.width / 2)
                    )

                    ball.xFac = (
                        hitPosition / (striker.width / 2)
                    )

                    ball.xFac = max(
                        -1, min(1, ball.xFac)
                    )

                    ball.posy = striker.posy - ball.radius

            # Collision with blocks
            for block in listOfBlocks[:]:

                if collisionChecker(
                    block.getRect(), ball.getRect()
                ):

                    # Play sound when ball hits block
                    if hitSound is not None:
                        hitSound.play()

                    ball.yFac *= -1
                    block.hit()

                    if block.getHealth() <= 0:

                        listOfBlocks.remove(block)
                        score += 10

                    break

            # Update ball
            lifeLost = ball.update()

            if lifeLost:

                lives -= 1
                ball.reset()

                if lives <= 0:
                    gameState = "gameover"

            # Win condition
            if not listOfBlocks:
                gameState = "win"

            # Display objects
            striker.display()
            ball.display()

            for block in listOfBlocks:
                block.display()

            # Bottom border
            pygame.draw.line(
                screen, BLUE,
                (0, HEIGHT - 40),
                (WIDTH, HEIGHT - 40), 2
            )

        # Game over and win screen
        else:

            if gameState == "gameover":

                message = "GAME OVER"
                color = RED

            else:

                message = "YOU WIN!"
                color = GREEN

            title = titleFont.render(
                message, True, color
            )

            titleRect = title.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 - 40)
            )

            screen.blit(title, titleRect)

            finalScore = font.render(
                "Final Score: " + str(score),
                True, WHITE
            )

            scoreRect = finalScore.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 10)
            )

            screen.blit(finalScore, scoreRect)

            restartText = font.render(
                "Press SPACE to Play Again",
                True, YELLOW
            )

            restartRect = restartText.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 55)
            )

            screen.blit(restartText, restartRect)

        pygame.display.update()
        clock.tick(FPS)

    # Stop music and close game
    pygame.mixer.music.stop()
    pygame.quit()


if __name__ == "__main__":
    main()
