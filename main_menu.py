import pygame, sys
from src.main import Main
from src.const import *
from src.server import Server
from src.client import Client
import time
import threading

pygame.init()
#config menu
canvas = pygame.Surface((width_menu, height_menu))
SCREEN = pygame.display.set_mode((width_menu,height_menu))
captions = pygame.display.set_caption("Menu Game Chess")

#FPS
FPS = 60
CLOCK = pygame.time.Clock()

#icon
icon = pygame.image.load(f"assets/icon/iconBG2_fix.png")
icon = pygame.transform.scale(icon,(2, 2))
set_icon = pygame.display.set_icon(icon)

#background main menu
BACKGROUND = pygame.transform.scale(pygame.image.load(f"assets/background/chessmainmenuBG0.jpg").convert_alpha(),(width_menu,height_menu))
BACKGROUND1 = pygame.transform.scale(pygame.image.load(f"assets/background/chessmainmenuBG1.jpg").convert_alpha(),(width_menu,height_menu))
BACKGROUND2 = pygame.transform.scale(pygame.image.load(f"assets/background/chessmainmenuBG2.jpg").convert_alpha(),(width_menu,height_menu))

#font chu
font1 = pygame.font.SysFont("Arial", 30)
font2 = pygame.font.SysFont("Arial", 40)
font3 = pygame.font.SysFont("Arial", 80)

#button
Buttons = []
Buttons.append({"text" : "Single", "rect" : None, "hovering": False, "pos" : (200, 130)})
Buttons.append({"text" : "2 Person", "rect" : None, "hovering": False, "pos" : (200, 180)})
Buttons.append({"text" : "Option", "rect" : None, "hovering": False, "pos" : (200, 230)})
Buttons.append({"text" : "Quit", "rect" : None, "hovering": False, "pos" : (200, 280)})
for button in Buttons:
    button_rect = font1.render(button["text"], True, WHITE).get_rect(center=(button["pos"]))
    button["rect"] = button_rect

#game varialbles


# button
def button(text, color, x, y):
    button_text = font1.render(text, True, color)
    button_rect = button_text.get_rect(center=(x, y))
    SCREEN.blit(button_text, button_rect) 
    return button_rect

#title
def title_menu(title, color,x, y):
    title_text = font2.render(title, True, color)
    title_rect = title_text.get_rect(center=(x, y))
    SCREEN.blit(title_text, title_rect) 


    
# def server():
#     SERVER_GET = ""
#     text_box = pygame.Rect(260, 230, 300, 50)
#     run = True
#     active = False
#     while run:
#         mx, my = pygame.mouse.get_pos()
#         BACKGROUND1.set_alpha(100)
#         canvas.fill(BLACK)
#         canvas.blit(BACKGROUND1, (0,0))
#         SCREEN.blit(canvas,(0,0,0,0))
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if button1.collidepoint((mx, my)):
#                     Server(SERVER_GET).main()
#                 if text_box.collidepoint((mx, my)):
#                     active = True
#                 else:
#                     active = False
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     menu_run()
#                 if active:
#                     if event.key == pygame.K_BACKSPACE:
#                         SERVER_GET = SERVER_GET[:-1]
#                     else:
#                         SERVER_GET += event.unicode


#         surf_text = font2.render(SERVER_GET, True, WHITE)
#         SCREEN.blit(surf_text, (text_box.x +15, text_box.y +10)) 
#         text_box.w = max(300, surf_text.get_width()+30)
#         pygame.draw.rect(SCREEN, WHITE, text_box, 2)
#         button1 = button("Init", WHITE, 400, 320)
#         title_menu("Sever IP", WHITE, 400, 200)
#         pygame.display.update()
#         CLOCK.tick(FPS)

def playwithAI():
    SCREEN.fill(BLACK)
    while True:
        Main().mainloop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

def Play2Person():
    # Server_thread = threading.Thread(target= Server().main)
    # Server_thread.start()
   
    run = True
    while run:
        mx, my = pygame.mouse.get_pos()
        BACKGROUND1.set_alpha(100)
        canvas.fill(BLACK)
        canvas.blit(BACKGROUND1, (0,0))
        SCREEN.blit(canvas,(0,0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button3.collidepoint((mx, my)):
                    menu_run()
                if button2.collidepoint((mx,my)):
                    client_thread = threading.Thread(target= Client().mainloop())
                    client_thread.start()
                    # client_thread.join()
                    break
                if button1.collidepoint((mx,my)):
                    Server_thread = threading.Thread(target= Server().main)
                    Server_thread.start()
                    # Server_thread.join()
                    break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_run()
    
        
        title_menu("SERVER CHESS GAME", WHITE, 400, 100)
        button1 = button("Create Room", WHITE, 150, 180)
        button2 = button("Play Random", WHITE, 150, 230)
        button3 = button("Back to menu", WHITE, 150, 280) 
        pygame.display.update()
        CLOCK.tick(FPS)
    # Server_thread.join()
def Option():
    click = False
    while True:
        mx, my = pygame.mouse.get_pos()
        BACKGROUND2.set_alpha(100)
        canvas.fill(BLACK)
        canvas.blit(BACKGROUND2, (0,0))
        SCREEN.blit(canvas,(0,0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button4.collidepoint((mx, my)):
                    menu_run()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_run()

        title_menu("OPTION", WHITE, 400, 50)
        button1 = button("Video", WHITE, 700, 150)
        button2 = button("Key Board", WHITE, 700, 200)
        button3 = button("Bind Controller", WHITE, 700, 250)
        button4 = button("Back", WHITE, 700, 300) 
        
        pygame.display.update()
        CLOCK.tick(FPS)

#main screen
def menu_run():
    SCREEN.fill(BLACK)
    run = True
    while run:
        # BACKGROUND.set_alpha(0)
        
        SCREEN.blit(BACKGROUND,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #Kiem tra xem con chuot co tro vao buton nao hay ko
            elif event.type == pygame.MOUSEMOTION:
                for button in Buttons:
                    if button["rect"].collidepoint(event.pos):
                        button["hovering"] = True
                    else:
                        button["hovering"] = False
            #kiem tra xem nguoi dung co click vao button nao ko
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in Buttons:
                    if button["rect"].collidepoint(event.pos):
                        if button["text"] == "Single":
                            print("Play with AI")
                            playwithAI()
                        elif button["text"] == "2 Person":
                            print("Play with dif person")
                            Play2Person()
                        elif button["text"] == "Option":
                            print("Config")
                            Option()
                        elif button["text"] == "Quit":
                            pygame.quit()
                            sys.exit()
                            
                            
        #Ve cac button
        for button in Buttons:
            #Neu con chuot tro vao thi dich sang ben phai va thay doi mau sac
            if button["hovering"]:
                button_text = font1.render(button["text"], True, BLACK)
                button_rect = button_text.get_rect(center=(button["pos"][0]+20, button["pos"][1]))
            #khong thi giu nguyen
            else:
                button_text = font1.render(button["text"], True, WHITE)
                button_rect = button_text.get_rect(center=(button["pos"][0], button["pos"][1]))
            SCREEN.blit(button_text, button_rect)
        
        title_menu("CHESS GAME ONLINE", WHITE,280, 50)
        pygame.display.update()
        CLOCK.tick(FPS)

menu_run().mainloop()


