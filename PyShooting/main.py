import pygame
import sys
import random #운석 랜덤으로 떨어지기

from time import sleep

##게임 화면 구성

#게임화면
#BLACK = (0, 0, 0) #RGB -> 이제 게임 배경으로 대신함 ㅇㅇ
padWidth = 480
padHeight = 640

rockImage = [
'rock01.png', 'rock02.png', 'rock03.png', 'rock04.png', 'rock05.png', \
'rock06.png', 'rock07.png', 'rock08.png', 'rock09.png', 'rock10.png', \
'rock11.png', 'rock12.png', 'rock13.png', 'rock14.png', 'rock15.png', \
'rock16.png', 'rock17.png', 'rock18.png', 'rock19.png', 'rock20.png', \
'rock21.png', 'rock22.png', 'rock23.png', 'rock24.png', 'rock25.png', \
'rock26.png', 'rock27.png', 'rock28.png', 'rock29.png', 'rock30.png', ]

explosionSound = ['explosion01.wav', 'explosion02.wav', 'explosion03.wav', 'explosion04.wav']


#운석 맞춘 갯수 계산
def writeScore(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('파괴한 운석 수: ' + str(count), True, (255, 255, 255)) #RGB 흰색
    gamePad.blit(text, (10, 0)) #위치 왼쪽 위 ㅇㅇ

#운석이 화면 아래로 통과한 갯수
def writePassed(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('놓친 운석: ' + str(count), True, (225, 0, 0)) #RGB red
    gamePad.blit(text, (360, 0)) #위치 오른쪽 위 ㅇㅇ


#게임 메시지 출력
def writeMessage(text):
    global gamePad, gameoverSound
    textfont = pygame.font.Font('NanumGothic.ttf', 80)
    text = textfont.render(text, True, (225, 0, 0))
    tectpos = text.get_rect()
    tectpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text, tectpos)
    pygame.display.update()
    pygame.mixer.music.stop() #배경음악 정지
    gameoverSound.play() #게임 오버 사운드 재생
    sleep(2)
    pygame.mixer.music.play(-1) #배경음악 재생
    runGame()

#전투기가 운석과 충돌했을 때 메시지 출력
def crash():
    global gamePad
    writeMessage('전투기 파괴!')

#게임 오버 메시지 출력
def gameOver():
    global gamePad
    writeMessage('게임 오버!')



##배경 그림 넣기

#게임에 등장하는 객체를 드로잉
def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))


#게임 초기화 -> 배경 화면, 전투기, 미사일 발사, 폭발, 음악 등등도 넣자

def initGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound, gameoverSound
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('PyShooting') #게임 이름 (제목으로 띄움)
    background = pygame.image.load('background.png') #배경 그림
    fighter = pygame.image.load('fighter.png') #전투기 그림
    missile = pygame.image.load('missile.png') #미사일 그림
    explosion = pygame.image.load('explosion.png') #폭발 그림
    pygame.mixer.music.load('music.wav') #배경 음악
    pygame.mixer.music.play(-1) #배경 음악 재생
    missileSound = pygame.mixer.Sound('missile.wav') #미사일 사운드
    gameoverSound = pygame.mixer.Sound('gameover.wav') #게임 오버 사운드
    clock = pygame.time.Clock()

#게임 실행
def runGame():
    global gamepad, clock, background, fighter, missile, explosion, missileSound

    #전투기 크기
    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    #전투기 초기 위치 (x, y)
    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0


    #미사일 좌표 리스트 -> 미사일 여러 개 위치를 가져옴
    missileXY = []

    #운석 랜덤 생성
    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    destroySound = pygame.mixer.Sound(random.choice(explosionSound))

    #운석 초기 위치 설정
    rockX = random.randrange(0, padWidth - rockWidth)
    rockY = 0
    rockSpeed = 2

    #미사일에 운석이 맞았을 경우 True
    isShot = False
    shotCount = 0
    rockPassed = 0


    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]: #게임 프로그램 종료
                pygame.quit()
                sys.exit()

            #전투기 움직이기
            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT: #왼쪽 이동
                    fighterX -= 5

                elif event.key == pygame.K_RIGHT: #오른쪽 이동
                    fighterX += 5

                elif event.key == pygame.K_SPACE: #미사일 발사
                    missileSound.play() #미사일 사운드 재생
                    missileX = x + fighterWidth/2
                    missileY = y - fighterHeight
                    missileXY.append([missileX, missileY]) #리스트에 좌표값 저장

            #방향키 떼면 전투기 멈춤
            if event.type in [pygame.KEYUP]: 
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0

        #gamePad.fill(BLACK) #게임 화면 -> 배경화면으로 대신하자
        drawObject(background, 0, 0) #배경 화면 그리기


        #키보드 조작 후에 변경된 전투기 위치 재조정
        x += fighterX
        if x < 0: #끝까지 왼쪽으로 갔을 때 (최대 위치 설정)
            x = 0

        elif x > padWidth - fighterWidth: 
            x = padWidth - fighterWidth


        #전투기가 운석과 충동했는지 check
        if y < rockY + rockHeight:
            if(rockX > x and rockX < x + fighterWidth) or \
                (rockX + rockWidth > x and rockX + rockWidth < x + fighterWidth):
                crash()


        drawObject(fighter, x, y) #전투기를 게임 화면의 (x, y)에 그림

        #미사일 발사 화면에 그리기
        if len(missileXY) != 0: #미사일 변수 length가 1개 이상일 때 (0이 아니면)
            for i, bxy in enumerate(missileXY): #미사일 요소에 대해 반복
                bxy[1] -= 10 #총알 y좌표 -10씩 이동 (위로 이동)
                missileXY[i][1] = bxy[1] #list 값으로 

                #미사일이 운석을 맞추었을 경우
                if bxy[1] < rockY:
                    if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount += 1

                #미사일이 화면 밖으로 벗어나면
                if bxy[1] <= 0:
                    try:
                        missileXY.remove(bxy) #미사일 제거
                    except:
                        pass

        if len(missileXY) != 0: 
            for bx, by in missileXY:
                drawObject(missile, bx, by) #미사일을 그려줌

        #운석 맞춘 점수 표시
        writeScore(shotCount)

        #운석 아래로 움직임
        rockY += rockSpeed

        #운석이 지구로 떨어진 경우
        if rockY > padHeight:
            #새로운 운석 (랜덤)
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            rockPassed += 1

        if rockPassed == 3: #운석 3개 놓치면 게임 오버
            gameOver()

        #놓친 운석 수 표시
        writePassed(rockPassed)

        #운석을 맞춘 경우
        if isShot:
            #운석 폭발
            drawObject(explosion, rockX, rockY) #폭발 그림
            destroySound.play() #운석 폭발 사운드 재생

            #새로운 운석 (랜덤)
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            destroySound = pygame.mixer.Sound(random.choice(explosionSound))
            isShot = False

            #운석 맞추면 속도 증가
            rockSpeed += 0.02
            if rockSpeed >= 10:
                rockSpeed = 10

        #운석 그리기
        drawObject(rock, rockX, rockY)

        pygame.display.update() #게임 화면을 다시 그림
        clock.tick(60) #게임 화면의 초당 프레임 수 설정
    
    pygame.quit() #pygame 종료

#함수 위에서 정의하고 실행시키자
initGame()
runGame()
