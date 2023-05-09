import pygame, sys
from main import Main
from const import *

pygame.init()
#config menu
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
BACKGROUND = pygame.image.load(f"assets/background/chessmainmenuBG0.jpg")
BACKGROUND = pygame.transform.scale(BACKGROUND,(width_menu,height_menu))

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

#title
def title_menu():
    title_text = font2.render("CHESS GAME ONLINE", True, WHITE)
    title_rect = title_text.get_rect(center=(280, 50))
    SCREEN.blit(title_text, title_rect) 

def playwithAI():
    while True:
        Main().mainloop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

#main screen
def main_menu():
    SCREEN.fill(BLACK)
    while True:
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
                        elif button["text"] == "Option":
                            print("Config")
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
        title_menu()
        pygame.display.update()
        CLOCK.tick(FPS)

main_menu().mainloop()

