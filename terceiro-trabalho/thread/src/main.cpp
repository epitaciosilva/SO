#include <iostream>
#include <thread>
#include <mutex>
#include <vector>
int n = 100000;

bool shared_n(int num)
{
    // para evitar aqueles erros citados coloquei um mutex
    // pras threads acessarem o valor n um por vez
    std::mutex mu;
    mu.lock();
    n -= num;
    mu.unlock();
    // std::cout << n << " ";
    return n;
}

bool isPrime(int num)
{
    int b = shared_n(num); // Eu esperava que a função me trouxesse o número atualizado, mas não traz
    // std::cout << b << std::endl;
    int resultado = 0;
    for (int i = 2; i <= n / 2; i++)
    {
        if (n % i == 0)
        {
            resultado++;
        }
    }
    
    // esses valores ainda estão meio cagados, tem número negativo e tals
    if (resultado == 0)
    {
        std::cout << n << ": Primo!" << std::endl;
    }
    else
    {
        std::cout << n << ": Não!" << std::endl;
    }
    // return resultado == 0;
}

int main()
{
    static const int t = 2;
    std::thread threads[t];

    for (int i = 0; i < n; ++i) // percorre os n numeros
    {
        for (int j = 0; j < t; ++j) // percorre as threads
        {
            threads[j] = std::thread(isPrime, i+1); // atribui threads ao vetor e manda número n pra função isPrime
        }
        
        // Sem esperar para matar as threads dá segmentation
        for (int j = 0; j < t; ++j)
        {
            threads[j].join();
        }
    }

    // prime_thread.join();

    // if (isPrime(i)) {
    //     std::cout << i << ": Primo!" << std::endl;
    // } else {
    //     std::cout << i << ": Não!" << std::endl;
    // }
    // }

    return 0;
}