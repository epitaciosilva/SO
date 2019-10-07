import math
import time
import random
import pygame
from snake import snake, cube, randomSnack, redrawWindow
import tkinter as tk
from tkinter import messagebox

def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((255,0,0), (10,10))
    
    snack = []
    snack.append(cube(randomSnack(rows, s), color=(0,255,0)))
    flag = True
    clock = pygame.time.Clock()
    t = time.clock()
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if (time.clock() - t) > 0.5: # recupera o tempo
            snack.append(cube(randomSnack(rows, s), color=(0,255,0)))
            t = time.clock() # reseta clock
        
        for i in snack:
            if s.body[0].pos == i.pos:
                s.addCube()
                snack.remove(i)
                snack.append(cube(randomSnack(rows, s), color=(0,255,0)))
                # break

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                # print('Score: ', len(s.body))
                # message_box('You Lost!', 'Play again...')
                for i in s.body:
                    snack.append(cube(i.pos, color=(0,255,0)))
                    # s.body.remove(i)
                s.reset((10,10))
                break
        redrawWindow(win, rows, width, s, snack)
    pass

main()
