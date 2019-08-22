import os
import random
import threading

def matriz_randomica(rows, cols):
    matriz = []
    for i in range(rows):
        matriz.append([])
        for j in range(cols):
            matriz[i].append([])
            matriz[i][j] = random.randint(0,10)
    return matriz

def soma_matrizes_threads(rowA, rowB, results):
    threading.currentThread()
    
    linha_somada = []
    for a,b in zip(rowA, rowB):
        linha_somada.append(b+a) # soma das matrizes

    results.append(linha_somada)

def soma_matrizes_processos(rowA, rowB, processo, results):
    processo = os.fork()
    if processo == 0:
        linha_somada = []
        for a,b in zip(rowA, rowB):
            linha_somada.append(b+a) # soma das matrizes

        results.append(linha_somada)  

def print_matriz(matriz):
    """Imprime matriz na tela, desde que ela tenha o formato [[]]"""
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            print(matriz[i][j], end=(", " if len(matriz[i])-1 != j else ""))
        print()

def unroll(args, func, method, results):
    matriz_aleatoria = matriz_randomica(len(args), len(args[0]))

    # ---------- Threads ----------
    # Acredito que esteja finalizada, nao sei se tem algo errado ou faltando
    if method == "thre":
        threds = []
        for arg, row_aleatoria in zip(args, matriz_aleatoria):
            threds.append([])
            threds[-1] = threading.Thread(target=func, args=(arg, row_aleatoria, results))
            threds[-1].start()

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
    unroll([[0, 1,3],[2,3,4],[4,5,7]], soma_matrizes_processos, 'proc', res)
    # unroll([[0, 1, 3, 4, 5],[2, 3, 1, 2, 3],[4, 5, 4, 2, 5]], soma_matrizes_threads, 'thre', res)