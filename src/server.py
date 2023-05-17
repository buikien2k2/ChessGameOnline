import socket, sys
from _thread import *
import time
import pygame
from src.const import *


#FPS
FPS = 60
CLOCK = pygame.time.Clock()


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1]), int(str[2]), int(str[3])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2]) + "," + str(tup[3])

class Server:
    def __init__(self):
        self.canvas = pygame.Surface((width_menu, height_menu))
        self.SCREEN = pygame.display.set_mode((width_menu,height_menu))
        self.BACKGROUND1 = pygame.transform.scale(pygame.image.load(f"assets/background/chessmainmenuBG1.jpg").convert_alpha(),(width_menu,height_menu))
        
        self.currentPlayer = 0
        self.SERVER = "10.0.2.15"
        self.port = 5555
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind = self.bind()
        self.clients = []
        self.pos = [(0,0,0,0),(1,1,1,1)]
        self.start_time = time.time()
        self.end_time = self.start_time + 40
        self.font1 = pygame.font.SysFont("Arial", 30)
        self.font2 = pygame.font.SysFont("Arial", 40)
        
    def bind(self):
        try:
            self.s.bind((self.SERVER, self.port))
        except socket.error as e:
            str(e)         
        self.s.listen(2)
        print("waiting for connect........")

    #title
    def title_menu(self,title, color,x, y):
        title_text = self.font2.render(title, True, color)
        title_rect = title_text.get_rect(center=(x, y))
        self.SCREEN.blit(title_text, title_rect) 

    # button
    def button(self, text, color, x, y):
        button_text = self.font1.render(text, True, color)
        button_rect = button_text.get_rect(center=(x, y))
        self.SCREEN.blit(button_text, button_rect) 
        return button_rect

    # def server(self):
    #     SERVER_GET = self.SERVER
    #     text_box = pygame.Rect(260, 230, 300, 50)
    #     run = True
    #     active = False
    #     while run:
    #         mx, my = pygame.mouse.get_pos()
    #         self.BACKGROUND1.set_alpha(100)
    #         self.canvas.fill(BLACK)
    #         self.canvas.blit(self.BACKGROUND1, (0,0))
    #         self.SCREEN.blit(self.canvas,(0,0,0,0))
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #                 sys.exit()
    #             if event.type == pygame.MOUSEBUTTONDOWN:
    #                 if button1.collidepoint((mx, my)):
    #                     self.waitingforPlayer()
    #                 if text_box.collidepoint((mx, my)):
    #                     active = True
    #                 else:
    #                     active = False
    #             if event.type == pygame.KEYDOWN:
    #                 if active:
    #                     if event.key == pygame.K_BACKSPACE:
    #                         SERVER_GET = SERVER_GET[:-1]
    #                     else:
    #                         SERVER_GET += event.unicode


    #         surf_text = self.font2.render(SERVER_GET, True, WHITE)
    #         self.SCREEN.blit(surf_text, (text_box.x +15, text_box.y +10)) 
    #         text_box.w = max(300, surf_text.get_width()+30)
    #         pygame.draw.rect(self.SCREEN, WHITE, text_box, 2)
    #         button1 = self.button("Init", WHITE, 400, 320)
            
    #         self.title_menu("Sever IP", WHITE, 400, 200)
    #         pygame.display.update()
    #         CLOCK.tick(FPS)
        

    # def waitingforPlayer(self):
    #     run = True
    #     while run:
    #         time_left = int(max(0, self.end_time - time.time()))
    #         mx, my = pygame.mouse.get_pos()
    #         self.BACKGROUND1.set_alpha(100)
    #         self.canvas.fill(BLACK)
    #         self.canvas.blit(self.BACKGROUND1, (0,0))
    #         self.SCREEN.blit(self.canvas,(0,0,0,0))
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #                 sys.exit()
    #         self.title_menu("Waiting for Player", WHITE, 400, 300)
    #         self.title_menu(str(time_left), WHITE, 400, 250)
    #         if time_left == 0:
    #             self.Reconnect(self.SCREEN)
    #         pygame.display.update()
    #         CLOCK.tick(FPS)

    
    # def Reconnect(self, screen):
    #     run = True
    #     while run:
    #         mx, my = pygame.mouse.get_pos()
    #         self.BACKGROUND1.set_alpha(100)
    #         self.canvas.fill(BLACK)
    #         self.canvas.blit(self.BACKGROUND1, (0,0))
    #         self.SCREEN.blit(self.canvas,(0,0,0,0))
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #                 sys.exit()
    #             if event.type == pygame.MOUSEBUTTONDOWN:
    #                 if button1.collidepoint((mx, my)):
    #                     Server().main()
    #         button1 = self.button("Reconnect", WHITE, 400, 300) 
    #         pygame.display.update()

    def threaded_client(self, conn, player):
        pos = self.pos
        conn.send(str.encode(make_pos(pos[player])))
        
        reply = ""
        
        while True:
            try:
                data = read_pos(conn.recv(4096*8).decode())
                pos[player] = data
                if not data:
                    print("Disconnected")
                    break
                else:
                    if player == 1:
                        reply = pos[0]
                    else:
                        reply = pos[1]
                    print("Receive: ", data)
                    print("Sending: ", reply)
                conn.sendall(str.encode(make_pos(reply)))
            except:
                break

        print("Lost connection")
        conn.close()

    def main(self):
        s = self.s
        currentPlayer = self.currentPlayer
        # self.server()
        run = True
        while run:
            # self.waitingforPlayer()
            
            conn, addr = s.accept()
            print("Connected to: ", addr)
            self.clients.append(addr)
            start_new_thread(self.threaded_client, (conn, currentPlayer))

            currentPlayer += 1
            


# server = Server()
# server.main()