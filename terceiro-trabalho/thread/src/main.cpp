#include <iostream>
#include <thread>
#include <vector>
#include <mutex>

int n = 1000;
std::mutex mtx;

bool isPrime(int num)
{
    bool resultado = true;
    for (int i = 2; i <= num / 2; i++)
    {
        if (num % i == 0)
        {
            resultado = false;
        }
    }

    return resultado;
}

void threadFunc(int num) {
    if (isPrime(num)) {
        // std::cout << num << std::endl;
    }
    mtx.lock();
    n--;
    mtx.unlock();
}

int main()
{
    int n = 10000;
    int numThreads = 6;
    std::thread threads[numThreads];
    
    for (int i = 2; i <= n; i += 2)
    {
        for (int j = 0; j < numThreads; j++) {
            threads[j] = std::thread(threadFunc, i + j);
        }

        for (int j = 0; j < numThreads; j++) {
            threads[j].join();
        }
    }
}