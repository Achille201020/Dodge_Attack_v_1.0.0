import os
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
os.chdir(cartella_corrente)
import random
import math
import pygame
pygame.init()
esplosione_1 = pygame.transform.scale(pygame.image.load("Assets\explosion_frame_1.png", "r"), (100,100))
esplosione_2 = pygame.transform.scale(pygame.image.load("Assets\explosion_frame_2.png", "r"), (100,100))
esplosione_3 = pygame.transform.scale(pygame.image.load("Assets\explosion_frame_3.png", "r"), (100,100))
esplosione_4 = pygame.transform.scale(pygame.image.load("Assets\explosion_frame_4.png", "r"), (100,100))
esplosione_5 = pygame.transform.scale(pygame.image.load("Assets\explosion_frame_5.png", "r"), (100,100))
esplosione_6 = pygame.transform.scale(pygame.image.load("Assets\explosion_frame_6.png", "r"), (100,100))
start = pygame.transform.scale(pygame.image.load("Assets\start-video.png"),(100,100))
fulmine_imm = pygame.transform.scale(pygame.image.load("Assets/fulmine.png"), (50,50))
suono_esplosione = pygame.mixer.Sound("Assets/esplosione.mp3")
suono_countdown =pygame.mixer.Sound("Assets/2-1.mp3")
musica_titolo = pygame.mixer.Sound("Assets/musica_arcade2.mp3")
musica_gioco = pygame.mixer.Sound("Assets/musica_arcade3.mp3")
font_1 = pygame.font.Font(("Assets/Pixeled.ttf"), 25)
font_2 = pygame.font.Font(("Assets/Pixeled.ttf"), 50)
pausa = False
mode = "easy"
scattando = False
durata_scatto = 5000 #ms
scatto = False
fine_scatto = 0  
fine_scatto = pygame.time.get_ticks()
ripristino_scatto = random.randint(5000, 15000) #ms

larghezza_finestra=1350
altezza_finestra=800
raggio_pl = 35
raggio_random = 50 # Giocatore e cerchi random
raggioAI = 20 # AI predator
raggio_scatto = 30
punteggio = 0
speed = 5
speedAI = 0
speed_max = 0
highscoring = False

angle1 = random.uniform(0, 2 * math.pi)
speed_x1 = math.cos(angle1) * 4
speed_y1 = math.sin(angle1) * 4

angle2 = random.uniform(0, 2 * math.pi)
speed_x2 = math.cos(angle2) * 4
speed_y2 = math.sin(angle2) * 4
screen = pygame.display.set_mode((larghezza_finestra,altezza_finestra))
screen.fill((0,0,0))
clock=pygame.time.Clock()
start_time = pygame.time.get_ticks()
titolo = pygame.display.set_caption("Dodge Attack")
running = True

x=larghezza_finestra//2 # Giocatore
y=altezza_finestra//2 # Giocatore
x1 = 330 #cerchio random
y1 = 150 #cerchio random
x2 = 100 #cerchio random
y2 = 180 #cerchio random
x3= 150 # AI predator
y3= 150 # AI predator
x_scatto = random.randint(raggio_scatto,larghezza_finestra)
y_scatto = random.randint(100+raggio_scatto, altezza_finestra)

target3 = (x,y)
text_outro = font_2.render("Game Over!", True, (0,0,0))
text_new_highscore = font_2.render("New highscore!", True, (0,0,0))
intro = False
circle_scatto = False

def schermata_principale():
    musica_gioco.stop()
    musica_titolo.stop()
    musica_titolo.set_volume(0.1)
    start = True
    screen.fill((255,255,255))
    text_nome_gioco = font_2.render("Dodge Attack", True, (0,0,0))
    text_nome_gioco_centr = text_nome_gioco.get_rect(center = (larghezza_finestra//2, altezza_finestra//2 - 100))
    screen.blit(text_nome_gioco, text_nome_gioco_centr)
    text_start_gioco = font_1.render("Press SPACE + difficulty to start", True, (0,0,0))
    text_start_gioco_centr = text_start_gioco.get_rect(center = (larghezza_finestra//2, altezza_finestra//2 + 50))
    screen.blit(text_start_gioco, text_start_gioco_centr)
    text_difficoltà = font_1.render("                                                               Select difficulty: z=easy, x=medium, c=hard", True, (0,0,0))
    text_difficoltà_centr = text_difficoltà.get_rect(center = (larghezza_finestra//2-300, altezza_finestra//2))
    screen.blit(text_difficoltà, text_difficoltà_centr)

    
    pygame.draw.circle(screen, (0,0,255), (1200,300), raggio_random)
    pygame.draw.circle(screen, (0,0,255), (200,700), raggio_random)
    pygame.draw.circle(screen, (0,255,0), (900,700), raggio_pl)
    pygame.draw.circle(screen, (100,50,150), (800,600), raggioAI)
    pygame.draw.circle(screen, (255,255,0), (400,100), raggio_scatto)
    fulmine_centrato = fulmine_imm.get_rect(center = (400, 100))
    pygame.draw.circle(screen, (255,255,0), (400, 100), raggio_scatto)
    screen.blit(fulmine_imm, fulmine_centrato)
    


    pygame.display.flip()

    in_attesa = True
    while in_attesa:
        musica_titolo.play()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            global speedAI, speed_max, mode, highscore, file_highscore
            if pygame.key.get_pressed()[pygame.K_z] and pygame.key.get_pressed()[pygame.K_SPACE]:
                    speed_max = 1.8
                    speedAI = 4
                    mode = "easy"
                    in_attesa = False
            if pygame.key.get_pressed()[pygame.K_x] and pygame.key.get_pressed()[pygame.K_SPACE]:
                speed_max = 2.5
                speedAI = 5
                mode = "medium"
                in_attesa = False
            if pygame.key.get_pressed()[pygame.K_c] and pygame.key.get_pressed()[pygame.K_SPACE]:
                speed_max = 3.4
                speedAI = 5.75
                mode = "hard"
                in_attesa = False
            with open(f"highscore_dodge_attack_v_1.0.0{mode}.txt", "r") as file_highscore:
                highscore = int(file_highscore.read())

def game_loop():
    musica_titolo.stop()
    musica_gioco.play()
    pausa = False
    with open(f"highscore_dodge_attack_v_1.0.0{mode}.txt", "r") as file_highscore:
        highscore = int(file_highscore.read())
    scattando = False
    durata_scatto = 5000 #ms
    scatto = False
    fine_scatto = 0  
    fine_scatto = pygame.time.get_ticks()
    ripristino_scatto = random.randint(5000, 15000) #ms

    larghezza_finestra=1350
    altezza_finestra=800
    raggio_pl = 35
    raggio_random = 50 # Giocatore e cerchi random
    raggioAI = 20 # AI predator
    raggio_scatto = 30
    punteggio = 0
    speed = 5
    highscoring = False

    angle1 = random.uniform(0, 2 * math.pi)
    speed_x1 = math.cos(angle1) * 4
    speed_y1 = math.sin(angle1) * 4

    angle2 = random.uniform(0, 2 * math.pi)
    speed_x2 = math.cos(angle2) * 4
    speed_y2 = math.sin(angle2) * 4
    screen = pygame.display.set_mode((larghezza_finestra,altezza_finestra))
    screen.fill((0,0,0))
    clock=pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    titolo = pygame.display.set_caption("Dodge Attack")
    running = True

    x=larghezza_finestra//2 # Giocatore
    y=altezza_finestra//2 # Giocatore
    x1 = 330 #cerchio random
    y1 = 150 #cerchio random
    x2 = 100 #cerchio random
    y2 = 180 #cerchio random
    x3= 150 # AI predator
    y3= 150 # AI predator
    x_scatto = random.randint(raggio_scatto,larghezza_finestra)
    y_scatto = random.randint(100+raggio_scatto, altezza_finestra)

    target3 = (x,y)
    text_outro = font_2.render("Game Over!", True, (0,0,0))
    text_new_highscore = font_2.render("New highscore!", True, (0,0,0))
    intro = False
    circle_scatto = False


    def animazione_finale():
        pygame.display.flip()
        suono_esplosione.play()
        pygame.time.wait(100)
        screen.fill((255,255,255))
        screen.blit(esplosione_2, (x,y))
        pygame.display.flip()
        pygame.time.wait(100)
        screen.fill((255,255,255))
        screen.blit(esplosione_3, (x,y))
        pygame.display.flip()
        pygame.time.wait(100)
        screen.fill((255,255,255))
        screen.blit(esplosione_4, (x,y))
        pygame.display.flip()
        pygame.time.wait(100)
        screen.fill((255,255,255))
        screen.blit(esplosione_5, (x,y))
        pygame.display.flip()
        pygame.time.wait(100)
        screen.fill((255,255,255))
        screen.blit(esplosione_6, (x,y))
        pygame.display.flip()
        pygame.time.wait(100)
        screen.fill((255,255,255))
        pygame.display.flip()
        text_outro_centrato = text_outro.get_rect(center = (larghezza_finestra//2, altezza_finestra//2))
        screen.blit(text_outro,(text_outro_centrato))
        if highscoring:
            screen.blit(text_new_highscore, (text_outro_centrato[0]-90,text_outro_centrato[1]+100))
        pygame.display.flip()
        pygame.time.wait(2000)

    def move_towards(x, y, target, speed):
        tx, ty = target
        dx = tx - x
        dy = ty - y
        dist = math.hypot(dx, dy)
        if dist == 0:
            return x, y
        step = min(speed, dist)
        x += dx / dist * step
        y += dy / dist * step
        return x, y

    running = True 
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and pausa == False:
                if event.key == pygame.K_p:
                    screen.blit(start, (altezza_finestra//2, altezza_finestra//2))
                    pausa = True
                    pygame.display.flip()
            elif pausa == True:
                if event.type == pygame.KEYDOWN and pausa == True:
                    if event.key == pygame.K_p:
                        pausa = False
            
        if pausa == False:
            if intro == False:
                text_intro = font_2.render("3", True, (0,0,0))
                screen.fill((255,255,255))
                screen.blit(text_intro,(larghezza_finestra//2, altezza_finestra//2))
                pygame.display.flip()
                suono_countdown.play()
                pygame.time.wait(1000)
                screen.fill((255,255,255))

                text_intro = font_2.render("2", True, (0,0,0))
                screen.blit(text_intro,(larghezza_finestra//2, altezza_finestra//2))
                pygame.display.flip()
                screen.fill((255,255,255))
                pygame.time.wait(1000)

                text_intro = font_2.render("1", True, (0,0,0))
                screen.blit(text_intro,(larghezza_finestra//2, altezza_finestra//2))
                pygame.display.flip()
                screen.fill((255,255,255))
                suono_countdown.play()
                pygame.time.wait(1000)

                text_intro = font_2.render("Go!", True, (0,0,0))
                screen.blit(text_intro,(larghezza_finestra//2, altezza_finestra//2))
                pygame.display.flip()
                screen.fill((255,255,255))
                pygame.time.wait(1000)

                intro = True

            current_time = pygame.time.get_ticks()
            text_punteggio = font_1.render(f"punteggio: {int(punteggio/10)}", True, (0,0,0))
            screen.blit(text_punteggio,(larghezza_finestra//8,20))
            if punteggio//10 > highscore:
                highscoring = True
                highscore = punteggio//10
            text_highscore = font_1.render(f"highscore: {int(highscore)}", True, (0,0,0))
            screen.blit(text_highscore,(larghezza_finestra/2,20))
            punteggio += 10
            if punteggio > 3000 and speed_x1<speed_max and speed_y1 < speed_max:
                speed_x1 *= 1.002
                speed_y1 *= 1.002
            if punteggio > 3000 and speed_x2<speed_max and speed_y2 < speed_max:
                speed_x2 *= 1.002
                speed_y2 *= 1.002

            x3, y3 = move_towards(x3, y3, target3, speedAI)

            target3 = (x,y)


            if pygame.key.get_pressed()[pygame.K_a] and x > raggio_pl :
                x += -speed
            if pygame.key.get_pressed()[pygame.K_d] and x < larghezza_finestra-raggio_pl:
                x += speed
            if pygame.key.get_pressed()[pygame.K_w] and y > raggio_pl+100:
                y += -speed
            if pygame.key.get_pressed()[pygame.K_s] and y < altezza_finestra-raggio_pl:
                y += speed
            if pygame.key.get_pressed()[pygame.K_SPACE] and scatto:
                speed = 10
                inizio_scatto = pygame.time.get_ticks()
                scattando = True
                scatto = False
            if scatto and not scattando:
                screen.blit(fulmine_imm, (1200,20))

            tempo_scatto_attuale = pygame.time.get_ticks()
            if scattando == True:
                tempo_trascorso_scatto = tempo_scatto_attuale - inizio_scatto
                if tempo_trascorso_scatto > durata_scatto:
                    scattando = False
                    speed = 5
                    ripristino_scatto = random.randint(5000, 15000) #ms
                    fine_scatto = pygame.time.get_ticks()


                

            pygame.draw.circle(screen, (0, 0, 255), (int(x1), int(y1)), raggio_random)

            if fine_scatto+ripristino_scatto < pygame.time.get_ticks() and not scatto and not scattando:
                fulmine_centrato = fulmine_imm.get_rect(center = (x_scatto, y_scatto))
                pygame.draw.circle(screen, (255,255,0), (x_scatto, y_scatto), raggio_scatto)
                screen.blit(fulmine_imm, fulmine_centrato)


            
            if x1+raggio_random > larghezza_finestra or x1 - raggio_random< 0:
                speed_x1 *= -1
            if y1+raggio_random > altezza_finestra or y1 - raggio_random < 100:
                speed_y1 *= -1
            if x2+raggio_random > larghezza_finestra or x2 - raggio_random < 0:
                speed_x2 *= -1
            if y2+raggio_random > altezza_finestra or y2 - raggio_random < 100:
                speed_y2 *= -1
            x1 += speed_x1
            y1 += speed_y1
            x2 += speed_x2
            y2 += speed_y2


            pygame.draw.circle(screen, (0, 0, 255), (int(x2), int(y2)), raggio_random)
            pygame.draw.circle(screen, (100, 50, 150), (int(x3), int(y3)), raggioAI)
            clock.tick(60)
            circle = pygame.draw.circle(screen, (0,255,0), (x,y), raggio_pl)
            pygame.display.flip()
            screen.fill((255,255,255))

            distanza = math.hypot(x_scatto - x, y_scatto - y)
            if distanza < raggio_pl + raggio_scatto and not scatto and not scattando:
                scatto = True

            distanza = math.hypot(x1 - x, y1 - y)
            if distanza < raggio_pl + raggio_random:
                running = False
                animazione_finale()
            distanza = math.hypot(x2 - x, y2 - y)
            if distanza < raggio_pl + raggio_random:
                running = False
                animazione_finale()
            distanza = math.hypot(x3 - x, y3 - y)
            if distanza < raggio_pl+raggioAI:
                running = False
                animazione_finale()
    if punteggio // 10 > highscore:
        with open(f"highscore_Dodge_Attack_v_1.0.0{mode}.txt", "w") as highscore_file:
            highscore_file.write(str(highscore))


while True:
    schermata_principale()
    game_loop()
    if not running: break
pygame.quit()