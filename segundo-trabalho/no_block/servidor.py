import socket
import select
import time
import sys
from snake import snake, redrawWindow, cube, randomSnack

port = 65432

def start_server():
	read_list = []
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.setblocking(0)
		s.bind(('', port))
		s.listen(5)
		read_list.append(s)

		while True :
			# Adicionar timeout para que o servidor não pare, fique sempre atualizando
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
						print("received", repr(data))
						sock.send(data)
					else:
						sock.close()
						read_list.remove(sock)

		
def main ():
    snakes = []
    width = 500
    rows = 30
    win = pygame.display.set_mode((width, width))
    # s = snake((random.randint(0,255),random.randint(0,255),random.randint(0,255)), (random.randint(0,30),random.randint(0,30)))
    snakes.append(s)
    snack = []
    snack.append(cube(randomSnack(rows, s), color=(0,255,0)))
    snake.redrawWindow(win, width, rows, snakes, snack)