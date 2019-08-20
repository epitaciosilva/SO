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

def soma_matrizes(matrizA, matrizB):
    matriz = []
    for a, b in zip(matrizA, matrizB):
        aux = []
        for i in range(len(a)):  # indice para somar as duas matrizes
            aux.append(b[i]+a[i]) # soma das matrizes
        matriz.append(aux)
    return matriz

def func(*args):
    for arg in args:
        print(str(arg), end=", ")
    print()

def print_matriz(matriz):
    """Imprime matriz na tela, desde que ela tenha o formato [[]]"""
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            print(matriz[i][j], end=(", " if len(matriz[i])-1 != j else ""))
        print()

def func_thread(matrizA, matrizB):
    threading.currentThread()
    matriz = soma_matrizes(matrizA, matrizB)
    print("\n----- Matriz resultante da soma -----")
    print_matriz(matriz)


def unroll(args, func, method, results):
    """
    Realiza a soma e multiplicação de duas matrizes quaisquer.

    Cada linha l da matriz args representa uma chamada de func.
    Os parâmetros de cada chamada de func são os elementos das
    linhas da matriz args, quando func retorna alguma coisa, esse
    retorno é armazenado na lista results. O Parâmetro method
    indica se unroll irá implementar o paralelismo das chamadas de 
    func usando processos com a função fork(default) ou usando threads.


    Parâmetros
    ----------
        args: list
            Recebe uma matriz(LxN) de valores.
        func: function
            Função a ser chamada paralelamente.
        results: list
            Armazena retornos da função func (se existir retorno).
        method: str
            Indica o tipo de implementação paralela, thread ou process.
    """
    matriz_aleatoria = matriz_randomica(len(args), len(args[0]))

    # Fork
    if method == 'proc':
        print("Processo filho")
        val = os.fork() # criar-se um novo processo

        # para que as matrizes sejam escritas antes do resultado soma/multiplicacao,
        # eh preciso que isso rode no processo pai/original

        if val != 0: # val != 0 indica que eh o processo original
            print("---- Args ----")
            for i in args:
                results.append(func(i[0], i[1]))

            print("---- Aleatoria ----")
            for i in matriz_aleatoria:
                results.append(func(i[0], i[1]))

        else: # igual a 0 diz que eh do processo filho
            matriz = soma_matrizes(args, matriz_aleatoria)

            print("\n----- Matriz resultante da soma -----")
            for i in matriz:
                func(i[0], i[1])
    # Threads
    else:
        # Com as threads os processo ocorrem simultaneamente, por isso que imprimi as duas coias "ao mesmo tempo"
        # Uma possibilidade eh usar semaforos para impedir que ambas acessem as matrizes simultaneamente.
        t1 = threading.Thread(target=func_thread, args=(args,matriz_aleatoria))
        t1.start()

        # processo principal
        print("\nProcesso " + str(os.getpid()) + " na thread " + str(t1.ident))

        print("\n---- Args ----")   
        for i in args:
            results.append(func(i[0], i[1]))

        print("\n---- Aleatoria ----")
        for i in matriz_aleatoria:
            results.append(func(i[0], i[1]))


if __name__ == '__main__':
    res = []
    # unroll([[0, 1],[2,3],[4,5]], func, 'proc', res)
    unroll([[0, 1],[2,3],[4,5]], func, 'thre', res)
