#include <iostream>
#include <thread>
#include <mutex>
#include <math.h>

int n = 100000;

void shared_n(int num)
{
    // para evitar aqueles erros citados coloquei um mutex
    // pras threads acessarem o valor n um por vez
    std::mutex mu;
    mu.lock();
    n -= num;
    mu.unlock();
}

void isPrime(int k)
{
    // shared_n(num);

    int resultado = 0;
    for (int i = 2; i <= k / 2; i++)
    {
        if (k % i == 0)
        {
            resultado++;
        }
    }

    // esses valores ainda estão meio cagados, tem número negativo e tals
    // if (k < 0)
    // {

    //     if (resultado == 0)
    //     {
    //         std::cout << k << ": Primo!" << std::endl;
    //     }
    //     else
    //     {
    //         std::cout << k << ": Não!" << std::endl;
    //     }
    // }
}

int main()
{
    static const int t = 4;
    std::thread threads[t];
    int ns[t]; // cria n da threads

    // Se o número n for par ele se torna ímpar
    if (n % 2 == 0)
    {
        n -= 1;
    }

    for (int j = 0; j < t; ++j)
    {
        ns[j] = n;
    }

    int k = n;

    for (int i = 0; i < k; ++i) // percorre os n numeros
    {
        for (int j = 0; j < t; ++j) // percorre as threads
        {
            threads[j] = std::thread(isPrime, (ns[j] - (pow(t, (j + 1))))); // atribui threads ao vetor e manda número n pra função isPrime
            ns[j] -= pow(t, (j + 1));
        }

        // Sem esperar as threads dá segmentation
        for (int j = 0; j < t; ++j)
        {
            threads[j].join();
        }
    }

    return 0;
}