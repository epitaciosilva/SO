from utils import *

def multiplicacao_matrizes_processos(row_a, col_a, index_row, index_col, processo, results):
    processo = os.fork()
    soma = 0
    if processo == 0: # se o processo for filho
        for i in range(len(row_a)):
            soma += row_a[i] * col_a[i]
        results[index_row][index_col] = soma
    return processo

def get_col(arr, col):
    return list(map(lambda x : x[col], arr))

def multiplicacao_matrizes_threads(row_a, col_b, index_row, index_col, results):
    threading.currentThread()

    soma = 0
    for i in range(len(row_a)):
        soma += row_a[i] * col_b[i]
    
    results[index_row][index_col] = soma

def unroll(args, func, method, results):
    # matriz_aleatoria = matriz_randomica(len(args[0]), random.randint(1,3))
    matriz_aleatoria = [[1,2],[3,4]]
    # ---------- Threads ----------
    # A soma de cada elemento é feito dentro de uma thread
    if method == "thre":
        # List das threads criadas
        threads = []

        # Dimensão das matrizes
        cols = len(matriz_aleatoria[0])
        rows = len(matriz_aleatoria)

        results = [[0 for i in range(cols)] for j in range(len(args))]

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
        rows = len(matriz_aleatoria)
        results = [[0 for i in range(cols)] for j in range(len(args))]
        for j in range(cols):
            m = []
            for i in range(rows):
                m.append(matriz_aleatoria[i][j])
            for index, arg in enumerate(args):
                processos.append([])
                processo = func(arg, m, index, j, processos[-1], results)
                processos[-1] = processo

        if len(list(filter(lambda x: x != 0, processos))) == 0: # verifica se todos os processos são filhos
            print("------ Args ------")
            print_matriz(args)
            print("\n------ Aleatoria ------")
            print_matriz(matriz_aleatoria)
            print("\n------ Matriz multiplicada ------")
            print_matriz(results)
            
            

if __name__ == '__main__':
    res = []
    unroll([[-1,3],[4,2]], multiplicacao_matrizes_processos, 'proc', res)
    # unroll([[2,3,1],[-1, 0, 2]], multiplicacao_matrizes_threads, 'thre', res)
