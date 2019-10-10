import sys
import time
import math
import random
import pygame
import socket, pickle
import select
import tkinter as tk
from tkinter import messagebox
from snake import snake, cube, randomSnack, redrawWindow

def start_server():
    port = 65432

    read_list = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setblocking(0)
        s.bind(('', port))
        s.listen(5)
        read_list.append(s)
        while True:
            readable, writeable, error = select.select(read_list,[],[])
            for sock in readable:
                if sock is s:
                    conn, addr = sock.accept()
                    print("connection received from ", addr)
                    read_list.append(conn)
                    data = conn.recv(4096)
                    snake = pickle.loads(data) #recebe snake do socket
                    if(snake):
                        main(snake)
                else:
                    data = sock.recv(1024)
                    if data:
                        print("received", repr(data))
                        sock.send(data)
                    else:
                        sock.close()
                        read_list.remove(sock)

def main(snk):
    # global width, rows, s, snack
    s = snake((255,0,0), (10,10))
    s.body = snk
    # start_server()
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
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
            if s.body != [] and s.body[0].pos == i.pos:
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

start_server()