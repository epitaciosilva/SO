import os
import random
import threading
from multiprocessing import Queue

def matriz_randomica(rows, cols):
    matriz = []

    for i in range(rows):
        matriz.append([])
        for j in range(cols):
            matriz[i].append([])
            matriz[i][j] = random.randint(0,10)
    return matriz

def multiplicacao_matrizes_processos(row_a, col_a, processo, results):
    processo = os.fork()
    if processo == 0: # se o processo for filho
        results.append([a*b for a,b in zip(row_a, col_a)])

def get_col(arr, col):
    return list(map(lambda x : x[col], arr))

def multiplicacao_matrizes_threads(row_a, col_b, index_row, index_col, results):
    threading.currentThread()

    soma = 0
    for i in range(len(row_a)):
        soma += row_a[i] * col_b[i]
    
    results[index_row][index_col] = soma

def print_matriz(matriz):
    """Imprime matriz na tela, desde que ela tenha o formato [[]]"""
    for i in range(len(matriz)):
        print("|", end=" ")
        for j in range(len(matriz[i])):
            print(matriz[i][j], end=(", " if len(matriz[i])-1 != j else ""))
        print(" |")

def unroll(args, func, method, results):
    # matriz_aleatoria = matriz_randomica(len(args[0]), random.randint(1,3))
    matriz_aleatoria = [[1,1,1],[1,1,1],[1,1,1]]
    # ---------- Threads ----------
    # A soma de cada elemento é feito dentro de uma thread
    if method == "thre":
        # List das threads criadas
        threads = []

        # Dimensão das matrizes
        cols = len(matriz_aleatoria[0])
        rows = len(matriz_aleatoria)

        results = [[0 for i in range(cols)] for j in range(rows)]

        for j in range(cols):
            m = []
            for i in range(rows):
                m.append(matriz_aleatoria[i][j])
            for index, arg in enumerate(args):
                threads.append([])
                threads[-1] = threading.Thread(target=func, args=(arg, m, index, j, results))
                threads[-1].start() 

        print("------ Args ------")
        print_matriz(args)

        print("\n------ Aleatoria ------")
        print_matriz(matriz_aleatoria)

        print("\n------ Matriz soma ------")
        print_matriz(results)
    
    # ---------- PROCESSOS ----------
    # Ainda não esta pronto, eh preciso fazer com os processos se comuniquem
    # provavelmente com memoria compartilhada so assim pra conseguir salvar os results 
    # de cada soma das linhas da matriz.
    # No caso o processo original devera imprimir a soma completa da matriz
    else:
        processos = []
        # Dimensão das matrizes
        cols = len(matriz_aleatoria[0])
        # rows = len(matriz_aleatoria)
        # arg = []
        for arg in args:
            for col in range(cols):
                processos.append([])
                func(arg, get_col(matriz_aleatoria,col), processos[-1], results)
                break
        
        # for arg, row_aleatoria in zip(args, matriz_aleatoria):
        #     processos.append([])
        #     func(arg, row_aleatoria, processos[-1], results)            

        print("------ Args ------")
        print_matriz(args)

        print("\n------ Aleatoria ------")
        print_matriz(matriz_aleatoria)

        print("\n------ Matriz multiplicada ------")
        print_matriz(results)

if __name__ == '__main__':
    res = []
    # results = Queue()
    unroll([[0, 1, 3],[2, 3, 1],[4, 5, 4]], multiplicacao_matrizes_processos, 'proc', res)
    # unroll([[0, 1, 3],[2, 3, 1],[4, 5, 4]], multiplicacao_matrizes_threads, 'thre', res)