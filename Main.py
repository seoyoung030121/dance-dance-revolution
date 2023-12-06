import pygame
import random
from pygame.rect import *

pygame.init()
pygame.display.set_caption("esw")

# 방향 아이콘 클래스
class Direction(object):
    def __init__(self):
        self.pos = None
        self.direction = 0
        self.image = pygame.image.load(f"Image/direction.png")
        self.image = pygame.transform.scale(self.image, (40, 40))  # Adjust the icon size
        self.rotated_image = pygame.transform.rotate(self.image, 0)
        self.y = -1
        self.x = int(SCREEN_WIDTH * 0.75) - (self.image.get_width() / 2)
        self.createTime = pygame.time.get_ticks()

    def rotate(self, direction=0):
        self.direction = direction
        self.rotated_image = pygame.transform.rotate(
            self.image, 90 * self.direction)

    def draw(self):
        if self.y >= SCREEN_HEIGHT:
            self.y = -1
            return True
        elif self.y == -1:
            return False
        else:
            self.y += 0.5
            self.pos = screen.blit(self.rotated_image, (self.x, self.y))
            return False

# Character 클래스
class Character(object):
    def __init__(self):
        self.images = {
            "up": pygame.image.load("Image/characterU.png"),
            "down": pygame.image.load("Image/characterD.png"),
            "left": pygame.image.load("Image/characterL.png"),
            "right": pygame.image.load("Image/characterR.png"),
        }
        self.direction = "down"
        self.image = self.images[self.direction]
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2 - resultImgRec.width // 2 - 20
        self.rect.centery = SCREEN_HEIGHT // 2

    def update_image(self):
        self.image = self.images[self.direction]
        self.image = pygame.transform.scale(self.image, (80, 80))

    def move(self, direction):
        if direction == 0:
            self.direction = "up"
        elif direction == 1:
            self.direction = "left"
        elif direction == 2:
            self.direction = "down"
        elif direction == 3:
            self.direction = "right"
        else:
            self.direction = "down"

        self.update_image()

    def draw(self):
        screen.blit(self.image, self.rect)

# 변수
isActive = True
SCREEN_WIDTH = 240
SCREEN_HEIGHT = 240
chance_MAX = 3
score = 0
combo = 0
chance = chance_MAX
isColl = False
CollDirection = 0
DrawResult, result_ticks = 0, 0
start_ticks = pygame.time.get_ticks()

perfectTolerance = 10  # 사용자 입력이 'Perfect' 판정을 받기 위한 거리 허용 범위
goodTolerance = 30  # 사용자 입력이 'Good' 판정을 받기 위한 거리 허용 범위

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.image.load("Image/background.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
bgm = pygame.mixer.Sound("music.ogg")
bgm.set_volume(0.7)

Directions = [Direction() for i in range(0, 10)] # 방향 아이콘
targetArea = Rect(SCREEN_WIDTH / 2, 160, SCREEN_WIDTH / 2, 70) # 타겟 박스

resultFileNames = ["Image/miss.png", "Image/perfect.png", "Image/good.png", "Image/bad.png"] # 결과 이모티콘
resultImg = []
for i, name in enumerate(resultFileNames):
    resultImg.append(pygame.image.load(name))
    resultImg[i] = pygame.transform.scale(resultImg[i], (100, 50))
resultImgRec = resultImg[0].get_rect()
resultImgRec.centerx = SCREEN_WIDTH / 2 - resultImgRec.width / 2 - 20
resultImgRec.centery = targetArea.centery

gradeFileNames = ["Image/gradeA.png", "Image/gradeB.png", "Image/gradeC.png", "Image/gradeD.png", "Image/gradeF.png"] # 결과
gradeImg = []
for i, name in enumerate(gradeFileNames):
    gradeImg.append(pygame.image.load(name))
    gradeImg[i] = pygame.transform.scale(gradeImg[i], (SCREEN_WIDTH, SCREEN_HEIGHT))

character = Character()

# 입력과 direction이 일치하는지 확인
def resultProcess(direction):
    global isColl, score, DrawResult, result_ticks, combo

    if isColl and CollDirection.direction == direction:

        # targetArea의 중앙과 아이콘의 중심 사이의 거리 계산
        distanceDifference = abs(targetArea.centerx - (CollDirection.x + CollDirection.image.get_width() / 2)) + abs(targetArea.centery - (CollDirection.y + CollDirection.image.get_height() / 2))

        if distanceDifference < perfectTolerance:
            score += 100
            combo += 1  # 정확한 입력 콤보 카운터 증가
            DrawResult = 1
        elif distanceDifference < goodTolerance:
            score += 70
            combo += 1  # 정확한 입력 콤보 카운터 증가
            DrawResult = 2
        else:
            score += 30
            combo = 0  # 잘못된 입력에 따른 콤보 카운터 초기화

        # 콤보 보너스 점수 추가
        if combo == 10:
            score += 10
        elif combo == 50:
            score += 20
        elif combo == 100:
            score += 50

        CollDirection.y = -1
    else:
        DrawResult = 3
        combo = 0  # 잘못된 입력에 따른 콤보 카운터 초기화
    result_ticks = pygame.time.get_ticks()

# 키 입력
def eventProcess():
    global isActive, score, chance

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isActive = False
            if chance > 0:
                if event.key == pygame.K_UP:  # 0
                    character.move(0)
                    resultProcess(0)
                if event.key == pygame.K_LEFT:  # 1
                    character.move(1)
                    resultProcess(1)
                if event.key == pygame.K_DOWN:  # 2
                    character.move(2)
                    resultProcess(2)
                if event.key == pygame.K_RIGHT:  # 3
                    character.move(3)
                    resultProcess(3)
            else:
                if event.key == pygame.K_SPACE:
                    score = 0
                    chance = chance_MAX
                    for direc in Directions:
                        direc.y = -1
                    character.move(2)

# 방향 아이콘 생성과 그리기
def drawIcon():
    global start_ticks, chance

    if chance <= 0:
        return

    elapsed_time = (pygame.time.get_ticks() - start_ticks)
    if elapsed_time > 400:
        start_ticks = pygame.time.get_ticks()
        for direc in Directions:
            if direc.y == -1:
                direc.y = 0
                direc.rotate(direction=random.randint(0, 3))
                break

    for direc in Directions:
        if direc.draw():
            chance -= 1

# 타겟 영역 그리기와 충돌 확인하기
def draw_targetArea():
    global isColl, CollDirection
    isColl = False
    for direc in Directions:
        if direc.y == -1:
            continue
        if direc.pos.colliderect(targetArea):
            isColl = True
            CollDirection = direc
            break
    pygame.draw.rect(screen, (255, 255, 255), targetArea, 2)

# 점수, 콤보, 목숨
def setText():
    global score, chance
    mFont = pygame.font.SysFont("굴림", 20)

    mtext = mFont.render(f'score: {score}', True, 'white')
    screen.blit(mtext, (10, 10, 0, 0))

    mtext = mFont.render(f'combo: {combo}', True, 'white')
    screen.blit(mtext, (10, 32, 0, 0))

    mtext = mFont.render(f'chance: {chance}', True, 'white')
    screen.blit(mtext, (170, 10, 0, 0))

# 게임 결과 그리기
def drawGrade():
    global score, chance

    if chance <= 0:

        if score >= 10000:
            displayGradeImg = gradeImg[0]
        elif score >= 8500:
            displayGradeImg = gradeImg[1]
        elif score >= 6000:
            displayGradeImg = gradeImg[2]
        elif score >= 3000:
            displayGradeImg = gradeImg[3]
        elif score < 3000:
            displayGradeImg = gradeImg[4]

        screen.blit(displayGradeImg, (0, 0))

# 판정 결과 그리기
def drawResult():
    global DrawResult, result_ticks
    if result_ticks > 0:
        elapsed_time = (pygame.time.get_ticks() - result_ticks)
        if elapsed_time > 400:
            result_ticks = 0
            DrawResult = 0

    if DrawResult == 1:
        displayResultImg = resultImg[1]
    elif DrawResult == 2:
        displayResultImg = resultImg[2]
    elif DrawResult == 3:
        displayResultImg = resultImg[3]
    else:
        displayResultImg = resultImg[0]

    screen.blit(displayResultImg, resultImgRec)


# 시작화면
start_image = pygame.image.load("Image/start.png")
start_image = pygame.transform.scale(start_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
screen.blit(start_image, (0, 0))
pygame.display.update()

# 아무 키나 누르기 전까지 대기
wait_for_key = True
while wait_for_key:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            wait_for_key = False

# 반복문
while (isActive):
    screen.blit(background, (0, 0))
    bgm.play()

    eventProcess()
    draw_targetArea()
    drawIcon()
    setText()
    drawGrade()
    character.draw()
    drawResult()
    pygame.display.update()
    clock.tick(400)