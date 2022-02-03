import pygame, math
from sys import exit
pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

posx = 100
posy = 450

shoot_state = False
base = 0
per = 0
hyp = 0
power = 0
angle = 0
ang = 0
time = 0
x_new = 0
y_new = 0


def find_angle(mouse_pos):
    global per, base, angle, hyp, ang, angle, power
    base = (posx - mouse_pos[0])
    per = (posy - mouse_pos[1])
    hyp = math.sqrt(base**2 + per**2)
    power = hyp/30
    try:
        ratio = per / base
        angle = math.atan(ratio)
    except ZeroDivisionError:
        if per > 0:
            angle = math.pi/2
    if base < 0 and per >= 0:
        angle = abs(angle)
    elif base > 0 and per >= 0:
        angle = math.pi - angle
    elif base > 0 and per < 0:
        angle = math.pi + abs(angle)
    elif base < 0 and per < 0:
        angle = math.pi*2 - angle
    ang = math.degrees(angle)


def path():
    global x_new, y_new
    x_vel = power*math.cos(angle)
    y_vel = power*math.sin(angle)
    x_new = x_vel*time
    y_new = (y_vel*time) - (9.8*time**2/2)
    # print(f'x : {x_new}    y:{y_new}', end='')


font = pygame.font.Font(None, 30)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            shoot_state = True
            mouse_pos = pygame.mouse.get_pos()
            find_angle(mouse_pos)
            time = 0
        if event.type == pygame.KEYDOWN:
            posx = 100
            posy = 450
            shoot_state = False
    screen.fill('black')
###################################################################
    if shoot_state:
        if posy <= 450:
            time += 0.025
            path()
            posx += x_new
            posy -= y_new
        elif posy > 450:
            posy = 450
            time = 0
            shoot_state = False


##################################################################
    # print(f'base : {base}   per:{per}    hyp:{hyp}')
    # showing angle on screen
    mouse_pos = pygame.mouse.get_pos()
    txt = font.render(f'angle:{round(ang)}  power:{round(power)}', True, (255, 255, 255))
    txt_rect = txt.get_rect(center=(230,50))
    screen.blit(txt, txt_rect)
##########################################################################
    pygame.draw.line(screen, 'white', (posx, posy), mouse_pos)
    pygame.draw.line(screen, 'white', (0, 450), (800,450))
    # pygame.draw.line(screen, 'white', mouse_pos, (mouse_pos[0], posy))
    pygame.draw.circle(screen, 'red', (posx, posy), 10)

    clock.tick(60)
    pygame.display.flip()
