import pygame
from random import *
import os

pygame.init()

swidth = 640
sheight = 480
screen = pygame.display.set_mode((swidth, sheight))

pygame.display.set_caption("PangGame")

clock = pygame.time.Clock()

current_path = os.path.dirname(__file__) #현재 파일 위치 반환
image_path = os.path.join(current_path, "image")

#배경
background = pygame.image.load(os.path.join(image_path, "paper2.png"))

#스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
st_height = stage_size[1]

#캐릭터
character = pygame.image.load(os.path.join(image_path, "ship02(1).png"))
character_size = character.get_rect().size
cwidth = character_size[0]
cheight = character_size[1]
c_x_pos = (swidth / 2) - (cwidth / 2)
c_y_pos = sheight - cheight - st_height
cspeed = 5
to_x = 0
to_y = 0

#무기
weapon = pygame.image.load(os.path.join(image_path, "missile.png"))
weapon_size = weapon.get_rect().size
w_width = weapon_size[0]
#무기는 여러발 발사
weapons = []
#무기속도
w_speed = 10
#공
ball_images = [ 
    pygame.image.load(os.path.join(image_path, "monster.png")),
    pygame.image.load(os.path.join(image_path, "monster(1).png")),
    pygame.image.load(os.path.join(image_path, "monster(2).png")),
    pygame.image.load(os.path.join(image_path, "monster(3).png"))
]
b_speed_y = [-18, -15, -12, -9] #index 0, 1, 2, 3에 해당하는 값

#공들
balls = []
balls.append({
    "pos_x" : 50, #공의 x좌표
    "pos_y" : 50, #공의 y 좌표
    "img_idx" : 0, #공의 이미지 인덱스
    "b_to_x" : 3, # x축 이동방향, -3이면 왼쪽으로, 3이면 오른쪽으로
    "b_to_y" : -6, #y축 이동방향
    "init_spd_y" : b_speed_y[0] #최초 속도
})

#사라질 무기, 공 정보 저장 변수
w_to_remove = -1
b_to_remove = -1

# Font 정의
game_font = pygame.font.Font(None, 40)
total_time = 100
start_ticks = pygame.time.get_ticks()

#게임 종료 
game_result = "Game Over"

running = True
while running:
    dt = clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x -= cspeed
            elif event.key == pygame.K_RIGHT:
                to_x += cspeed
            elif event.key == pygame.K_SPACE:
                w_x_pos = c_x_pos + (cwidth / 2) - (w_width / 2)
                w_y_pos = c_y_pos
                weapons.append([w_x_pos, w_y_pos])


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
    
    c_x_pos += to_x
    c_y_pos += to_y

    if c_x_pos < 0:
        c_x_pos = 0
    elif c_x_pos > swidth - cwidth:
        c_x_pos = swidth - cwidth
    if c_y_pos < 0:
        c_y_pos = 0
    elif c_y_pos > sheight - cheight:
        c_y_pos = sheight - cheight
    
    #무기위치
    weapons = [[w[0], w[1] - w_speed] for w in weapons]


    #천장에 닿은 무기 없애기
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]

    #공 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        b_x_pos = ball_val["pos_x"]
        b_y_pos = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        bwidth = ball_size[0]
        bheight = ball_size[1]
        
        #가로벽에 닿았을때 공 이동 위치 변경
        if b_x_pos < 0 or b_x_pos > swidth - bwidth:
            ball_val["b_to_x"] = ball_val["b_to_x"] * -1
        #세로위치
        #튕겨서 올라가는 처리
        if b_y_pos >= sheight - st_height - bheight:
            ball_val["b_to_y"] = ball_val["init_spd_y"]
        else: #그 외의 모든 경우에는 속도 증가
            ball_val["b_to_y"] += 0.5
        
        ball_val["pos_x"] += ball_val["b_to_x"]
        ball_val["pos_y"] += ball_val["b_to_y"]

    # 충돌 처리

    #캐릭터 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = c_x_pos
    character_rect.top = c_y_pos

    for ball_idx, ball_val in enumerate(balls):
        b_x_pos = ball_val["pos_x"]
        b_y_pos = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
        
        #공 rect정보 업데이트
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = b_x_pos
        ball_rect.top = b_y_pos

        #공과 캐릭터 충돌 처리
        if character_rect.colliderect(ball_rect):
            running = False
            break

        #공과 무기들 충돌 처리
        for weapon_idx, weapon_val in enumerate(weapons):
            w_x_pos = weapon_val[0]
            w_y_pos = weapon_val[1]

            #무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = w_x_pos
            weapon_rect.top = w_y_pos

            #충돌체크
            if weapon_rect.colliderect(ball_rect):
                w_to_remove = weapon_idx
                b_to_remove = ball_idx
            
            #공쪼개기
            #가장 작은 크기가 아닐때 다음 단계 공으로 나누기
                if ball_img_idx < 3:
                    #현재 공 크기 정보
                    bwidth = ball_rect.size[0]
                    bheight = ball_rect.size[1]

                    #나눠진 공 정보
                    small_ball_rect = ball_images[ball_img_idx +1].get_rect()
                    smb_width = small_ball_rect.size[0]
                    smb_height = small_ball_rect.size[1]

                    #왼쪽으로 튕기기
                    balls.append({
                        "pos_x" : b_x_pos + (bwidth / 2) - (smb_width / 2), #공의 x좌표
                        "pos_y" : b_y_pos + (bheight / 2) - (smb_height / 2), #공의 y 좌표
                        "img_idx" : ball_img_idx + 1, #공의 이미지 인덱스
                        "b_to_x" : -3, # x축 이동방향, -3이면 왼쪽으로, 3이면 오른쪽으로
                        "b_to_y" : -6, #y축 이동방향
                        "init_spd_y" : b_speed_y[ball_img_idx + 1] #최초 속도
                    })
                    #오른쪽으로 튕기기
                    balls.append({
                        "pos_x" : b_x_pos + (bwidth / 2) - (smb_width / 2), #공의 x좌표
                        "pos_y" : b_y_pos + (bheight / 2) - (smb_height / 2), #공의 y 좌표
                        "img_idx" : ball_img_idx + 1, #공의 이미지 인덱스
                        "b_to_x" : 3, # x축 이동방향, -3이면 왼쪽으로, 3이면 오른쪽으로
                        "b_to_y" : -6, #y축 이동방향
                        "init_spd_y" : b_speed_y[ball_img_idx + 1] #최초 속도
                    })
                break
        else:
            continue
        break

    #충돌된 공 or 무기 없애기
    if b_to_remove > -1:
        del balls[b_to_remove]
        b_to_remove = -1
    
    if w_to_remove > -1:
        del weapons[w_to_remove]
        w_to_remove = -1
    
    #모든 공을 없앤 경우 게임 종료
    if len(balls) == 0:
        game_result = "Mission Complete"
        running = False

    


    #화면 그리기
    screen.blit(background, (0, 0))

    for w_x_pos, w_y_pos in weapons:
        screen.blit(weapon, (w_x_pos, w_y_pos))

    for idx, val in enumerate(balls):
        b_x_pos = val["pos_x"]
        b_y_pos = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (b_x_pos,  b_y_pos))

    screen.blit(stage, (0, sheight - st_height))
    screen.blit(character, (c_x_pos, c_y_pos))

    #경과 시간
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)),True, (255,255,255))
    screen.blit(timer,(10, 10))

    #시간초과
    if total_time - elapsed_time < 0:
        game_result = "Time Over"
        running = False

    pygame.display.update()
#게임 오버 메시지
msg = game_font.render(game_result, True, (255,255,0))
msg_rect = msg.get_rect(center=(int(swidth / 2), int(sheight / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

pygame.time.delay(2000)
pygame.quit()
