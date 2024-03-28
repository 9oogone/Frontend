import pygame
import sys
import random

pygame.init() # pygame 모듈 초기화

img_neko = [ 
    None,
    pygame.image.load("neko1.png"),
    pygame.image.load("neko2.png"),
    pygame.image.load("neko3.png"),
    pygame.image.load("neko4.png"),
    pygame.image.load("neko5.png"),
    pygame.image.load("neko6.png"),
    pygame.image.load("neko_niku.png"),
]




map_y = 10
map_x = 8
display_width = 912
display_height = 768
bg = pygame.image.load("neko_bg.png")
cursor = pygame.image.load("neko_cursor.png")

neko = [[] for _ in range(map_y)]
check = [[0 for _ in range(map_x)] for _ in range(map_y)]
search = [[0 for _ in range(map_x)] for _ in range(map_y)]
for y in range(map_y):
    for x in range(map_x):
        neko[y].append(random.choice(range(1,7)))

gameDisplay = pygame.display.set_mode((display_width, display_height)) #스크린 초기화
pygame.display.set_caption("애니팡")  # 타이틀
clock = pygame.time.Clock() #Clock 오브젝트 초기화

class Mouse :
    def __init__(self,cursor,map_y,map_x):
        self.turn = 0
        self.cursor = cursor
        self.map_y = map_y
        self.map_x = map_x

    def get_mouse(self):
        position = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for y in range(map_y):
            for x in range(map_x):
                if x*72+20 < position[0] < (x+1)*72+20 and y*72+20 < position[1] < (y+1)*72+20 :
                    if self.turn == 0 :
                        gameDisplay.blit(self.cursor,(x*72+20,y*72+20))
                        if click[0] :
                            self.turn = 1
                            check[y][x] = 1
                    else :
                        if (0 <= y-1 and check[y-1][x] == 1) or (y+1 < self.map_y and check[y+1][x] == 1) \
                            or (self.map_x > x+1 and check[y][x+1] == 1) or (0 <= x-1 and check[y][x-1] == 1):
                            gameDisplay.blit(self.cursor,(x*72+20,y*72+20)) 
                            if click[0] :
                                self.turn = 0
                                switch_neko(y,x)
                                cursor_set()
                                # 초기화 시켜주기
                        if click[2] :
                            self.turn = 2
                            cursor_set() # 초기화 시켜주기
                            self.turn = 0


def switch_neko(y,x): 
    for i in range(map_y):
        for j in range(map_x):
            if check[i][j] == 1:
                neko[y][x], neko[i][j] = neko[i][j], neko[y][x]
                
      
def check_neko(idx):
    idx = 0
    for y in range(10):
        for x in range(8):
            search[y][x] = neko[y][x]

    for y in range(1, 9):
        for x in range(8):
            if search[y][x] > 0:
                if search[y-1][x] == search[y][x] and search[y+1][x] == search[y][x]:
                    neko[y-1][x] = 7
                    neko[y][x] = 7
                    neko[y+1][x] = 7
                    idx = 1

    for y in range(10):
        for x in range(1, 7):
            if search[y][x] > 0:
                if search[y][x-1] == search[y][x] and search[y][x+1] == search[y][x]:
                    neko[y][x-1] = 7
                    neko[y][x] = 7
                    neko[y][x+1] = 7
                    idx = 1
    return idx



def cursor_set():
    # 커서 초기화
    for y in range(map_y):
        for x in range(map_x):
            if check[y][x] == 1:
                check[y][x] = 0
    
def cursor_draw():
    for y in range(map_y):
        for x in range(map_x):
            if check[y][x] == 1:
                gameDisplay.blit(cursor,(x*72+20, y*72+20))

def neko_draw():
    for y in range(map_y):
        for x in range(map_x):
            if neko[y][x] > 0 :
                gameDisplay.blit(img_neko[neko[y][x]], (x*72+20, y*72+20))
            

def drop_neko():
    for x in range(map_x):
        for y in range(map_y-1, -1, -1):  # 맨 아래부터 시작해서 위로 올라감
            if neko[y][x] == 0:  # 빈 공간을 발견하면
                for ny in range(y-1, -1, -1):  # 현재 위치 위쪽으로 탐색
                    if neko[ny][x] != 0:  # 빈 공간이 아닌 것을 찾으면
                        neko[y][x] = neko[ny][x]  # 빈 공간에 위에 있는 네코를 내려놓음
                        neko[ny][x] = 0  # 위에 있던 자리는 빈 공간으로 만듦
                        break
                else:  # 위쪽에 네코가 없을 때 (가장 위쪽에 있는 경우)
                    neko[y][x] = random.randint(1, 6)  # 랜덤한 네코 생성

def sweep_neko():
    for y in range(map_y):
        for x in range(map_x):
            if neko[y][x] == 7:
                neko[y][x] = 0

def check_switch(y,x):
    for y in range(10):
        for x in range(8):
            search[y][x] = neko[y][x]

    for y in range(1, 9):
        for x in range(8):
            if search[y][x] > 0:
                if search[y-1][x] == search[y][x] and search[y+1][x] == search[y][x]:
                    return True

    for y in range(10):
        for x in range(1, 7):
            if search[y][x] > 0:
                if search[y][x-1] == search[y][x] and search[y][x+1] == search[y][x]:
                    return True
    return False



def game(): # 메인 게임 함수
    tmr = 0 # 시간 관리 변수
    # 마우스 클래스 부르기
    m = Mouse(cursor,map_y,map_x)
    idx = 0
    while True:
        tmr += 1 # 매 시간 1초 증가
        for event in pygame.event.get(): # 윈도운 X 누를 시 나오게끔
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        gameDisplay.blit(bg,(0,0))
        neko_draw() # 네코 떨어지기
        m.get_mouse() # 마우스 작동
        cursor_draw()
        if idx == 0 :
            idx = check_neko(idx)
        elif 4 > idx >= 1 :
            idx += 1
        elif idx == 4 :
            sweep_neko()
            idx = 0 
        drop_neko()
        pygame.display.update()
        clock.tick(20)

        

game()
