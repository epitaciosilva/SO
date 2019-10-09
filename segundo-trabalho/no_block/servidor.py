import socket
import select
import time
import sys
from snake import snake, redrawWindow, cube, randomSnack

port = 65432
snakes = []
width = 500
rows = 30
tabuleiro = [[[0,0] for j in range(0,rows)] for i in range(0,rows)]
colors_all_snakes = [(0,255,0)] 
# win = pygame.display.set_mode((width, width))
# s = snake((random.randint(0,255),random.randint(0,255),random.randint(0,255)), (random.randint(0,30),random.randint(0,30)))
# snakes.append(s)
# snack = []
# snack.append(cube(randomSnack(rows, s), color=(0,255,0)))
# snake.redrawWindow(win, width, rows, snakes, snack)

def randomColor():
	color = (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
	while color in colors_all_snakes:
		color = (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
	
	colors_all_snakes.append(color)
	return color

def randomPosition():
	x = random.randint(0,30)
	y = random.randint(0,30)

	while tabuleiro[x][y][0] != 0:
		x = random.randint(0,30)
		y = random.randint(0,30)
	
	tabuleiro[x][y][0] = 1
	return [x,y]

def start_server():
	read_list = []
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.setblocking(0)
		s.bind(('', port))
		s.listen(5)
		read_list.append(s)

		while True :
			readable, writeable, error = select.select(read_list,[],[])
			for sock in readable:
				if sock is s:
					conn, info = sock.accept()
					read_list.append(conn)
					conn.setblocking(0)
					
					print("connection received from ", info)	
				else:
					data = sock.recv(1024)
					if data:
						# Converter para bytes e mandar para o cliente a cor e o tabuleiro
						# lá que será feito a represntação do jogo através do tabuleiro
						position = randomPosition()
						color_snake = randomColor()
						tabuleiro[position[0]][position[1]][1] = color_snake
						print("received", repr(data))
						sock.send(data)
					else:
						sock.close()
						read_list.remove(sock)

start_server()

def main ():
    snakes = []
    width = 500
    rows = 30
    win = pygame.display.set_mode((width, width))
    snakes.append(s)
    snack = []
    snack.append(cube(randomSnack(rows, s), color=(0,255,0)))
    snake.redrawWindow(win, width, rows, snakes, snack)