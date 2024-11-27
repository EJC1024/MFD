import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from BaseClasses import Colors, Quad
from Utilities import gl_init_2d
import Globals
#from KspWireless import begin_wireless 

def draw_statics():
    static_select_backround = Quad(100, 0, 600, 25, Colors.Background)
    background_divider = Quad(200, 0, 2, 25, Colors.White)

    static_select_backround.draw()
    static_select_backround.y = 575
    static_select_backround.draw()

    for y in range(2):
        for x in range(5):
            background_divider.draw()
            background_divider.x += 100
        
        background_divider.y = 575
        background_divider.x = 200
    background_divider.y = 0
    static_select_backround.y = 0

def main():
    pygame.init()
    screen = pygame.display.set_mode((1024, 600), pygame.DOUBLEBUF | pygame.OPENGL)
    clock = pygame.time.Clock()

    Globals.init_screens()
    Globals.init_menu_text()
    gl_init_2d()

    screen_number = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:  
                if event.key == pygame.K_RIGHT:
                    screen_number += 1
                    if screen_number >= len(Globals.screen_select):  
                        screen_number = 0

                elif event.key == pygame.K_LEFT:
                    screen_number -= 1
                    if screen_number < 0: 
                        screen_number = len(Globals.screen_select) - 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            Globals.screen_select[1].navball.rotate([1, 0, 0], 1)
        if keys[pygame.K_s]:
            Globals.screen_select[1].navball.rotate([1, 0, 0], -1)
        if keys[pygame.K_a]:
            Globals.screen_select[1].navball.rotate([0, 1, 0], -1)
        if keys[pygame.K_d]:
            Globals.screen_select[1].navball.rotate([0, 1, 0], 1)
        if keys[pygame.K_q]:
            Globals.screen_select[1].navball.rotate([0, 0, 1], 1)
        if keys[pygame.K_e]:
            Globals.screen_select[1].navball.rotate([0, 0, 1], -1)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Globals.screen_select[screen_number].draw()

        draw_statics()

        for texts in Globals.menu_texts:
            texts.draw()
            
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
