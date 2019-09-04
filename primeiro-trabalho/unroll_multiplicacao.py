import os
import random
import threading

def matriz_randomica(rows, cols):
    matriz = [[1,0,0], [0,1,0], [0,0,1]]

    # for i in range(rows):
    #     matriz.append([])
    #     for j in range(cols):
    #         matriz[i].append([])
    #         matriz[i][j] = random.randint(0,10)
    return matriz

def multiplicacao_matrizes_processos(rowA, rowB, processo, results):
    processo = os.fork()
    if processo == 0:
        linha_somada = []
        for a,b in zip(rowA, rowB):
            linha_somada.append(b+a) # soma das matrizes

        results.append(linha_somada)  

def multiplicacao_matrizes_threads(row_A, col_B, results):
    threading.currentThread()
    soma = 0
    for i in range(len(row_A)):
        soma += row_A[i] + col_B[i]
    
    results[-1] = soma

def print_matriz(matriz):
    """Imprime matriz na tela, desde que ela tenha o formato [[]]"""
    print(matriz)
    # for i in range(len(matriz)):
    #     for j in range(len(matriz[i])):
    #         print(matriz[i][j], end=(", " if len(matriz[i])-1 != j else ""))
    #     print()

def unroll(args, func, method, results):
    matriz_aleatoria = matriz_randomica(len(args), len(args[0]))

    # ---------- Threads ----------
    # A soma de cada elemento é feito dentro de uma thread
    if method == "thre":
        # List das threads criadas
        threads = []

        # Dimensão das matrizes
        cols = len(matriz_aleatoria[0])
        rows = len(matriz_aleatoria)

        results = [0 for j in range(rows)]

        for j in range(cols):
            for arg in args:
                m = []
                for i in range(rows):
                    m.append(matriz_aleatoria[i][j])  
                print(m)
                threads.append([])
                threads[-1] = threading.Thread(target=func, args=(arg, m, results))
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

        for arg, row_aleatoria in zip(args, matriz_aleatoria):
            processos.append([])
            func(arg, row_aleatoria, processos[-1], results)            

        print("------ Args ------")
        print_matriz(args)

        print("\n------ Aleatoria ------")
        print_matriz(matriz_aleatoria)

        print("\n------ Matriz soma ------")
        print_matriz(results)

if __name__ == '__main__':
    res = []
    # unroll([[0, 1,3],[2,3,4],[4,5,7]], multiplicacao_matrizes_processos, 'proc', res)
    unroll([[0, 1, 3],[2, 3, 1],[4, 5, 4]], multiplicacao_matrizes_threads, 'thre', res)