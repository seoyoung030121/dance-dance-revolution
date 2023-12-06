import pygame
from PIL import Image, ImageDraw, ImageFont
import random
from colorsys import hsv_to_rgb
from Joystick import Joystick

# 방향 아이콘 클래스
class Direction(object):
    def __init__(self):
        self.pos = None
        self.direction = 0
        self.image = Image.open("Image/direction.png").convert("RGBA")
        self.image = self.image.resize((40, 40))  # Adjust the icon size
        self.rotated_image = self.image.rotate(0)
        self.y = -1
        self.x = int(SCREEN_WIDTH * 0.75) - (self.image.width / 2)
        self.createTime = pygame.time.get_ticks()

    def rotate(self, direction=0):
        self.direction = direction
        self.rotated_image = self.image.rotate(90 * self.direction)

    def draw(self):
        if self.y >= SCREEN_HEIGHT:
            self.y = -1
            return True
        elif self.y == -1:
            return False
        else:
            self.y += 0.5
            screen.paste(self.rotated_image, (int(self.x), int(self.y)), self.rotated_image)
            return False

# Character 클래스
class Character(object):
    def __init__(self):
        self.images = {
            "up": Image.open("Image/characterU.png"),
            "down": Image.open("Image/characterD.png"),
            "left": Image.open("Image/characterL.png"),
            "right": Image.open("Image/characterR.png"),
        }
        self.direction = "down"
        self.image = self.images[self.direction]
        self.image = self.image.resize((80, 80))
        self.rect = self.image.getbbox()
        self.rect = (self.rect[0] - resultImgRec.width // 2 - 20, self.rect[1], self.rect[2] - resultImgRec.width // 2 - 20, self.rect[3])
        self.rect = [int(i) for i in self.rect]

    def update_image(self):
        self.image = self.images[self.direction]
        self.image = self.image.resize((80, 80))

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
        screen.paste(self.image, (self.rect[0], self.rect[1]), self.image)

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
screen = Image.new("RGB", (SCREEN_WIDTH, SCREEN_HEIGHT), (0, 0, 0))
bgm = pygame.mixer.Sound("music.ogg")
bgm.set_volume(0.7)

Directions = [Direction() for i in range(0, 10)]  # 방향 아이콘
targetArea = ImageDraw.Draw(screen) # 타겟 박스
targetArea.rectangle([(SCREEN_WIDTH / 2, 160), (SCREEN_WIDTH, 160 + 70)], outline=(255, 255, 255))

resultFileNames = ["Image/miss.png", "Image/perfect.png", "Image/good.png", "Image/bad.png"]  # 결과 이모티콘
resultImg = [Image.open(name).resize((100, 50)) for name in resultFileNames]
resultImgRec = resultImg[0].get_rect()
resultImgRec.centerx = SCREEN_WIDTH / 2 - resultImgRec.width / 2 - 20
resultImgRec.centery = targetArea.centery

gradeFileNames = ["Image/gradeA.png", "Image/gradeB.png", "Image/gradeC.png", "Image/gradeD.png",
                  "Image/gradeF.png"]  # 등급
gradeImg = [Image.open(name).resize((SCREEN_WIDTH, SCREEN_HEIGHT)) for name in gradeFileNames]

character = Character()
joystick = Joystick()

# 입력과 direction이 일치하는지 확인
def resultProcess(direction):
    global isColl, score, DrawResult, result_ticks, combo

    if isColl and CollDirection.direction == direction:

        # targetArea의 중앙과 아이콘의 중심 사이의 거리 계산
        distanceDifference = abs(targetArea.centerx - (CollDirection.x + CollDirection.image.width / 2)) + abs(targetArea.centery - (CollDirection.y + CollDirection.image.height / 2))

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
    command = None

    if not joystick.button_U.value:
        command = 'up_pressed'
        character.move(0)
        resultProcess(0)
    elif not joystick.button_D.value:
        command = 'down_pressed'
        character.move(2)
        resultProcess(2)
    elif not joystick.button_L.value:
        command = 'left_pressed'
        character.move(1)
        resultProcess(1)
    elif not joystick.button_R.value:
        command = 'right_pressed'
        character.move(3)
        resultProcess(3)

# 방향 아이콘 생성과 그리기
def drawIcon():
    global start_ticks, chance

    if chance <= 0:
        return

    elapsed_time = (pygame.time.get_ticks() - start_ticks)
    if elapsed_time > 400:
        start_ticks = pygame.time.get_ticks()
        for direction in Directions:
            if direction.y == -1:
                direction.y = 0
                direction.rotate(direction=random.randint(0, 3))
                break

    for direction in Directions:
        if direction.draw():
            chance -= 1

# 타겟 영역 그리기와 충돌 확인하기
def draw_targetArea():
    global isColl, CollDirection
    isColl = False
    for direction in Directions:
        if direction.y == -1:
            continue
        if direction.pos.colliderect(targetArea):
            isColl = True
            CollDirection = direction
            break
    draw = ImageDraw.Draw(screen)
    draw.rectangle([(targetArea.x, targetArea.y), (targetArea.x + targetArea.width, targetArea.y + targetArea.height)], outline=(255, 255, 255))

# 점수, 콤보, 목숨
def setText():
    global score, chance
    font_path = "Gulim.ttf"  # Replace with the path to your font file
    mFont = ImageFont.truetype(font_path, 20)

    draw = ImageDraw.Draw(screen)

    mtext = f'score: {score}'
    draw.text((10, 10), mtext, font=mFont, fill=(255, 255, 255))

    mtext = f'combo: {combo}'
    draw.text((10, 32), mtext, font=mFont, fill=(255, 255, 255))

    mtext = f'chance: {chance}'
    draw.text((170, 10), mtext, font=mFont, fill=(255, 255, 255))

# 게임 결과 그리기
def drawGrade():
    global score, chance

    if chance <= 0:
        if score >= 10000:
            displayGradeImg = Image.open("Image/gradeA.png")
        elif score >= 8500:
            displayGradeImg = Image.open("Image/gradeB.png")
        elif score >= 6000:
            displayGradeImg = Image.open("Image/gradeC.png")
        elif score >= 3000:
            displayGradeImg = Image.open("Image/gradeD.png")
        elif score < 3000:
            displayGradeImg = Image.open("Image/gradeF.png")

        displayGradeImg = displayGradeImg.resize((SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.paste(displayGradeImg, (0, 0))

# 판정 결과 그리기
def drawResult():
    global DrawResult, result_ticks
    if result_ticks > 0:
        elapsed_time = (pygame.time.get_ticks() - result_ticks)
        if elapsed_time > 400:
            result_ticks = 0
            DrawResult = 0

    if DrawResult == 1:
        displayResultImg = Image.open("Image/perfect.png")
    elif DrawResult == 2:
        displayResultImg = Image.open("Image/good.png")
    elif DrawResult == 3:
        displayResultImg = Image.open("Image/bad.png")
    else:
        displayResultImg = Image.open("Image/miss.png")

    displayResultImg = displayResultImg.resize((100, 50))
    screen.paste(displayResultImg, resultImgRec)


# 시작화면
start_image = Image.open("Image/start.png").resize((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.paste(start_image, (0, 0))

# 아무 키나 누르기 전까지 대기
wait_for_key = True
while wait_for_key:
    for event in pygame.event.get():
        if not joystick.button_A.value:
            wait_for_key = False

# 반복문
while isActive:
    draw_targetArea()
    drawIcon()
    setText()
    drawGrade()
    character.draw()
    drawResult()
    screen.show()
    pygame.display.update()
    clock.tick(400)